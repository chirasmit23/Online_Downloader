from flask import Flask
def create_app():
    app = Flask(
        __name__,
        template_folder="Frontend/templates",
        static_folder="Frontend/static", 
    )
    from .routes import all_routes
    all_routes(app)
    return app