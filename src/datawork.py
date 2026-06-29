# data.py
import pandas as pd
from dataclasses import dataclass
import numpy as np
import ast
import matplotlib
matplotlib.use('Agg')  # неблокирующий бэкенд, чтобы не всплывало окно
import matplotlib.pyplot as plt
import json
import os

import config as cfg

@dataclass
class Variables:
    orig_df: pd.DataFrame | None = None
    work_df: pd.DataFrame | None = None
    view_df: pd.DataFrame | None = None
    curr_page: int = None
    work_page: int = None
    tot_pages: int = None
    info = None

# Создаем единственный экземпляр состояния данных
var = Variables()

def load_csv(path: str):
    """Возвращает датафрейм по указанному пути"""
    return pd.read_csv(path)

def get_pages(df, curr_page=1):
    """
    Возвращает текущую страницу и общее число страниц df.
    По умолчанию возвращает первую страницу, но если указать другую, может вернуть её, ЕСЛИ ОНА ВАЛИДНА.
    Валидность текущей страницы проверяется функцией get_current_page().
    """
    return get_current_page(df, curr_page), get_total_pages(df)

def get_total_pages(df):
    """Возвращает количество страниц, необходимое для размещения датафрейма.
    Для пустого df выдаст 0 страниц."""
    if df.empty:
        return 0
    return (len(df) + cfg.MAX_VISIBLE_ROWS - 1) // cfg.MAX_VISIBLE_ROWS

def get_current_page(df, curr_page):
    """
    Возвращает номер текущей страницы, для датафрейма, предварительно прогоняя его по условию выхода за пределы диапазона общего числа страниц.
    """
    tot_pages = get_total_pages(df)
    curr_page = check_curr_page(curr_page, tot_pages)
    return curr_page

def check_curr_page(curr_page: int, tot_pages: int):
    """
    Возвращает указанный номер страницы, если он подходит под интервал общего числа страниц. 
    Если общее число страниц равно 0 - вернёт 0 сразу.
    Если общее число страниц больше 0, то возможны три варианта:
    - если указать страницу меньше 1 — вернёт 1.
    - если указать страницу больше общего числа страниц - вернёт общее число страниц.
    - если указать страницу в правильном диапазоне - вернёт её.
    """
    if tot_pages == 0:
        return 0
    if curr_page < 1:
        return 1
    if curr_page > tot_pages:
        return tot_pages
    return curr_page

def get_rows_from_page(df, page):
    """
    Возвращает срез датасета для указанной страницы.
    ПОДРАЗУМЕВАЕТСЯ, ЧТО НУЖНАЯ СТРАНИЦА СУЩЕСТВУЕТ И ДАТАФРЕЙМ НЕ ПУСТ!!!
    """
    start_index = (page - 1) * cfg.MAX_VISIBLE_ROWS
    end_index = start_index + cfg.MAX_VISIBLE_ROWS
    return df.iloc[start_index:end_index]

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет дубликаты из датафрейма и сбрасывает индексы."""
    if df.empty:
        return df
    return df.drop_duplicates().reset_index(drop=True)

def add_column_with_expr(df, col_name, target_dtype, expression):
    """
    Вычисляет выражение, создает колонку и приводит её к типу.
    Возвращает: (новый_df, успех: bool, сообщение: str)
    """
    try:
        # 1. Безопасное окружение для eval. 
        # Разрешаем только df, numpy и pandas. Блокируем __builtins__.
        safe_env = {"df": df, "np": np, "pd": pd, "__builtins__": {}}
        
        # Пытаемся вычислить как выражение (например, df['a'] + df['b'])
        try:
            new_data = eval(expression, safe_env)
        except SyntaxError:
            # Если синтаксическая ошибка, возможно, пользователь ввел просто текст без кавычек (Петя)
            # или число. Пробуем распарсить как литерал Python.
            try:
                new_data = ast.literal_eval(expression)
            except (ValueError, SyntaxError):
                # Если и это не вышло, считаем это просто строкой
                new_data = expression

        # 2. Создаем копию df и добавляем колонку
        df = df.copy()
        df[col_name] = new_data

        # 3. Приводим к нужному типу с обработкой ошибок
        if target_dtype == "string":
            df[col_name] = df[col_name].astype('string')
        elif target_dtype == "category":
            df[col_name] = df[col_name].astype("category")
        elif target_dtype == "bool":
            # Pandas плохо понимает строки в bool, но 0/1 поймет
            df[col_name] = df[col_name].astype(bool)
        elif target_dtype == "float64": # int64, float64
            # errors='raise' вызовет ValueError, если там есть нечисловые символы (например, 'Петя')
            df[col_name] = df[col_name].astype("float64", errors='raise') 
        elif target_dtype == "int64":
            df[col_name] = df[col_name].astype("int64", errors='raise')

        return df, True, f"Колонка '{col_name}' успешно добавлена."

    except Exception as e:
        # Ловим любые ошибки (ошибки вычислений, ошибки приведения типов)
        return df, False, f"Ошибка: {str(e)}"

def get_numeric_columns(df):
    """Возвращает список числовых столбцов (int, float)."""
    if df is None or df.empty:
        return []
    return df.select_dtypes(include=['number']).columns.tolist()

def get_categorical_columns(df):
    """Возвращает список категориальных и логических столбцов."""
    if df is None or df.empty:
        return []
    return df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

def build_hist_figure(df, col, hue_col=None, stacked=False):
    """
    Строит гистограмму.
    Если hue_col не задан — одна гистограмма.
    Если hue_col задан и stacked=False — гистограммы в ряд (subplots).
    Если hue_col задан и stacked=True — гистограмма с накоплением.
    """
    data = df[col].dropna()
    # bins = calculate_bins(data)
    fig = None
    
    if hue_col is None:
        # --- Одиночная гистограмма ---
        fig, ax = plt.subplots()
        ax.hist(data, bins=cfg.BINS, edgecolor=cfg.HIST_BINS_EDGECOLOR, color=cfg.HIST_BINS_COLOR)
        add_normal_curve_and_stats(ax, data, bins=cfg.BINS)
        ax.set_xlabel(col)
        ax.set_ylabel('Частота')
        ax.set_title(f'Гистограмма: {col}')
        # Горизонтальная сетка
        ax.grid(axis='y', alpha=0.4, linestyle='--', color='gray')
        
    else:
        # --- Гистограммы в ряд по категориям ---
        categories = sorted(df[hue_col].dropna().unique())
        
        if stacked:
            # --- Гистограмма с накоплением ---
            data_list = [df[df[hue_col] == cat][col].dropna().values for cat in categories]
            fig, ax = plt.subplots()
            ax.hist(
                data_list,
                bins=cfg.BINS,
                stacked=True,
                edgecolor=cfg.HIST_BINS_EDGECOLOR,
                label=categories
            )
            ax.set_xlabel(col)
            ax.set_ylabel('Частота')
            ax.set_title(f'Гистограмма с накоплением: {col} по {hue_col}')
            ax.legend(title=hue_col, loc='upper right')
            ax.grid(axis='y', alpha=0.4, linestyle='--', color='gray')
        
        else:
            # --- Гистограммы в ряд (subplots) ---
            n = len(categories)
            # Создаём N подграфиков в один ряд. sharey=True — одинаковая шкала Y для сравнения.
            fig, axes = plt.subplots(1, n, sharey=True)
            if n == 1:
                axes = [axes]  # чтобы можно было итерироваться
                
            for ax, cat in zip(axes, categories):
                data = df[df[hue_col] == cat][col].dropna()
                # bins = calculate_bins(data)
                ax.hist(data, bins=cfg.BINS, edgecolor=cfg.HIST_BINS_EDGECOLOR, color=cfg.HIST_BINS_COLOR)
                add_normal_curve_and_stats(ax, data, bins=cfg.BINS)
                ax.set_xlabel(col)
                ax.set_title(f'{hue_col} = {cat}')
                ax.grid(axis='y', alpha=0.4, linestyle='--', color='gray')

            # Подпись оси Y только у первого, чтобы не дублировать    
            axes[0].set_ylabel('Частота')
        
    plt.tight_layout()
    return fig

def build_box_figure(df, cols):
    """
    Строит box plot для нескольких числовых столбцов.
    Каждый столбец получает свой отдельный подграфик со своей шкалой Y.
    """
    n = len(cols)
    fig, axes = plt.subplots(1, n)
    
    # Если выбран только один столбец, plt.subplots возвращает не список, а один ax
    if n == 1:
        axes = [axes]
    
    for ax, col in zip(axes, cols):
        data = df[col].dropna()
        
        # Рисуем box plot на своём подграфике. 
        # labels=[''] — чтобы не было подписи снизу (заголовок сверху достаточно)
        ax.boxplot(data, labels=[''], patch_artist=True,
                   boxprops=dict(facecolor='lightsteelblue', edgecolor='black'),
                   medianprops=dict(color='black', linewidth=1.5),
                   whiskerprops=dict(color='black'),
                   capprops=dict(color='black'),
                   flierprops=dict(marker='o', markerfacecolor='gray', markeredgecolor='none' ,markersize=4))
        
        ax.set_title(col, fontweight='bold')
        
        # Горизонтальная сетка
        ax.grid(axis='y', alpha=0.4, linestyle='--', color='gray')
    
    # Подпись оси Y только у первого подграфика
    axes[0].set_ylabel('Значение')
    
    plt.tight_layout()
    return fig

def build_bar_figure(df, cols):
    """Строит bar plot для нескольких категориальных/логических столбцов в ряд."""
    n = len(cols)
    fig, axes = plt.subplots(1, n,)
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        counts = df[col].value_counts()
        ax.bar(counts.index.astype(str), counts.values, edgecolor='none', color='coral')
        ax.set_title(col)
        ax.grid(axis='y', alpha=0.4, linestyle='--', color='gray')
        plt.sca(ax)
        plt.xticks(rotation=90, ha='right')
    axes[0].set_ylabel('Частота')
    plt.tight_layout()
    return fig

def build_scatter_figure(df, col1, col2, hue_col=None):
    """Строит scatter plot. Если hue_col задан — раскрашивает по категориям."""
    fig, ax = plt.subplots()
    if hue_col is None:
        ax.scatter(df[col1], df[col2], alpha=0.75, edgecolor='none', color='steelblue')
    else:
        categories = df[hue_col].dropna().unique()
        for cat in categories:
            mask = df[hue_col] == cat
            ax.scatter(df.loc[mask, col1], df.loc[mask, col2],
                       label=str(cat), alpha=0.75, edgecolor='none')
        ax.legend()
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    ax.set_title(f'{col1} vs {col2}')
    ax.grid(alpha=0.4, linestyle='--', color='gray')
    plt.tight_layout()
    return fig

def calculate_bins(data):
    """
    Вычисляет оптимальное число бинов по правилу Стерджеса.
    Если данных мало (< 2), возвращает 10 (дефолт matplotlib).
    """
    n = len(data.dropna())
    if n < 2:
        return 10
    # Правило Стерджеса: ceil(log2(n) + 1)
    bins = int(np.ceil(np.log2(n)) + 1)
    # Ограничиваем разумными пределами, чтобы график не стал "забором"
    return min(bins, 50)

def save_df_with_dtypes(df: pd.DataFrame, file_path: str):
    """Сохраняет DataFrame в CSV и его типы в соседний JSON файл."""
    # 1. Сохраняем сам CSV
    df.to_csv(file_path, index=False)
    
    # 2. Формируем путь для JSON (например, data.csv -> data.csv.dtypes.json)
    dtypes_path = file_path + ".dtypes.json"
    
    # 3. Собираем словарь типов (приводим к строке для JSON)
    dtypes_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # 4. Сохраняем JSON
    with open(dtypes_path, 'w', encoding='utf-8') as f:
        json.dump(dtypes_dict, f, ensure_ascii=False, indent=4)
        
    return dtypes_path

def load_csv_with_dtypes(file_path: str):
    """Загружает CSV и применяет типы из соседнего JSON, если он есть."""
    df = pd.read_csv(file_path)
    
    dtypes_path = file_path + ".dtypes.json"
    if os.path.exists(dtypes_path):
        try:
            with open(dtypes_path, 'r', encoding='utf-8') as f:
                dtypes_dict = json.load(f)
            
            # Применяем типы
            for col, dtype in dtypes_dict.items():
                if col in df.columns:
                    try:
                        # Обработка специфичных типов pandas
                        if dtype == 'category':
                            df[col] = df[col].astype('category')
                        elif dtype.startswith('datetime'):
                            df[col] = pd.to_datetime(df[col])
                        else:
                            df[col] = df[col].astype(dtype)
                    except Exception:
                        # Если не удалось привести (например, NaN в int), оставляем как есть
                        pass
        except Exception as e:
            print(f"Ошибка чтения типов: {e}")
            
    return df

def add_normal_curve_and_stats(ax, data, bins=cfg.BINS):
    """
    Добавляет на ось ax:
    - кривую нормального распределения (того же цвета, что и гистограмма)
    - вертикальную линию среднего арифметического (μ)
    - вертикальные линии μ±3σ
    Все линии подписаны.
    """
    if len(data) < 2:
        return  # недостаточно данных для статистики
    
    mu = data.mean()
    sigma = data.std()
    
    if sigma == 0:
        return  # все значения одинаковы, нет распределения
    
    # --- Среднее арифметическое (μ) ---
    ax.axvline(mu, color='black', linestyle='--', linewidth=1.5, label=f'μ = {mu:.2f}')
    # Подпись μ сверху
    y_top = ax.get_ylim()[1]
    ax.text(mu, y_top * 0.97, f'μ = {mu:.2f}', 
            color='black', fontsize=10,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', alpha=0.8))
    
    # --- 3 сигмы (μ-3σ и μ+3σ) ---
    lower = mu - 3 * sigma
    upper = mu + 3 * sigma
    
    ax.axvline(lower, color='gray', linestyle='-.', linewidth=1, label=f'μ-3σ = {lower:.2f}')
    ax.axvline(upper, color='gray', linestyle='-.', linewidth=1, label=f'μ+3σ = {upper:.2f}')
    
    # --- Кривая нормального распределения ---
    # Создаём массив X от мин до макс значения
    x_min, x_max = ax.get_xlim()
    x = np.linspace(x_min, x_max, 200)
    # Формула PDF нормального распределения (без scipy)
    pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    # Масштабируем PDF под частоты гистограммы: N * bin_width
    bin_width = (data.max() - data.min()) / bins
    pdf_scaled = pdf * len(data) * bin_width
    # Рисуем кривую того же цвета, что и гистограмма, но потолще
    ax.plot(x, pdf_scaled, color='black', linewidth=1.5, label='Нормальное распределение')
    
    # Подписи 3σ чуть ниже, чтобы не перекрывались с μ
    y_mid = y_top * 0.85
    ax.text(lower, y_mid, f'μ-3σ = {lower:.2f}', color='gray', fontsize=9,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))
    ax.text(upper, y_mid, f'μ+3σ = {upper:.2f}', color='gray', fontsize=9,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))