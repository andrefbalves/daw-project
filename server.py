from flask import Flask, g
import views
from database_actions import init_database

def create_app():
    app = Flask(__name__)

    app.config.from_object('settings')

    with app.app_context():
        init_database()

    @app.before_request
    def load_current_user():
        g.current_user = views.get_logged_user()

    @app.context_processor
    def inject_current_user():
        return {"current_user": g.get("current_user")}

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login, methods=["POST"])
    app.add_url_rule("/register", view_func=views.register, methods=["GET", "POST"])
    app.add_url_rule("/jogo", view_func=views.game_page)
    app.add_url_rule("/logout", view_func=views.logout)

    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get("PORT", 5000)

    app.run(host='0.0.0.0', port=port)
