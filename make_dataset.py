from pathlib import Path
import random
import shutil

SOURCE_DIR = Path("labels")
OUTPUT_DIR = Path("dataset_yolo")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
TRAIN_RATIO = 0.8
SEED = 42

images = [
    path for path in SOURCE_DIR.iterdir()
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
]

if not images:
    raise SystemExit(f"В папке {SOURCE_DIR} не найдены изображения.")

# Для каждого изображения требуется одноимённый .txt.
missing = [image.name for image in images if not image.with_suffix(".txt").is_file()]
if missing:
    print("Не найдены файлы разметки для:")
    for name in missing:
        print(f"  {name}")
    raise SystemExit("Добавь соответствующие .txt-файлы и запусти скрипт снова.")

random.Random(SEED).shuffle(images)
split_index = int(len(images) * TRAIN_RATIO)

# Если изображений больше одного, оставляем хотя бы одно для val.
if len(images) > 1:
    split_index = max(1, min(split_index, len(images) - 1))

splits = {
    "train": images[:split_index],
    "val": images[split_index:],
}

for split_name, split_images in splits.items():
    image_dir = OUTPUT_DIR / "images" / split_name
    label_dir = OUTPUT_DIR / "labels" / split_name
    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    for image in split_images:
        shutil.copy2(image, image_dir / image.name)
        shutil.copy2(image.with_suffix(".txt"), label_dir / image.with_suffix(".txt").name)

# Создаём конфигурацию датасета YOLO
yaml_content = """path: .
train: images/train
val: images/val

names:
  0: game
"""
(OUTPUT_DIR / "data.yaml").write_text(yaml_content, encoding="utf-8")

print(f"Готово! Датасет создан в папке: {OUTPUT_DIR.resolve()}")
print(f"Train: {len(splits['train'])} изображений")
print(f"Val:   {len(splits['val'])} изображений")
print(f"Конфиг: {OUTPUT_DIR / 'data.yaml'}")