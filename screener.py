import time
import os
from datetime import datetime
import mss

# Папка для сохранения скриншотов
save_dir = "screenshots"
os.makedirs(save_dir, exist_ok=True)

print("Начинаю делать скриншоты каждые 5 секунд...")
print("Нажмите Ctrl+C для остановки\n")

count = 0

try:
    with mss.mss() as sct:
        while True:
            # Скриншот всего экрана
            screenshot = sct.grab(sct.monitors[0])

            # Формируем имя файла с датой и временем
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{save_dir}/screenshot_{timestamp}.png"

            # Сохраняем
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
            count += 1
            print(f"[{count}] Сохранено: {filename}")

            time.sleep(5)

except KeyboardInterrupt:
    print(f"\nОстановлено. Всего сделано скриншотов: {count}")
