from flask import Flask, render_template, request, jsonify
import os
import sqlite3
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

model_path = 'C:/Users/Huawei/.cache/kagglehub/models/krishnagarigipati/pneumonia-detector/keras/v1/1/final_pneumonia_model.h5'

# Создаем папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('pneumonia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  prediction REAL NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Загрузка модели
try:
    model = load_model(model_path)
    logger.info("Модель успешно загружена")
except Exception as e:
    logger.error(f"Ошибка при загрузке модели: {str(e)}")
    raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path):
    try:
        img = load_img(img_path, target_size=(224, 224), color_mode='rgb')
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.warning("Файл не найден в запросе")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("Пустое имя файла")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logger.info(f"Файл сохранен: {filepath}")
            
            # Обработка изображения и получение предсказания
            processed_image = preprocess_image(filepath)
            prediction = model.predict(processed_image)[0][0]
            logger.info(f"Получено предсказание: {prediction}")
            
            # Сохранение результата в базу данных
            conn = sqlite3.connect('pneumonia.db')
            c = conn.cursor()
            c.execute('INSERT INTO predictions (filename, prediction) VALUES (?, ?)',
                     (filename, float(prediction)))
            conn.commit()
            conn.close()
            logger.info("Результат сохранен в базу данных")
            
            # Удаление файла после обработки
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info("Файл удален после обработки")
            
            result_message = 'Пневмония обнаружена' if prediction > 0.5 else 'Пневмония не обнаружена'
            probability = float(prediction) * 100
            
            return jsonify({
                'success': True,
                'prediction': float(prediction)
            })
            
        except Exception as e:
            logger.error(f"Ошибка при обработке файла: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info("Файл удален после ошибки")
            return jsonify({'error': str(e)}), 500
    
    logger.warning("Неверный тип файла")
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 