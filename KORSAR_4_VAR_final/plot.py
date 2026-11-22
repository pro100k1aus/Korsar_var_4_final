import pandas as pd
import matplotlib.pyplot as plt
import os

print("--> Скрипт запущен...")

# Создаем папку pic для картинок, если ее нет
if not os.path.exists('pic'):
    os.makedirs('pic')
    print("--> Создана папка pic")

# Указываем ваше точное имя файла
filename = "result.dat"

if not os.path.exists(filename):
    print(f"!!! ОШИБКА: Файл '{filename}' не найден в этой папке!")
    exit()

print(f"--> Читаем данные из файла: {filename}...")
try:
    df = pd.read_csv(filename, sep=r'\s+', skiprows=2, 
                     names=['Time', 'REV', 'QT', 'DP'], engine='python')
    print(f"--> Данные успешно прочитаны! Строк: {len(df)}")
except Exception as e:
    print(f"!!! ОШИБКА при чтении файла: {e}")
    exit()

print("--> Строим графики...")

# --- СОЗДАЕМ 3 ОТДЕЛЬНЫХ ГРАФИКА (3 строки, 1 колонка) ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# 1. График оборотов (REV)
ax1.plot(df['Time'], df['REV'], 'b-', linewidth=2)
ax1.axvline(x=20.0, color='r', linestyle='--', linewidth=2, label='Отключение (t=20 с)')
ax1.set_ylabel('Обороты (REV), отн. ед.', fontsize=12)
ax1.set_title('Выбег насоса: Обороты', fontsize=14, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# 2. График расхода (QT)
ax2.plot(df['Time'], df['QT'], 'g-', linewidth=2)
ax2.axvline(x=20.0, color='r', linestyle='--', linewidth=2, label='Отключение (t=20 с)')
ax2.set_ylabel('Расход (QT), отн. ед.', fontsize=12)
ax2.set_title('Выбег насоса: Расход', fontsize=14, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

# 3. График давления (DP)
ax3.plot(df['Time'], df['DP'] / 1000.0, 'k-', linewidth=2)
ax3.axvline(x=20.0, color='r', linestyle='--', linewidth=2, label='Отключение (t=20 с)')
ax3.set_xlabel('Время, с', fontsize=12)
ax3.set_ylabel('Давление (DP), кПа', fontsize=12)
ax3.set_title('Выбег насоса: Перепад давления', fontsize=14, fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.legend()

# Автоматически выравниваем расстояния между графиками
plt.tight_layout()
plt.savefig('pic/coastdown.png', dpi=300)
print("--> Общий график (3 в 1) сохранен: pic/coastdown.png")

# --- ГРАФИК 4: СТАЦИОНАРНАЯ ХАРАКТЕРИСТИКА H(Q) ---
plt.figure(figsize=(8, 6))
# Берем последнюю точку до отключения (t < 20)
steady = df[df['Time'] < 20].iloc[-1]
Q = steady['QT']
H = steady['DP'] / 1000.0

plt.plot(Q, H, 'ro', markersize=10, label='Стационарная точка (из КОРСАР)')
plt.xlabel('Относительный расход (q)', fontsize=12)
plt.ylabel('Перепад давления, кПа', fontsize=12)
plt.title('Характеристика H(Q)', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('pic/qh_characteristic.png', dpi=300)
print("--> График H(Q) сохранен: pic/qh_characteristic.png")

print("=======================================")
print("УСПЕХ! Все графики сохранены в папку 'pic'.")
print("=======================================")

# Показ окон на экране
plt.show()