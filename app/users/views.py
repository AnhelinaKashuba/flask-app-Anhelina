from . import bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta

VALID_USERNAME = "anhelina"
VALID_PASSWORD = "12345"

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Успішний вхід!", "success")
            return redirect(url_for("user_name.get_profile"))
        else:
            flash("Невірне ім'я користувача або пароль", "danger")
    return render_template("login.html")


@bp.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if "username" in session:
        username_value = session["username"]
        theme = request.cookies.get('theme', 'light')  # Значення за замовчуванням — світла тема
        
        if request.method == 'POST':
            action = request.form.get('action')
            key = request.form.get('key')
            value = request.form.get('value')
            expiry = request.form.get('expiry')

            if action == "add":
                if not key or not value:
                    flash("Ключ і значення обов'язкові.", "danger")
                else:
                    try:
                        max_age = timedelta(days=int(expiry)) if expiry else timedelta(days=1)
                        response = make_response(render_template("profile.html", username=username_value, cookies=request.cookies, theme=theme))
                        response.set_cookie(key, value, max_age=max_age)
                        flash(f"Кука '{key}' додана!", "success")
                        return response
                    except ValueError:
                        flash("Термін дії куки має бути числом.", "danger")
            elif action == "delete":
                if not key:
                    flash("Ключ обов'язковий для видалення.", "danger")
                else:
                    response = make_response(render_template("profile.html", username=username_value, cookies=request.cookies, theme=theme))
                    response.set_cookie(key, '', expires=0)
                    flash(f"Кука '{key}' видалена!", "success")
                    return response

        cookies = request.cookies
        return render_template("profile.html", username=username_value, cookies=cookies, theme=theme)

    flash("Ви повинні ввійти, щоб переглянути цю сторінку", "warning")
    return redirect(url_for("user_name.login"))



@bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('user_name.get_profile'))

@bp.route('/set_theme/<theme>', methods=['GET'])
def set_theme(theme):
    if theme not in ['light', 'dark']:
        flash("Невірна кольорова схема", "danger")
        return redirect(url_for('user_name.get_profile'))
    
    response = make_response(redirect(url_for('user_name.get_profile')))
    response.set_cookie('theme', theme, max_age=30*24*60*60)  # Зберігаємо на 30 днів
    flash(f"Кольорова схема '{theme}' вибрана!", "success")
    return response
