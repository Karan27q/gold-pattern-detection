from flask import Flask
from app.routes import routes as main_blueprint

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(main_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)