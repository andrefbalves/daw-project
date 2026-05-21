import sqlite3

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database_actions import create_user, get_user_by_id, get_user_by_username


def get_logged_user():
    user_id = session.get("user_id")

    if user_id is None:
        return None

    return get_user_by_id(user_id)


def home_page():
    if get_logged_user():
        return redirect(url_for("game_page"))

    return render_template("index.html")


def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = get_user_by_username(username)

    if user is None or not check_password_hash(user.password_hash, password):
        flash("Utilizador ou password invalidos.", "error")
        return redirect(url_for("home_page"))

    session["user_id"] = user.id
    return redirect(url_for("game_page"))


def register():
    if get_logged_user():
        return redirect(url_for("game_page"))

    if request.method == "GET":
        return render_template("register.html")

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not password or not confirm_password:
        flash("Preenche os campos obrigatorios.", "error")
        return redirect(url_for("register"))

    if password != confirm_password:
        flash("As passwords nao coincidem.", "error")
        return redirect(url_for("register"))

    try:
        user = create_user(
            username=username,
            full_name=full_name or None,
            email=email or None,
            password_hash=generate_password_hash(password),
        )
    except sqlite3.IntegrityError:
        flash("Esse utilizador ou email ja existe.", "error")
        return redirect(url_for("register"))

    session["user_id"] = user.id
    return redirect(url_for("game_page"))


def game_page():
    if not get_logged_user():
        return redirect(url_for("home_page"))

    return render_template("game.html")


def logout():
    session.clear()
    return redirect(url_for("home_page"))
