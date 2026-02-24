from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="secretaria")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(140), nullable=False)
    class_name = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.String(20), nullable=True)
    guardian_name = db.Column(db.String(140), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


def ensure_admin_user() -> None:
    admin = User.query.filter_by(email="admin@escola.local").first()
    if admin:
        return
    admin = User(name="Administrador", email="admin@escola.local", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
