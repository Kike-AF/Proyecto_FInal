from flask import Flask, request, render_template, redirect, url_for, session, flash

import db

app = Flask(__name__)

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

app.run(host='0.0.0.0', port=5000, debug=True)
