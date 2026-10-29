import cv2
import albumentations as A
from pathlib import Path

# Пути относительно папки со скриптом
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "screenshots"
OUTPUT_DIR = BASE_DIR / "screenshots_augmented"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

if not INPUT_DIR.exists():
    raise FileNotFoundError(f"Папка с исходными изображениями не найдена: {INPUT_DIR}")

files = [
    f for f in INPUT_DIR.iterdir()
    if f.is_file() and f.suffix.lower() in image_extensions
]

print(f"Исходная папка: {INPUT_DIR}")
print(f"Папка для результатов: {OUTPUT_DIR}")
print(f"Найдено изображений: {len(files)}")

if not files:
    raise SystemExit("В папке screenshots нет изображений подходящих форматов.")

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.3),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(
        shift_limit=0.05, scale_limit=0.1, rotate_limit=15, p=0.5
    ),
    A.Perspective(scale=(0.02, 0.08), p=0.3),
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(
        hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=20, p=0.4
    ),
    A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.3),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),
    A.MotionBlur(blur_limit=5, p=0.2),
    A.OpticalDistortion(distort_limit=0.1, shift_limit=0.05, p=0.3),
    A.GridDistortion(num_steps=5, distort_limit=0.1, p=0.3),
    A.RandomResizedCrop(size=(640, 640), scale=(0.8, 1.0), p=0.4),
])

NUM_AUGS = 5
created = 0

for idx, image_path in enumerate(files):
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Не удалось прочитать: {image_path}")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for i in range(NUM_AUGS):
        aug_image = transform(image=image)["image"]
        aug_image = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)

        out_path = OUTPUT_DIR / f"{image_path.stem}_aug{i}_{idx}.jpg"

        if cv2.imwrite(str(out_path), aug_image):
            created += 1
        else:
            print(f"Не удалось сохранить: {out_path}")

    print(f"Обработано: {idx + 1}/{len(files)}")

print(f"Готово! Создано изображений: {created}")
print(f"Результаты находятся в: {OUTPUT_DIR}")
