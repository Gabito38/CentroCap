from flask import Flask
from config import Config
from Models.database import create_tables

def create_app():
    app = Flask(__name__, template_folder='Views')
    app.config.from_object(Config)

    from Controllers.auth_controller import bp as auth_controller
    app.register_blueprint(auth_controller, url_prefix='/auth')

    from Controllers.dashboard_controller import bp as dashboard_controller
    app.register_blueprint(dashboard_controller)

    from Controllers.estudiantes_controller import bp as estudiantes_controller
    app.register_blueprint(estudiantes_controller, url_prefix='/estudiantes')

    from Controllers.cursos_controller import bp as cursos_controller
    app.register_blueprint(cursos_controller, url_prefix='/cursos')

    from Controllers.inscripcion_controller import bp as inscripcion_controller
    app.register_blueprint(inscripcion_controller, url_prefix='/inscripcion')

    from Controllers.usuarios_controller import bp as usuarios_controller
    app.register_blueprint(usuarios_controller, url_prefix='/usuarios')

    with app.app_context():
        create_tables()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
