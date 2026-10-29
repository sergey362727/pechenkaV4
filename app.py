import time

import cv2
import numpy as np
import pyautogui
from mss import mss
from ultralytics import YOLO


model = YOLO("runs/detect/cookie_detector/weights/best.pt")

TARGET_CLASSES = {"game", "add", "upp1", "upp2"}
CONFIDENCE_THRESHOLD = 0.5
CLICKS_ON_GAME = 10

# Убираем встроенную задержку PyAutoGUI
pyautogui.PAUSE = 0.01
pyautogui.MINIMUM_DURATION = 0.01


def find_and_click(sct, monitor):
    screenshot = np.array(sct.grab(monitor))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    results = model(screenshot, verbose=False)
    detections = []

    for result in results:
        for box in result.boxes:
            confidence = box.conf[0].item()
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            class_id = int(box.cls[0].item())
            class_name = model.names[class_id]

            if class_name not in TARGET_CLASSES:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            center_x = monitor["left"] + (x1 + x2) / 2
            center_y = monitor["top"] + (y1 + y2) / 2

            detections.append((class_name, center_x, center_y))
            print(f"Обнаружено: {class_name}, уверенность: {confidence:.2f}")

    # Сначала кликаем по улучшениям, затем по печенью
    priority = {"upp1": 0, "upp2": 1, "add": 2, "game": 3}
    detections.sort(key=lambda item: priority[item[0]])

    for class_name, center_x, center_y in detections:
        click_count = CLICKS_ON_GAME if class_name == "game" else 1

        for _ in range(click_count):
            pyautogui.click(center_x, center_y)

        print(f"Клик: {class_name} ({center_x:.0f}, {center_y:.0f})")

    return bool(detections)


with mss() as sct:
    monitor = sct.monitors[1]

    try:
        while True:
            if not find_and_click(sct, monitor):
                time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nСкрипт остановлен.")
