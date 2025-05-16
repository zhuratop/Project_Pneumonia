from flask import Flask, render_template, request, jsonify
import os
import sqlite3
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.layers import InputLayer
import numpy as np
import logging
import sys
import json
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Путь к модели относительно текущей директории
model_path = 'models/final_pneumonia_model.h5'

# Создаем папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Создаем папку для модели, если её нет
os.makedirs('models', exist_ok=True)

# Кастомный класс для загрузки старой модели
class CustomInputLayer(InputLayer):
    @classmethod
    def from_config(cls, config):
        # Преобразуем batch_shape в input_shape и batch_size
        if 'batch_shape' in config:
            batch_shape = config.pop('batch_shape')
            if batch_shape[0] is None:  # Если batch_size не определен
                config['input_shape'] = batch_shape[1:]
            else:
                config['input_shape'] = batch_shape[1:]
                config['batch_size'] = batch_shape[0]
        return super(CustomInputLayer, cls).from_config(config)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('pneumonia.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            result TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_result(filename, result, confidence):
    conn = sqlite3.connect('pneumonia.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO results (filename, result, confidence)
        VALUES (?, ?, ?)
    ''', (filename, result, confidence))
    conn.commit()
    conn.close()

def get_last_results(limit=3):
    conn = sqlite3.connect('pneumonia.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, filename, result, confidence, timestamp
        FROM results
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    return results

# Загрузка модели
try:
    if not os.path.exists(model_path):
        logger.error(f"Модель не найдена по пути: {model_path}")
        logger.error("Пожалуйста, убедитесь, что файл модели находится в папке models/")
        sys.exit(1)
    
    # Регистрируем кастомный класс для загрузки
    custom_objects = {'InputLayer': CustomInputLayer}
    model = load_model(model_path, custom_objects=custom_objects)
    logger.info("Модель успешно загружена")
except Exception as e:
    logger.error(f"Ошибка при загрузке модели: {str(e)}")
    sys.exit(1)

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
def index():
    last_results = get_last_results()
    return render_template('index.html', last_results=last_results)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            logger.error("Файл не найден в запросе")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("Пустое имя файла")
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(filepath)
                logger.info(f"Файл сохранен: {filepath}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении файла: {str(e)}")
                return jsonify({'error': 'Error saving file'}), 500
            
            try:
                # Получаем предсказание
                prediction = model.predict(preprocess_image(filepath))
                result = "Пневмония" if prediction[0][0] > 0.5 else "Норма"
                confidence = float(prediction[0][0])
                logger.info(f"Получено предсказание: {result} (уверенность: {confidence})")
            except Exception as e:
                logger.error(f"Ошибка при обработке изображения: {str(e)}")
                return jsonify({'error': 'Error processing image'}), 500
            
            try:
                # Сохраняем результат
                save_result(filename, result, confidence)
                logger.info("Результат сохранен в базу данных")
            except Exception as e:
                logger.error(f"Ошибка при сохранении результата в БД: {str(e)}")
                return jsonify({'error': 'Error saving result'}), 500
            
            # Получаем последние результаты для отображения
            last_results = get_last_results()
            
            return render_template('result.html', 
                                 prediction=result,
                                 confidence=confidence,
                                 filename=filename,
                                 last_results=last_results)
        else:
            logger.error(f"Недопустимый тип файла: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False) 