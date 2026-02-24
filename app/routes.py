from functools import wraps

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from .models import Student, User
from .services import import_students_from_excel


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in roles:
                flash("Você não tem permissão para acessar este recurso.", "error")
                return redirect(url_for("dashboard"))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def register_routes(app):
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "")
            password = request.form.get("password", "")

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("dashboard"))

            flash("E-mail ou senha inválidos.", "error")

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        students_count = Student.query.count()
        return render_template("dashboard.html", students_count=students_count)

    @app.route("/alunos")
    @login_required
    def students():
        data = Student.query.order_by(Student.name.asc()).all()
        return render_template("students.html", students=data)

    @app.route("/importar", methods=["GET", "POST"])
    @login_required
    @role_required("admin", "secretaria")
    def import_excel():
        if request.method == "POST":
            file = request.files.get("file")
            if file is None or file.filename == "":
                flash("Selecione uma planilha .xlsx", "error")
                return redirect(url_for("import_excel"))

            try:
                result = import_students_from_excel(file)
                flash(
                    f"Importação finalizada: {result.inserted} inseridos, {result.updated} atualizados.",
                    "success",
                )
                return redirect(url_for("students"))
            except ValueError as exc:
                flash(str(exc), "error")

        return render_template("import.html")

    @app.route("/documentos/declaracao/<int:student_id>")
    @login_required
    def declaracao(student_id: int):
        student = Student.query.get_or_404(student_id)
        return render_template("document_declaration.html", student=student)

    @app.route("/documentos/ficha-some/<int:student_id>")
    @login_required
    def ficha_some(student_id: int):
        student = Student.query.get_or_404(student_id)
        return render_template("document_some.html", student=student)
