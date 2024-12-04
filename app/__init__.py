from flask import Flask

# Створення factory-функції для Flask додатка
def create_app(config_name="config"):
    # Ініціалізація Flask додатка
    app = Flask(__name__)
    
    # Завантаження конфігурацій з об'єкта, що передається
    app.config.from_object(config_name)
    
    # Реєстрація блюпринтів
    with app.app_context():
        # Імпортуємо та реєструємо в'юшки та блюпринти
        from . import views  # Імпортуємо основні в'юшки
        from .posts import post_bp  # Імпортуємо блюпринт для постів
        from .users import bp as user_bp  # Імпортуємо блюпринт для користувачів
        
        # Реєструємо блюпринти
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp, url_prefix="/users")
    
    # Повертаємо налаштований додаток
    return app
