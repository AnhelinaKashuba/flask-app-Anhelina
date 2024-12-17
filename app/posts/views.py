from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from app import db
from flask import current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from .models import User
from .models import Tag


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    form.author_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()]

    if form.validate_on_submit():
        image_file = form.image.data
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', image_filename)
            image_file.save(image_path)

        # Create new post
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data or datetime.utcnow(),
            user_id=int(form.author_id.data),
            image=f'images/{image_filename}' if image_filename else None
        )

        # Add selected tags to the post
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(selected_tags)

        # Add post to the database
        db.session.add(new_post)
        db.session.commit()

        flash(f"Пост '{new_post.title}' додано успішно!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template('posts/add_post.html', form=form)




@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/post/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/detail_post.html", post=post)

@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
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
    post = Post.query.get_or_404(post_id)
    
    form = PostForm(obj=post)
    
    form.publish_date.data = post.posted
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data or post.posted  

        image_file = form.image.data
        if image_file:
            from werkzeug.utils import secure_filename
            import os
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', image_filename)
            image_file.save(image_path)
            post.image = f'images/{image_filename}'

        db.session.commit()
        flash(f"Post '{post.title}' updated successfully!", "success")
        return redirect(url_for('posts.get_posts'))
    
    return render_template('posts/add_post.html', form=form, title="Edit Post")

    def upgrade():
        with op.batch_alter_table('posts', schema=None) as batch_op:
            batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key('user_id', 'users', ['user_id'], ['id'])
            batch_op.drop_column('author')