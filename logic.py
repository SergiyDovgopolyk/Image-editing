from PIL import Image, PngImagePlugin
import os
import random

def add_metadata(image, size_increase_kb):
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Description", "X" * 1024 * size_increase_kb)
    return metadata

def increase_image_size(input_path, output_path, new_width, new_height, target_size_mb):
    # Открываем изображение и изменяем размер
    image = Image.open(input_path)
    resized_image = image.resize((new_width, new_height))

    # Добавляем метаданные для увеличения размера
    metadata = add_metadata(resized_image, size_increase_kb=512)  # можно поэкспериментировать с размером

    # Сохраняем изображение с метаданными в PNG
    resized_image.save(output_path, format="PNG", pnginfo=metadata)
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Текущий размер файла после добавления метаданных: {file_size_mb:.2f} МБ")

    # Проверяем, достигли ли целевого размера, и добавляем шум, если не достигли
    while file_size_mb < target_size_mb:
        resized_image = add_noise(resized_image)
        resized_image.save(output_path, format="PNG", pnginfo=metadata)
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Текущий размер файла: {file_size_mb:.2f} МБ")

        # Если достигли целевого размера, выходим из цикла
        if file_size_mb >= target_size_mb:
            break

    print(f"Изображение сохранено с размером {file_size_mb:.2f} МБ")

def add_noise(image):
    pixels = image.load()
    width, height = image.size

    # Увеличиваем интенсивность шума для роста размера
    for i in range(width):
        for j in range(height):
            if random.randint(0, 10) < 3:  # Применяем шум примерно к 30% пикселей
                r, g, b = pixels[i, j]
                noise = random.randint(-50, 50)
                pixels[i, j] = (
                    min(255, max(0, r + noise)),
                    min(255, max(0, g + noise)),
                    min(255, max(0, b + noise))
                )
    return image

if __name__ == "__main__":
    input_path = input("Введите путь к изображению: ")
    output_path = "increased_image.png"
    new_width = int(input("Введите новую ширину: "))
    new_height = int(input("Введите новую высоту: "))
    target_size_mb = float(input("Введите целевой размер файла (в МБ): "))

    increase_image_size(input_path, output_path, new_width, new_height, target_size_mb)
