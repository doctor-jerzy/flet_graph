# data.py
import pandas as pd
from dataclasses import dataclass

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


