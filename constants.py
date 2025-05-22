"""Можете аккуратно поэкспериментировать с параметрами роботов
но тогда необходимо будет и исправить некоторые параметры в classes.py
а именно констаты погрешности в классе Robot в методах
drive_to_target на 234 и 250 строках
rotate_to_target на 281 и 296 строках"""
BASE_HEIGHT = 30 #cm
BASE_LENGTH = 70 #cm
BASE_MASS = 2 #kg

MAIN_WHEEL_RADIUS = 10 #cm
MAIN_WHEEL_WIDTH = 3 #cm
MAIN_WHEEL_OFFSET = 10 #cm
MAIN_WHEEL_MASS = 0.05 #kg

SUPPORT_WHEEL_RADIUS = 6 #cm
SUPPROT_WHEEL_WIDTH = 1 #cm
SUPPORT_WHEEL_OFFSET = 7 #cm
SUPPORT_WHEEL_DISTANCE = 5 #cm 
SUPPORT_WHEEL_MASS = 0.03 #kg

MOTOR_POWER = 90 #wt
NOMINAL_SPEED = 3000 #count/min
MOTOR_MASS = 1 #kg
ROTOR_MOMENTUM = 0.0005
REDUCTOR_VALUE = 30

TICKS = 120
