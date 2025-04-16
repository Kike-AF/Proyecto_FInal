from flask import Flask, request, render_template, redirect, url_for, session, flash

import db
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) # Generar una clave secreta aleatoria para la sesión

# Inicializar la base de datos
db.init_db()

@app.route('/')
def index():

    # Obtener lista de pacientes 
    pacientes = db.obtener_pacientes()
    return render_template('index.html', pacientes=pacientes)

@app.route('/nuevo_paciente', methods=['GET', 'POST'])

def nuevo_paciente():

    # Obtener los datos del formulario
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        diagnostico = request.form['diagnostico']

        if not nombre or not edad or not diagnostico:
            flash('Por favor, completa todos los campos obligatorios', 'error')
            return redirect(url_for('nuevo_paciente'))

        # Agregar el nuevo paciente a la base de datos
        db.agregar_paciente(nombre, edad, diagnostico)
        flash('Paciente agregado exitosamente')

        # Redigir a la página de inicio
        return redirect(url_for('index'))
    
    # Si es un GET, simplemente mostramos el formulario
    return render_template('nuevo_paciente.html')

# Ruta para editar un paciente
@app.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    # Obtener el paciente de la base de datos
    paciente = db.obtener_paciente(id)

    # Si el paciente fue enviado con el metodo post
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        diagnostico = request.form['diagnostico']

        # Verificar que los campos no estén vacíos
        if not nombre or not edad or not diagnostico:
            flash('Por favor, completa todos los campos que son obligatorios')
            return redirect(url_for('editar_paciente', id=id))

        # Actualizar el paciente en la base de datos
        db.actualizar_paciente(id, nombre, int(edad), diagnostico)
        flash('Paciente actualizado exitosamente')

        # Redigir a la página de inicio
        return redirect(url_for('index'))
    # Si la solicitud es un GET, simplemente renderizamos el formulario 
    return render_template('editar_paciente.html', paciente=paciente)

# Define la ruta que responda a las solicitudes POST para eliminar un paciente
@app.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    # Llamamos a la función de eliminar paciente en la base de datos
    db.eliminar_paciente(id)
    flash('Paciente eliminado exitosamente')
    # Redigir a la página de inicio
    return redirect(url_for('index'))

app.run(host='0.0.0.0', port=5000, debug=True)
