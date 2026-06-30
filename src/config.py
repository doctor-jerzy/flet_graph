import flet as ft
import matplotlib as mpl

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
TOOLBAR_ICON_SIZE = 24
TOOLBAR_DIVIDER_COLOR = ft.Colors.OUTLINE_VARIANT
TOOLBAR_BGCOLOR = ft.Colors.SURFACE_CONTAINER_LOW
TOOLBAR_ELEMENTS_SPACING = 10

SLIDER_PADDING = ft.Padding(0, 10, 0, 10)

# Слоты параметров и вывода
PARAMETERS_SLOT_HEIGHT = 360
PARAMETERS_SLOT_WIDTH = 400
OUTPUT_SLOT_HEIGHT = 360
OUTPUT_SLOT_WIDTH = None

SLOT_BORDER_WIDTH = 1
SLOT_BORDER_COLOR = ft.Colors.OUTLINE_VARIANT
SLOT_PADDING = 10
SLOT_TITLE_TEXT_SIZE = 16

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
LOG_TEXT_SIZE = 14

COLOR_HOVER_BG = ft.Colors.SURFACE_CONTAINER_HIGHEST

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
TIP_SAVE_STATE = "Сохранить состояние"
TIP_SAVE_CSV_WITH_TYPES = "Сохранить датасет и типы полей"
TIP_REVERT = "Сбросить изменения"
TIP_ADD_COL = "Добавить/изменить поле"
TIP_DEL_COL = "Удалить поле"
TIP_DEL_DUP = "Удалить дубликаты"
TIP_OUTLIERS = "Работа с выбросами"
TIP_INFO = "Информация о датасете"
TIP_STATS = "Показать/скрыть статистику"
TIP_CHARTS = "Построить график"

# --- Слайдер (Тултипы) ---
TIP_TO_BEGIN = "В начало"
TIP_BACKWARD = "Назад"
TIP_FORWARD = "Вперёд"
TIP_TO_END = "В конец"

# --- Параметры и поля ввода ---
LBL_DEL_COL_DROPDOWN = "Столбец"
TIP_DELETE_FIELD = "Удалить поле"

LBL_COL_NAME_INPUT = "Имя поля"
HINT_COL_NAME_INPUT = "new_field"

LBL_COL_TYPE_DROPDOWN = "Тип поля"

LBL_COL_VALUE_INPUT = "Значение/выражение"
HINT_COL_VALUE_INPUT = "1, 'str_example', df['price']/df['totsp']"

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

LBL_CHART_TYPE_DROPDOWN = "Тип графика"
CHART_TYPES = {
    "hist": "Гистограмма",
    "box": "Ящик с усами",
    "bar": "Столбчатая",
    "scatter": "Точечная"
}
LBL_STACKED_HIST = "C накоплением"
LBL_SELECT_COLUMN_DROPDOWN = "Столбец"
LBL_SELECT_COLUMNS = "Выберите столбцы"
LBL_SCATTER_X_DROPDOWN = "Ось X"
LBL_SCATTER_Y_DROPDOWN = "Ось Y"
LBL_CATEGORY_COL_DROPDOWN = "Группировка по категории (необязательно)"
TXT_BUILD_CHART = "Построить"
TXT_NO_NUMERIC_COLS = "В датасете нет числовых столбцов"
TXT_NO_CATEGORICAL_COLS = "В датасете нет категориальных столбцов"
TXT_SELECT_AT_LEAST_ONE = "Выберите хотя бы один столбец"
TXT_SELECT_TWO_COLS = "Выберите ровно два столбца"

# Размеры слота графиков
CHART_SLOT_HEIGHT = 720
CHART_SLOT_WIDTH = 1280
CHART_SLOT_BORDER_WIDTH = SLOT_BORDER_WIDTH
CHART_SLOT_BORDER_COLOR = SLOT_BORDER_COLOR
CHART_SLOT_PADDING = 0

# В раздел 6. ТЕКСТЫ И НАДПИСИ (UI TEXTS) добавь:

TXT_FIND_OUTLIERS = "Найти выбросы "
TXT_REMOVE_OUTLIERS = "Удалить выбросы "
TXT_SELECT_COLS_FOR_OUTLIERS = "Выберите числовые столбцы (Z-оценка): "
TXT_NO_OUTLIER_COL = "Сначала нажмите 'Определить выбросы' "
TXT_OUTLIER_WARNING = "ВНИМАНИЕ: удаление строк меняет статистику датасета. При повторном поиске границы выбросов могут измениться."

# Имя служебной колонки (лучше вынести, чтобы не хардкодить в коде)
OUTLIER_COL_NAME = "is_outlier" 

# ==========================================
# 6. ПАРАМЕТРЫ ОФОРМЛЕНИЯ ДИАГРАММ
# ==========================================
# 0. ОБЩИЕ
GRID_APLPHA = 0.25
GRID_COLOR = 'black'
GRID_LINESTYLE = '--'
LEGEND_LOC = 'upper right'
ADJUST_WSPACE = 0.1
ADJUST_COEF = 0.05
ADJUST_COEF_WHERE_LABELS = ADJUST_COEF * 1.5

COLORMAP = mpl.colormaps['tab10']

# 1. ГИСТОГРАММЫ
BINS = 20 # количество бинов (интервалов)
HIST_BINS_EDGECOLOR = 'white' # цвет контура бинов
HIST_BINS_COLOR = COLORMAP.colors[0] # цвет бинов
HIST_Y_LABEL = "Частота" # подпись оси Y
HIST_TITLE = "{num_col}"
HIST_HUE_TITLE = "{num_col} по {hue_col}"
HIST_STACKED_HUE_TITLE = "{num_col} по {hue_col}"
HIST_GRID_AXIS = 'y'

NORM_LINE_COLOR = 'black'
NORM_LINE_LINESTYLE = '-'
NORM_LINE_LINEWIDTH = 1.5

MEAN_LINE_COLOR = 'black'
MEAN_LINE_LINESTYLE = '--'
MEAN_LINE_LINEWIDTH = 1.25

MEAN_LINE_TEXT = "μ = {:.2f}"
MEAN_LINE_TEXT_HEIGHT_COEF = 0.95
MEAN_LINE_TEXT_COLOR = 'black'
MEAN_LINE_TEXT_FONTSIZE = 11
MEAN_LINE_TEXT_HA = 'center'
MEAN_LINE_TEXT_VA = 'top'
MEAN_LINE_TEXT_BBOX_STYLE = 'round,pad=0.3'
MEAN_LINE_TEXT_BBOX_FACECOLOR = 'white'
MEAN_LINE_TEXT_BBOX_EDGECOLOR = MEAN_LINE_TEXT_COLOR
MEAN_LINE_TEXT_BBOX_ALPHA = 0.75

SIGMA_LINE_COLOR = MEAN_LINE_COLOR
SIGMA_LINE_LINESTYLE = '-.'
SIGMA_LINE_LINEWIDTH = MEAN_LINE_LINEWIDTH / 1

SIGMA_LOWER_LINE_TEXT = "μ-3σ = {:.2f}"
SIGMA_UPPER_LINE_TEXT = "μ+3σ = {:.2f}"
SIGMA_LINE_TEXT_HEIGHT_COEF = MEAN_LINE_TEXT_HEIGHT_COEF * 0.80
SIGMA_LINE_TEXT_COLOR = MEAN_LINE_TEXT_COLOR
SIGMA_LINE_TEXT_FONTSIZE = 10
SIGMA_LINE_TEXT_HA = MEAN_LINE_TEXT_HA
SIGMA_LINE_TEXT_VA = MEAN_LINE_TEXT_VA
SIGMA_LINE_TEXT_BBOX_STYLE = MEAN_LINE_TEXT_BBOX_STYLE
SIGMA_LINE_TEXT_BBOX_FACECOLOR = MEAN_LINE_TEXT_BBOX_FACECOLOR
SIGMA_LINE_TEXT_BBOX_EDGECOLOR = MEAN_LINE_TEXT_COLOR
SIGMA_LINE_TEXT_BBOX_ALPHA = MEAN_LINE_TEXT_BBOX_ALPHA/75*50

# 2. ЯЩИК С УСАМИ
BOX_GRID_AXIS = 'y'
BOX_Y_LABEL = "Значение" # подпись оси Y

# 3. ТОЧЕЧНАЯ
SCATTER_ALPHA = 1
SCATTER_SIZE = 30