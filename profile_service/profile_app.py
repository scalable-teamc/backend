from flask import Flask

from profile_service import profile_db
from profile_service.profile_controller import profile_controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/profile_db"

if __name__ == '__main__':
    profile_db.init_app(app)
    with app.app_context():
        profile_db.create_all()
        profile_db.session.commit()
    app.register_blueprint(profile_controller)

    # run app in debug mode on port 8084
    app.run(debug=True, port=8084)
