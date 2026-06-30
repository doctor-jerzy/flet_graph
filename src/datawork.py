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
from scipy.optimize import curve_fit
from scipy import stats
from scipy.stats import zscore

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

def build_hist_figure(df, col, hue_col=None, stacked=False):
    """
    Строит гистограмму.
    Если hue_col не задан — одна гистограмма.
    Если hue_col задан и stacked=False — гистограммы в ряд (subplots).
    Если hue_col задан и stacked=True — гистограмма с накоплением.
    """
    if hue_col is None:
        # --- Одиночная гистограмма ---
        data = df[col].dropna().values
        
        fig, ax = plt.subplots()
        ax.hist(data, bins=cfg.BINS, edgecolor=cfg.HIST_BINS_EDGECOLOR, color=cfg.HIST_BINS_COLOR)
        add_normal_curve_and_stats(ax, data, bins=cfg.BINS)
        ax.set_xlabel(col)
        ax.set_ylabel(cfg.HIST_Y_LABEL)
        ax.set_title(cfg.HIST_TITLE.format(num_col=col), fontweight='bold')
        # Горизонтальная сетка
        ax.grid(axis=cfg.HIST_GRID_AXIS, alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)
        
    else:
        # --- Гистограммы в ряд по категориям ---
        categories = sorted(df[hue_col].dropna().unique())
        n = len(categories)
        colors = cfg.COLORMAP(np.linspace(0, 1, n))
        
        if stacked:
            # --- Гистограмма с накоплением ---
            data_list = [df[df[hue_col] == cat][col].dropna().values for cat in categories]
            
            fig, ax = plt.subplots()
            ax.hist(
                data_list,
                bins=cfg.BINS,
                stacked=True,
                color=colors,
                edgecolor=cfg.HIST_BINS_EDGECOLOR,
                label=categories
            )
            ax.set_xlabel(col)
            ax.set_ylabel(cfg.HIST_Y_LABEL)
            ax.set_title(cfg.HIST_STACKED_HUE_TITLE.format(num_col=col, hue_col=hue_col), fontweight='bold')
            ax.legend(title=hue_col, loc=cfg.LEGEND_LOC)
            ax.grid(axis=cfg.HIST_GRID_AXIS, alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)
        
        else:
            # --- Гистограммы в ряд (subplots) ---
            # N подграфиков в один ряд. sharey=True — одинаковая шкала Y для сравнения.
            fig, axes = plt.subplots(1, n, sharey=True, gridspec_kw={'wspace': 0.05})
            if n == 1:
                axes = [axes]  # чтобы можно было итерироваться
            for ax, cat, color in zip(axes, categories, colors):
                data = df[df[hue_col] == cat][col].dropna().values
                ax.hist(data, bins=cfg.BINS, color=color, edgecolor=cfg.HIST_BINS_EDGECOLOR)
                add_normal_curve_and_stats(ax, data, bins=cfg.BINS)
                ax.set_xlabel(col)
                ax.set_title(cat)
                ax.grid(axis=cfg.HIST_GRID_AXIS, alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)

            # Подпись оси Y только у первого, чтобы не дублировать    
            fig.suptitle(cfg.HIST_HUE_TITLE.format(num_col=col, hue_col=hue_col), fontweight='bold')
            axes[0].set_ylabel(cfg.HIST_Y_LABEL)
            
    plt.subplots_adjust(
        wspace=cfg.ADJUST_WSPACE,
        left=cfg.ADJUST_COEF_WHERE_LABELS,
        right=1-cfg.ADJUST_COEF,
        bottom=cfg.ADJUST_COEF_WHERE_LABELS
    )    
    # plt.tight_layout()
    return fig

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
    ax.axvline(
        mu,
        color=cfg.MEAN_LINE_COLOR,
        linestyle=cfg.MEAN_LINE_LINESTYLE,
        linewidth=cfg.MEAN_LINE_LINEWIDTH
    )
    # Подпись μ сверху
    y_top = ax.get_ylim()[1]
    ax.text(mu,
            y_top * cfg.MEAN_LINE_TEXT_HEIGHT_COEF,
            cfg.MEAN_LINE_TEXT.format(mu), 
            color=cfg.MEAN_LINE_TEXT_COLOR,
            fontsize=cfg.MEAN_LINE_TEXT_FONTSIZE,
            ha=cfg.MEAN_LINE_TEXT_HA,
            va=cfg.MEAN_LINE_TEXT_VA,
            bbox=dict(
                boxstyle=cfg.MEAN_LINE_TEXT_BBOX_STYLE,
                facecolor=cfg.MEAN_LINE_TEXT_BBOX_FACECOLOR,
                edgecolor=cfg.MEAN_LINE_TEXT_BBOX_EDGECOLOR,
                alpha=cfg.MEAN_LINE_TEXT_BBOX_ALPHA
            )
    )
    
    # --- 3 сигмы (μ-3σ и μ+3σ) ---
    lower = mu - 3 * sigma
    upper = mu + 3 * sigma
    
    # Подписи 3σ чуть ниже, чтобы не перекрывались с μ
    if (data < 0).any():
        ax.axvline(
            lower,
            color=cfg.SIGMA_LINE_COLOR,
            linestyle=cfg.SIGMA_LINE_LINESTYLE,
            linewidth=cfg.SIGMA_LINE_LINEWIDTH
        )
        ax.text(
            lower,
            y_top * cfg.SIGMA_LINE_TEXT_HEIGHT_COEF,
            cfg.SIGMA_LOWER_LINE_TEXT.format(lower),
            color=cfg.SIGMA_LINE_TEXT_COLOR,
            fontsize=cfg.SIGMA_LINE_TEXT_FONTSIZE,
            ha=cfg.SIGMA_LINE_TEXT_HA, va=cfg.SIGMA_LINE_TEXT_VA,
            bbox=dict(
                boxstyle=cfg.SIGMA_LINE_TEXT_BBOX_STYLE,
                facecolor=cfg.SIGMA_LINE_TEXT_BBOX_FACECOLOR,
                edgecolor=cfg.SIGMA_LINE_TEXT_BBOX_EDGECOLOR,
                alpha=cfg.SIGMA_LINE_TEXT_BBOX_ALPHA
            )
        )
    ax.axvline(
        upper,
        color=cfg.SIGMA_LINE_COLOR,
        linestyle=cfg.SIGMA_LINE_LINESTYLE,
        linewidth=cfg.SIGMA_LINE_LINEWIDTH
    )
    ax.text(
        upper,
        y_top * cfg.SIGMA_LINE_TEXT_HEIGHT_COEF,
        cfg.SIGMA_UPPER_LINE_TEXT.format(upper),
        color=cfg.SIGMA_LINE_TEXT_COLOR,
        fontsize=cfg.SIGMA_LINE_TEXT_FONTSIZE,
        ha=cfg.SIGMA_LINE_TEXT_HA, va=cfg.SIGMA_LINE_TEXT_VA,
        bbox=dict(
            boxstyle=cfg.SIGMA_LINE_TEXT_BBOX_STYLE,
            facecolor=cfg.SIGMA_LINE_TEXT_BBOX_FACECOLOR,
            edgecolor=cfg.SIGMA_LINE_TEXT_BBOX_EDGECOLOR,
            alpha=cfg.SIGMA_LINE_TEXT_BBOX_ALPHA
        )
    )
    # --- Кривая нормального распределения ---
    # Создаём массив X от мин до макс значения
    x_min, x_max = ax.get_xlim()
    x = np.linspace(x_min, x_max, 100)
    # pdf возвращает плотность вероятности. 
    # Умножаем на N * bin_width, чтобы перевести в "частоты" гистограммы
    bin_width = (data.max() - data.min()) / bins
    y = stats.norm.pdf(x, mu, sigma) * len(data) * bin_width
    # Рисуем кривую
    ax.plot(x, y,
            color=cfg.NORM_LINE_COLOR,
            linestyle=cfg.NORM_LINE_LINESTYLE,
            linewidth=cfg.NORM_LINE_LINEWIDTH
    )

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
        data = df[col].dropna().values
        
        # Рисуем box plot на своём подграфике. 
        # labels=[''] — чтобы не было подписи снизу (заголовок сверху достаточно)
        ax.boxplot(data, labels=[''], patch_artist=True,
                   boxprops=dict(facecolor='lightsteelblue', edgecolor='black'),
                   medianprops=dict(color='black', linewidth=1.5),
                   whiskerprops=dict(color='black'),
                   capprops=dict(color='black'),
                   flierprops=dict(marker='o', markerfacecolor='gray', markeredgecolor='none', markersize=4))
        
        ax.set_title(col, fontweight='bold')
        
        # Горизонтальная сетка
        ax.grid(axis=cfg.BOX_GRID_AXIS, alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)
    
    # Подпись оси Y только у первого подграфика
    axes[0].set_ylabel(cfg.BOX_Y_LABEL)
    
    plt.tight_layout()
    return fig

def build_bar_figure(df, cols):
    """Строит bar plot для нескольких категориальных/логических столбцов в ряд."""
    n = len(cols)
    colors = cfg.COLORMAP(np.linspace(0, 1, n))
    fig, axes = plt.subplots(1, n,)
    if n == 1:
        axes = [axes]
    for ax, col, color in zip(axes, cols, colors):
        counts = df[col].value_counts()
        ax.bar(counts.index.astype(str), counts.values, edgecolor='none', color=color)
        ax.set_title(col)
        ax.grid(axis='y', alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)
        plt.sca(ax)
        plt.xticks(rotation=90, ha='right')
    axes[0].set_ylabel('Частота')
    plt.tight_layout()
    plt.subplots_adjust(
        wspace=cfg.ADJUST_WSPACE*2,
        left=cfg.ADJUST_COEF_WHERE_LABELS,
        right=1-cfg.ADJUST_COEF
    )    
    return fig

def add_trend_line(ax, x_data, y_data, color='blue', label=None, linewidth=2):
    """
    Добавляет линию тренда (линейную регрессию) на scatter plot.
    Использует scipy.optimize.curve_fit для подбора параметров.
    
    Parameters:
    - ax: matplotlib axis
    - x_data: pd.Series или массив данных для оси X
    - y_data: pd.Series или массив данных для оси Y
    - color: цвет линии тренда
    - label: подпись для легенды (по умолчанию "y = mx + b")
    - linewidth: толщина линии
    """
    
    # Удаляем NaN значения
    mask = ~(x_data.isna() | y_data.isna())
    X = x_data[mask].values
    Y = y_data[mask].values
    
    if len(X) < 2:
        return  # Недостаточно данных для регрессии
    
    # Проверка на нулевую дисперсию
    if np.std(X) == 0 or np.std(Y) == 0:
        return  # Нет вариации в данных
    
    # Функция линейной регрессии: y = m*x + b
    def linear_func(x, m, b):
        return m * x + b
    
    try:
        # Подбираем параметры регрессии (m - наклон, b - пересечение)
        popt, _ = curve_fit(linear_func, X, Y)
        m, b = popt
        
        # Создаём точки для линии тренда (от мин до макс X)
        x_line = np.linspace(X.min(), X.max(), 100)
        y_line = linear_func(x_line, m, b)
        
        # Формируем подпись, если не задана
        if label is None:
            label = f'y = {m:.2f}x + {b:.2f}'
        
        # Рисуем линию тренда (пунктирная, того же цвета, что и точки)
        ax.plot(x_line, y_line, color=color, linestyle='--', 
                linewidth=linewidth, label=label, alpha=1)
        
    except Exception as e:
        # Если не удалось подобрать регрессию (например, данные вырождены)
        pass

def build_scatter_figure(df, col1, col2, hue_col=None):
    """
    Строит scatter plot.
    Если hue_col не задан — обычный scatter с линией тренда.
    Если hue_col задан — scatter с раскраской по категориям, 
    для каждой категории своя линия тренда.
    """
    fig, ax = plt.subplots()
    
    if hue_col is None:
        # --- Обычный scatter plot ---
        X = df[col1].dropna()
        Y = df[col2].dropna()
        
        # Синхронизируем индексы, чтобы точки соответствовали друг другу
        mask = df[col1].notna() & df[col2].notna()
        X = df.loc[mask, col1]
        Y = df.loc[mask, col2]
        
        ax.scatter(X, Y, alpha=cfg.SCATTER_ALPHA, edgecolor='none', color='steelblue', s=cfg.SCATTER_SIZE)
        
        # Добавляем линию тренда
        add_trend_line(ax, X, Y, color='steelblue', linewidth=1.5)
        
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f'{col1} vs {col2}', fontweight='bold')
        ax.legend(loc=cfg.LEGEND_LOC)
        
    else:
        # --- Scatter plot с группировкой по категориям ---
        categories = sorted(df[hue_col].dropna().unique())
        
        # Используем цветовую палитру matplotlib
        colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
        
        for idx, cat in enumerate(categories):
            mask = df[hue_col] == cat
            X = df.loc[mask, col1]
            Y = df.loc[mask, col2]
            
            # Удаляем NaN
            valid_mask = X.notna() & Y.notna()
            X = X[valid_mask]
            Y = Y[valid_mask]
            
            if len(X) < 2:
                continue  # Пропускаем категории с недостаточным количеством данных
            
            color = colors[idx]
            ax.scatter(X, Y, alpha=cfg.SCATTER_ALPHA, edgecolor='none', color=color, s=cfg.SCATTER_SIZE, label=f'{hue_col} = {cat}')
            
            # Добавляем линию тренда для каждой категории (того же цвета)
            add_trend_line(ax, X, Y, color=color, label=None, linewidth=1.5)
        
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f'{col1} vs {col2} (по {hue_col})', fontweight='bold')
        ax.legend(loc=cfg.LEGEND_LOC, fontsize=8)
    
    # Сетка
    ax.grid(axis='both', alpha=cfg.GRID_APLPHA, linestyle=cfg.GRID_LINESTYLE, color=cfg.GRID_COLOR)
    plt.tight_layout()
    plt.subplots_adjust(
        left=cfg.ADJUST_COEF_WHERE_LABELS,
        right=1-cfg.ADJUST_COEF,
        bottom=cfg.ADJUST_COEF_WHERE_LABELS
    )  
    return fig


def mark_outliers_zscore(df, cols, threshold=3):
    """
    Создает/обновляет логический столбец с выбросами на основе Z-оценки.
    Возвращает: (новый_df, успех: bool, сообщение: str)
    """
    if not cols:
        return df, False, "Не выбраны столбцы для анализа."
    
    try:
        # Считаем абсолютные Z-оценки. nan_policy='omit' игнорирует NaN в данных.
        z_scores = np.abs(df[cols].apply(zscore, nan_policy='omit'))
        
        # Если в столбце нет вариации (все числа равны), zscore вернет NaN. 
        # Заменяем NaN на 0 (это не выброс).
        z_scores = z_scores.fillna(0.0)
        
        # Маска: True, если ХОТЯ БЫ в одном столбце Z > threshold
        mask = (z_scores > threshold).any(axis=1)
        
        df_out = df.copy()
        df_out[cfg.OUTLIER_COL_NAME] = mask
        
        outliers_count = mask.sum()
        return df_out, True, f"Столбец выбросов '{cfg.OUTLIER_COL_NAME}' по столбцам {cols} создан.\nНайдено выбросов: {outliers_count}."
    except Exception as e:
        return df, False, f"Ошибка расчета Z-оценок: {e}"

def remove_outliers_by_col(df, outlier_col_name):
    """
    Удаляет строки, помеченные как выбросы, и удаляет сам столбец-маску.
    Возвращает: (новый_df, успех: bool, сообщение: str)
    """
    if outlier_col_name not in df.columns:
        return df, False, "Столбец с маской выбросов не найден."
    
    initial_count = len(df)
    # Оставляем только те строки, где is_outlier == False
    df_clean = df[df[outlier_col_name] == False].copy()
    df_clean = df_clean.drop(columns=[outlier_col_name]).reset_index(drop=True)
    
    removed_count = initial_count - len(df_clean)
    return df_clean, True, f"Удалено строк-выбросов: {removed_count}. Служебный столбец удален."