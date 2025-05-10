import os
import kagglehub
import shutil
import sys

def download_model():
    # Создаем директорию для модели, если её нет
    os.makedirs('models', exist_ok=True)
    
    print("Загрузка модели...")
    try:
        # Загружаем модель через kagglehub
        model_path = kagglehub.model_download("krishnagarigipati/pneumonia-detector/keras/v1")
        
        # Копируем модель в нужную директорию
        shutil.copy(model_path, 'models/final_pneumonia_model.h5')
        print("Модель успешно загружена")
        
    except Exception as e:
        print(f"Ошибка при загрузке модели: {str(e)}")
        print("\nПожалуйста, выполните следующие шаги вручную:")
        print("1. Зарегистрируйтесь на Kaggle (https://www.kaggle.com)")
        print("2. Перейдите в Account -> Create New API Token")
        print("3. Скачайте kaggle.json")
        print("4. Создайте папку .kaggle в вашей домашней директории")
        print("5. Поместите kaggle.json в папку .kaggle")
        print("6. Запустите скрипт снова")
        sys.exit(1)

def check_model():
    # Проверяем наличие директории models
    if not os.path.exists('models'):
        print("Ошибка: директория models не найдена")
        sys.exit(1)
    
    # Проверяем наличие файла модели
    model_path = 'models/final_pneumonia_model.h5'
    if not os.path.exists(model_path):
        print(f"Ошибка: файл модели не найден по пути {model_path}")
        print("Пожалуйста, убедитесь, что файл модели находится в папке models/")
        sys.exit(1)
    
    print("Модель найдена в папке models/")

if __name__ == '__main__':
    check_model() 