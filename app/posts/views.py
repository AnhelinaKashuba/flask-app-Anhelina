from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from app import db
from flask import current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Обробка зображення
        image_file = form.image.data
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', image_filename)
            image_file.save(image_path)

        # Створення нового поста
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data or datetime.utcnow(),
            author=session.get("username", "Anhelina"),
            image=f'images/{image_filename}' if image_filename else None
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f"Пост '{new_post.title}' додано успішно!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template('posts/add_post.html', form=form)


@post_bp.route('/')
def get_posts():
    # Отримання всіх постів з БД, відсортованих за спаданням дати
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/post/<int:id>')
def detail_post(id):
    # Отримання конкретного поста за ID
    post = Post.query.get_or_404(id)
    return render_template("posts/detail_post.html", post=post)

@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    # Отримуємо пост за ID або виводимо 404
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash(f"Пост '{post.title}' успішно видалено!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Помилка при видаленні поста!", "danger")
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Отримуємо пост із БД або викидаємо 404
    post = Post.query.get_or_404(post_id)
    
    # Створюємо форму, заповнюючи її полями об'єкта post
    form = PostForm(obj=post)
    
    # Ініціалізуємо дату публікації вручну
    form.publish_date.data = post.posted
    
    if form.validate_on_submit():
        # Оновлюємо поля поста з даних форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data or post.posted  # Використовуємо введену дату або залишаємо попередню

        # Якщо було завантажене нове зображення
        image_file = form.image.data
        if image_file:
            from werkzeug.utils import secure_filename
            import os
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', image_filename)
            image_file.save(image_path)
            post.image = f'images/{image_filename}'

        # Зберігаємо оновлений пост у БД
        db.session.commit()
        flash(f"Post '{post.title}' updated successfully!", "success")
        return redirect(url_for('posts.get_posts'))
    
    # Рендеримо шаблон із формою редагування
    return render_template('posts/add_post.html', form=form, title="Edit Post")
