import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

def analyze_model(model_path):
    try:
        # Загружаем модель
        model = load_model(model_path)
        
        # Выводим информацию о модели
        print("\n=== Информация о модели ===")
        print(f"Тип модели: {type(model).__name__}")
        print(f"Количество слоев: {len(model.layers)}")
        
        # Выводим структуру модели
        print("\n=== Структура модели ===")
        model.summary()
        
        # Проверяем входные и выходные данные
        print("\n=== Входные и выходные данные ===")
        print(f"Входная форма: {model.input_shape}")
        print(f"Выходная форма: {model.output_shape}")
        
        # Проверяем веса модели
        print("\n=== Информация о весах ===")
        total_params = model.count_params()
        print(f"Общее количество параметров: {total_params:,}")
        
        # Проверяем, является ли это моделью для классификации
        if model.output_shape[-1] == 1:
            print("\nЭто модель бинарной классификации (подходит для определения пневмонии)")
        else:
            print("\nЭто модель с несколькими классами")
            
    except Exception as e:
        print(f"Ошибка при анализе модели: {str(e)}")

if __name__ == '__main__':
    model_path = 'models/final_pneumonia_model.h5'
    analyze_model(model_path) 