import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Models.database import get_db_connection
from werkzeug.security import generate_password_hash
from Utils.helpers import login_required

bp = Blueprint('usuarios_controller', __name__, template_folder='../templates')

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios ORDER BY id DESC").fetchall()
    return render_template('usuarios/list.html', usuarios=usuarios)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        usuario = request.form['nombre']
        correo = request.form['correo']
        celular = request.form['ceular']
        contraseña = request.form['contraseña']
        confirmar = request.form['confirmar']

        if contraseña != confirmar:
            flash('Las contraseñas no coinciden.')
            return render_template('usuarios/add.html')
        
        conn = get_db_connection()
        try:
            from werkzeug.security import generate_password_hash
            hashed = generate_password_hash(contraseña)
            conn.execute("INSERT INTO usuarios (usuario, correo, celular, contraseña) VALUES (?, ?, ?, ?)",
                        (usuario, correo, celular, hashed))
            conn.commit()
            flash('Usuario agregado correctamente')
            return redirect(url_for('usuarios_controller.index'))
        except sqlite3.IntegrityError:
            flash('Usuario o correo ya registrado: ')
        finally:
            conn.close()

    return render_template('usuarios/add.html')
