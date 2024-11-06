from flask import Flask, render_template, request, send_file, redirect, url_for
from logic import increase_image_size  # Импорт функции из logic.py
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Папка для загрузок

# Убедитесь, что папка для загрузок существует
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/uploads/<filename>")
def download_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получаем загруженный файл и параметры
        uploaded_file = request.files["file"]
        new_width = int(request.form["width"])
        new_height = int(request.form["height"])
        target_size_mb = float(request.form["size"])

        # Сохраняем загруженное изображение
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "increased_image.jpg")
        uploaded_file.save(input_path)

        # Вызываем функцию для увеличения размера изображения
        increase_image_size(input_path, output_path, new_width, new_height, target_size_mb)

        # Возвращаем шаблон с кнопкой для скачивания измененного изображения
        return render_template("index.html", image_ready=True, output_path=output_path)

    return render_template("index.html", image_ready=False)


if __name__ == "__main__":
    # Используем порт, предоставленный Heroku, если переменная окружения PORT существует, иначе используем порт 5000 для локальной разработки
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
