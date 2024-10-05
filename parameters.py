import scipy.constants
import math

#основное окно
DEF_SIZE = (1200,800)
MIN_SIZE = (900, 650)
PROGRAM_TITLE = "Математическое моделирование"
PARAMETERS_ERROR = 'Ошибка в параметрах.'
PLANET_PARAMETER_WARNING = 'Ошибка в данных планет.'
NEXT_STEP_WARNING = 'Шаг обновления должен быть больше шага сетки.'

# параметры настройки
G_NAME = 'Гравитационная постоянная:'
STEP_NAME = 'Шаг сетки:'
STEP_NEXT_NAME = 'Шаг обновления:'
TIME_NAME = 'Время расчета:'
BAL_MASS_NAME = 'Установка центра массы\n в начало координат:'
BAL_IMPL_NAME = 'Обнуления суммарного\n импульса системы:'

# значения параметров по умолчанию
G_DEF_VAL = str(scipy.constants.G)
STEP_DEF_VAL = '3600'
STEP_NEXT_VAL = str(3600*100)
TIME_DEF_VAL = str(60*60*24*364)

SUN_MASS = 1.98892E30
EARTH_MASS = 5.972E24
EARTH_X_POS = 149597871000.
EARTH_Y_VEL = math.sqrt(scipy.constants.G * SUN_MASS / EARTH_X_POS)

# столбцы в табличках
WIGHT = 150
MASS_NAME = 'Масса'
X_POS_NAME = 'x'
Y_POS_NAME = 'y'
X_VEL_NAME = 'Скорость x'
Y_VEL_NAME = 'Скорость y'

# названия кнопок
ADD_ROW_NAME = 'Добавить планету'
DEL_ROW_NAME = 'Удалить планету'
RESET_NAME = 'Сбросить'
ANI_NAME = 'Анимирование'
TRAJ_NAME = 'Траектории'

#графики
X_NAME = 'x'
Y_NAME = 'y'
RAD_NAME = 'Радиус'
ALP_NAME = 'Угол, гр.'
TIME_NAME = 'Время'

#диалоговые окна
FONT_SIZE = 16
DIALOG_DEFAULT_SIZE = (1000, 800)
DIALOG_MIN_SIZE = (600, 400)
TRAJ_TITLE_NAME = 'Траектории движения'
ANIMATION_WINDOW_NAME = 'Анимация'
TRAJECTORY_WINDOW_NAME = 'Траектории движения планет'
