from flask import Blueprint

bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
    template_folder="templates/users",
)

# Імпортуємо views тут, після визначення `bp`
from . import views
