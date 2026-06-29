import flet as ft

# ==========================================
# 1. НАСТРОЙКИ ПРИЛОЖЕНИЯ И СТРАНИЦЫ
# ==========================================
APP_TITLE = "Анализ рынка недвижимости №13"
PAGE_PADDING = 0
THEME_MODE = ft.ThemeMode.LIGHT

# ==========================================
# 2. РАБОТА С ДАННЫМИ И ФАЙЛАМИ
# ==========================================
CSV_DIALOG_TITLE = "Выберите файл с данными"
CSV_EXTENSIONS = ["csv"]

# ==========================================
# 4. РАЗМЕРЫ, ОТСТУПЫ И ГРАНИЦЫ СЛОТОВ (LAYOUT)
# ==========================================
# Загрузочный экран
LOAD_SCREEN_PADDING = 30

# Тулбар
TOOLBAR_PADDING = ft.Padding(10, 10, 10, 10)
TOOLBAR_BGCOLOR = ft.Colors.PRIMARY_CONTAINER
TOOLBAR_ELEMENTS_SPACING = 10

SLIDER_PADDING = ft.Padding(0, 10, 0, 10)

# Слоты параметров и вывода
PARAMETERS_SLOT_HEIGHT = 360
PARAMETERS_SLOT_WIDTH = 450
OUTPUT_SLOT_HEIGHT = 360
OUTPUT_SLOT_WIDTH = 640

SLOT_BORDER_WIDTH = 1
SLOT_BORDER_COLOR = ft.Colors.OUTLINE
SLOT_PADDING = 10

# Рабочая зона и главный экран
WORKSPACE_PADDING = ft.Padding(10, 0, 10, 10)
MAIN_SCREEN_PADDING = 0

# ==========================================
# 3. ПАРАМЕТРЫ GUI. ТАБЛИЦА
# ==========================================
HEADER_HEIGHT = 30
CELL_HEIGHT = 24
MAX_VISIBLE_ROWS = 15
TABLE_HEIGHT = CELL_HEIGHT * MAX_VISIBLE_ROWS + HEADER_HEIGHT

TABLE_HEADER_BG_COLOR = ft.Colors.SURFACE_CONTAINER_HIGHEST
TABLE_OUTER_BORDERS_WIDTH = SLOT_BORDER_WIDTH
TABLE_INNER_VERTICAL_BORDERS_WIDTH = 1
TABLE_INNER_HORIZONTAL_BORDERS_WIDTH = 1
TABLE_BORDER_COLOR = SLOT_BORDER_COLOR

# ==========================================
# 5. ЦВЕТА И ШРИФТЫ (СТИЛИ)
# ==========================================
COLOR_ERROR = ft.Colors.ERROR
COLOR_OUTLINE_BUTTON_BG = ft.Colors.PRIMARY_CONTAINER
COLOR_OUTLINE_BUTTON = ft.Colors.ON_SURFACE
COLOR_SELECTED_OUTLINE_BUTTON_BG = ft.Colors.SECONDARY
COLOR_SELECTED_OUTLINE_BUTTON = ft.Colors.ON_SECONDARY

FONT_MONOSPACE = 'Consolas'

# Размеры шрифтов
LOAD_TITLE_SIZE = 28
LOG_TEXT_SIZE = 12

# ==========================================
# 6. ТЕКСТЫ И НАДПИСИ (UI TEXTS)
# ==========================================
# --- Загрузочный экран ---
TXT_LOAD_TITLE = "Данные для анализа"
TXT_LOAD_DESC_DEFAULT = "Откройте CSV-файл, чтобы приступить к работе с данными."
TXT_LOAD_DESC_ERROR_PREFIX = "Ошибка чтения CSV: "
TXT_LOAD_BUTTON = "Выбрать файл"

# --- Тулбар (Тултипы) ---
TIP_OPEN_CSV = "Открыть CSV"
TIP_SAVE_CSV_WITH_TYPES = "Сохранить датасет и типы"
TIP_REVERT = "Сбросить изменения"
TIP_ADD_COL = "Добавить/изменить поле"
TIP_DEL_COL = "Удалить столбец"
TIP_INFO = "Информация о датасете"
TIP_STATS = "Показать/скрыть статистику"
TIP_DEL_DUP = "Удалить дубликаты"

# --- Слайдер (Тултипы) ---
TIP_TO_BEGIN = "В начало"
TIP_BACKWARD = "Назад"
TIP_FORWARD = "Вперёд"
TIP_TO_END = "В конец"

# --- Параметры и поля ввода ---
LBL_COLUMN_DROPDOWN = "Столбец"
TIP_DELETE_FIELD = "Удалить поле"

LBL_COL_NAME = "Имя поля"
HINT_COL_NAME = "new_field"

LBL_COL_TYPE = "Тип поля"

LBL_COL_VALUE = "Значение/выражение"
HINT_COL_VALUE = "1, 'str_example', df['price']/df['totsp']"

TXT_SUBMIT_ADD_COL = "Добавить/изменить"
TXT_PARAMETERS_DEFAULT = "Параметры"


COLUMN_TYPES = {
    "int64": "integer",
    "float64": "float",
    "string": "string",
    "category": "category",
    "bool": "boolean"
}

# --- Графики ---
TIP_CHARTS = "Построить график"
LBL_CHART_TYPE = "Тип графика"
CHART_TYPES = {
    "hist": "Гистограмма",
    "box": "Ящик с усами",
    "bar": "Столбчатая",
    "scatter": "Точечная"
}
LBL_STACKED_HIST = "C накоплением"
LBL_SELECT_COLUMN = "Столбец"
LBL_SELECT_COLUMNS = "Выберите столбцы"
LBL_SCATTER_X = "Ось X"
LBL_SCATTER_Y = "Ось Y"
LBL_CATEGORY_VAR = "Группировка по категории (необязательно)"
TXT_BUILD_CHART = "Построить"
TXT_NO_NUMERIC_COLS = "В датасете нет числовых столбцов"
TXT_NO_CATEGORICAL_COLS = "В датасете нет категориальных столбцов"
TXT_SELECT_AT_LEAST_ONE = "Выберите хотя бы один столбец"
TXT_SELECT_TWO_COLS = "Выберите ровно два столбца"

BINS = 20

# Размеры слота графиков
CHART_SLOT_HEIGHT = 720
CHART_SLOT_WIDTH = 1280
CHART_SLOT_BORDER_WIDTH = SLOT_BORDER_WIDTH
CHART_SLOT_BORDER_COLOR = SLOT_BORDER_COLOR
CHART_SLOT_PADDING = 0

HIST_BINS_EDGECOLOR = 'white'
HIST_BINS_COLOR = 'steelblue'