from flask import Flask
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()  # Load from .env

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')
    app.config['STRIPE_PUBLISHABLE_KEY'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
    app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')

    from .routes import bp
    app.register_blueprint(bp)

    return app
