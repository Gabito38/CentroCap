from flask import Blueprint, render_template, request, redirect, url_for, flash
from Models.database import get_db_connection
from Utils.helpers import login_required

bp = Blueprint('inscripcion_controller', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    inscripciones = conn.execute('''
                SELECT i.id, e.nombre, e.apellidos, i.fecha, c.descripcion
                FROM inscripcion i
                JOIN estudiantes e ON e.id = i.estudiante_id
                JOIN cursos c ON c.id = i.curso_id
                ORDER BY i.id DESC''').fetchall()
    conn.close()
    return render_template('inscripcion/list.html', inscripciones=inscripciones)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estudiante_id = request.form['estudiante_id']
        curso_id = request.form['curso_id']
        
        conn.execute("INSERT INTO inscripcion (fecha, estudiante_id, curso_id) VALUES (?, ?, ?)",
                        (fecha, estudiante_id, curso_id))
        conn.commit()
        conn.close()
        
        flash('Inscripción agregada correctamente.')
        return redirect(url_for('inscripcion_controller.index'))
    
    conn.close()
    return render_template('inscripcion/add.html', estudiantes=estudiantes, cursos=cursos)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    inscripcion = conn.execute("SELECT * FROM inscripcion WHERE id = ?", (id,)).fetchone()
    if not inscripcion:
        conn.close()
        flash('Inscripcion no encontrada')
        return redirect(url_for('inscripcion_controller.index'))
    
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estudiante_id = request.form['estudiante_id']
        curso_id = request.form['curso_id']

        conn.execute("UPDATE inscripcion SET fecha=?, estudiante_id=?, curso_id=? WHERE id=?",
                        (fecha, estudiante_id, curso_id, id))
        conn.commit()
        conn.close()

        flash('inscripcion actualizada correctamente')
        return redirect(url_for('inscripcion_controller.index'))
    
    conn.close()
    return render_template('inscripcion/edit.html', inscripcion=inscripcion, estudiantes=estudiantes, cursos=cursos)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inscripcion WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    flash('Inscripcion eliminada correctamente.')
    return redirect(url_for('inscripcion_controller.index'))