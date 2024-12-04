from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
import json
from flask import current_app

JSON_FILE = "app/posts/posts.json"


posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Завантажити існуючі пости
        posts = load_posts()

        # Дані нового поста
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publication_date": form.publish_date.data,
            "author": session.get("username", "Anhelina")  
        }

        # Додати новий пост
        posts.append(new_post)
        save_posts(posts)

        flash(f"Пост '{new_post['title']}' додано успішно!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template('posts/add_post.html', form=form)


@post_bp.route('/')
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == id), None)
    if not post:
        abort(404)
    return render_template("posts/detail_post.html", post=post)


def load_posts():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Якщо файл не існує, повертаємо порожній список
    except json.JSONDecodeError:
        return []  # Якщо помилка у форматі файлу

from datetime import date

def save_posts(posts):
    # Перетворюємо кожну дату на рядок перед збереженням
    for post in posts:
        if isinstance(post['publication_date'], date):
            post['publication_date'] = post['publication_date'].strftime('%Y-%m-%d')

    with open('app/posts/posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)