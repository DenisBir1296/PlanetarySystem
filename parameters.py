import scipy.constants
import math

# основное окно
DEF_SIZE = (1200, 800)
MIN_SIZE = (1000, 650)
PROGRAM_TITLE = "Математическое моделирование"
PARAMETERS_ERROR = 'Ошибка в параметрах.'
PLANET_PARAMETER_WARNING = 'Ошибка в данных планет.'
NEXT_STEP_WARNING = 'Шаг обновления должен быть больше шага сетки.'

# параметры
parameters = {'g': {'name': 'Гравитационная постоянная:', 'type': 'textctrl', 'value': str(scipy.constants.G)},
              'step': {'name': 'Шаг сетки:', 'type': 'textctrl', 'value': '3600'},
              'time': {'name': 'Время расчета:', 'type': 'textctrl', 'value': str(60 * 60 * 24 * 364*10)},
              'bal mass': {'name': 'Установка центра массы\n в начало координат:', 'type': 'checkbox', 'value': False},
              'bal impl': {'name': 'Обнуления суммарного\n импульса системы:', 'type': 'checkbox', 'value': False}}

RESISTANS_DEFAULT_VALUE = 0.000000001

SUN_MASS = 1.98892E30
EARTH_MASS = 5.972E24
EARTH_X_POS = 149597871000.
EARTH_Y_VEL = math.sqrt(scipy.constants.G * SUN_MASS / EARTH_X_POS)

# столбцы в табличках
table_headers_name = {'m': 'Масса',
              'x pos': 'x',
              'y pos': 'y',
              'x vel': 'Скорость x',
              'y vel': 'Скорость y',
              'res': 'Сопротивление'}
WIGHT = 150

# названия кнопок
buttons_name = {'add row': 'Добавить планету',
                'del row': 'Удалить планету',
                'reset': 'Сбросить',
                'calculate': 'Расчет'}

# графики
X_NAME = 'x'
Y_NAME = 'y'

FONT_SIZE = 16
DIALOG_DEFAULT_SIZE = (1500, 800)
DIALOG_MIN_SIZE = (1100, 400)
