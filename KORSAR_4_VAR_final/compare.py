import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 1. Читаем данные из KORSAR
try:
    df_korsar = pd.read_csv("result.dat", sep=r'\s+', skiprows=2, 
                            names=['Time', 'REV', 'QT', 'DP'], engine='python')
except FileNotFoundError:
    print("ОШИБКА: Файл result.dat не найден!")
    exit()

# Берем данные только после отключения (на 20-й секунде)
df_korsar['t_shutdown'] = df_korsar['Time'] - 20.0
df_korsar = df_korsar[df_korsar['t_shutdown'] >= 0]

# 2. Данные из таблицы V1000CT-1 (стр. 92-93)
# t, Q (m3/h), P (kgf/cm2), N (rad/s)
ref_data = np.array([
    [0,   20000, 6.50, 104.196],
    [5,   15650, 4.08, 81.68],
    [10,  12850, 2.70, 67.02],
    [15,  10900, 2.00, 56.76],
    [20,  9400,  1.45, 45.87],
    [25,  8400,  1.15, 43.77],
    [30,  7500,  1.00, 39.06],
    [50,  5160,  0.45, 26.91],
    [90,  3200,  0.15, 15.71],
    [135, 1820,  0.05, 9.42],
    [180, 1100,  0.02, 5.76],
    [210, 720,   0.01, 3.98],
    [232, 0,     0.00, 0.00]
])

# Нормировочные значения
Q0 = 20000.0
P0 = 6.5
N0 = 104.196

ref_time = ref_data[:, 0]
ref_REV = ref_data[:, 3] / N0
ref_QT  = ref_data[:, 1] / Q0
ref_DP  = ref_data[:, 2] / P0

# 3. Аналитические модели для оборотов
t_model = np.linspace(0, 240, 500)
J = 7600.0
M0 = 47500.0
Omega0 = 104.199

# Модель 1: Постоянный момент
REV_model1 = np.maximum(0, 1.0 - (M0 / (J * Omega0)) * t_model)

# Модель 2: Квадратичный момент
K_Omega = M0 / (Omega0**2)
REV_model2 = 1.0 / (1.0 + (K_Omega * Omega0 / J) * t_model)

# 4. Строим графики (теперь 3 графика друг под другом)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# --- Обороты ---
ax1.plot(df_korsar['t_shutdown'], df_korsar['REV'], 'b-', linewidth=2, label='KORSAR (расчет)')
ax1.plot(ref_time, ref_REV, 'ko', markersize=6, label='V1000CT-1 (эксперимент)')
ax1.plot(t_model, REV_model1, 'r--', linewidth=1.5, label='Модель 1 (пост. момент)')
ax1.plot(t_model, REV_model2, 'g--', linewidth=1.5, label='Модель 2 (квадр. момент)')
ax1.set_ylabel('Отн. обороты (REV)', fontsize=12)
ax1.set_title('Сравнение выбега: Обороты', fontsize=14, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper right')
ax1.set_xlim(0, 240)

# --- Расход ---
ax2.plot(df_korsar['t_shutdown'], df_korsar['QT'], 'g-', linewidth=2, label='KORSAR (расчет)')
ax2.plot(ref_time, ref_QT, 'ko', markersize=6, label='V1000CT-1 (эксперимент)')
ax2.set_ylabel('Отн. расход (QT)', fontsize=12)
ax2.set_title('Сравнение выбега: Расход', fontsize=14, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='upper right')
ax2.set_xlim(0, 240)

# --- Давление ---
ax3.plot(df_korsar['t_shutdown'], df_korsar['DP'] / 589467.0, 'k-', linewidth=2, label='KORSAR (расчет)')
ax3.plot(ref_time, ref_DP, 'ko', markersize=6, label='V1000CT-1 (эксперимент)')
ax3.set_xlabel('Время после отключения, с', fontsize=12)
ax3.set_ylabel('Отн. перепад давления (DP)', fontsize=12)
ax3.set_title('Сравнение выбега: Перепад давления', fontsize=14, fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.legend(loc='upper right')
ax3.set_xlim(0, 240)

plt.tight_layout()
if not os.path.exists('pic'):
    os.makedirs('pic')
plt.savefig('pic/comparison.png', dpi=300)
print("График сравнения (3 в 1) сохранен: pic/comparison.png")

plt.show()