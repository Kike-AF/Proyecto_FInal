import sqlite3 # Importamos el modulo sqlite3
import werkzeug.security # importamos el modulo werkzeug.security para hashear contraseñas
from werkzeug.security import generate_password_hash, check_password_hash # importamos las funciones para hashear y verificar contraseñas

# Función para iniciar la base de datos 

def init_db():

    conn = sqlite3.connect('data.db') # Conectamos a la base de datos
    cursor = conn.cursor() # Creamos un cursor para ejecutar comandos SQL

# Creamos la tabla de pacientes si no existe

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            diagnostico TEXT NOT NULL
        )
    ''')

    # Creamos la tabla de usuarios si no existe

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    ''')

    conn.commit() # Guardamos los cambios
    conn.close() # Cerramos la conexión a la base de datos

# Función para agregar un nuevo paciente a la base de datos

def agregar_paciente(nombre, edad, diagnostico):
    conn = sqlite3.connect('data.db') # Conectamos a la base de datos
    cursor = conn.cursor() # Creamos un cursor para ejecutar comandos SQL
    # Insertamos el nuevo paciente en la tabla
    cursor.execute('''
        INSERT INTO Pacientes (nombre, edad, diagnostico)
        VALUES (?, ?, ?)
    ''', (nombre, edad, diagnostico))

    conn.commit() 
    conn.close() 

    # Función para obtener todos los pacientes de la base de datos

def buscar_pacientes(filtro="", pagina=1, por_pagina=5):
    # Calculamos el desplazamiento para la paginación
    offset = (pagina - 1) * por_pagina
    try:
        conn = sqlite3.connect('data.db') 
        cursor = conn.cursor() 

        # Si hay un filtro, lo aplicamos a la consulta
        if filtro:
            consulta = '''
                SELECT * FROM Pacientes
                WHERE nombre LIKE ? or diagnostico LIKE ?
                LIMIT ? OFFSET ?
            '''
            parametros = ('%' + filtro + '%', '%' + filtro + '%', por_pagina, offset)
            cursor.execute(consulta, parametros)

        else:
            # Si no hay filtro, solo aplicamos la paginación
            consulta = '''
                SELECT * FROM Pacientes
                LIMIT ? OFFSET ?
            '''
            parametros = (por_pagina, offset)
            cursor.execute(consulta, parametros)

        pacientes = cursor.fetchall() # Obtenemos todos los resultados

        if filtro:
            # Obtenemos el total de pacientes para la paginación
            cursor.execute('SELECT COUNT(*) FROM Pacientes WHERE nombre LIKE ? or diagnostico LIKE ?', ('%' + filtro + '%', '%' + filtro + '%'))
        else:
            cursor.execute('SELECT COUNT(*) FROM Pacientes')
        total_pacientes = cursor.fetchone()[0] # Obtenemos el total de pacientes

        conn.close() 
        return pacientes, total_pacientes # Retornamos la lista de pacientes
    
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return [], 0 # Retornamos una lista vacía y 0 si hay un error
    
    # Función para obtener un paciente por su ID
def obtener_paciente_por_id(id):
    conn = sqlite3.connect('data.db') 
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM Pacientes WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    conn.close()
    return paciente
    
    # Función para actualizar un paciente en la base de datos
def actualizar_paciente(id, nombre, edad, diagnostico):
    conn = sqlite3.connect('data.db') 
    cursor = conn.cursor() 
    cursor.execute('''
        UPDATE Pacientes
        SET nombre = ?, edad = ?, diagnostico = ?
        WHERE id = ?
    ''', (nombre, edad, diagnostico, id))
    conn.commit() 
    conn.close()

# Función para eliminar un paciente de la base de datos
def eliminar_paciente(id):
    conn = sqlite3.connect('data.db') 
    cursor = conn.cursor() 
    cursor.execute('DELETE FROM Pacientes WHERE id = ?', (id,))
    conn.commit() 
    conn.close()

# Función para registrar usuario
def registrar_usuario(usuario, contraseña):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    hashed_contraseña = generate_password_hash(contraseña)  # Hasheamos la contraseña

    try:
        cursor.execute('''
            INSERT INTO Usuarios (usuario, contraseña)
            VALUES (?, ?)
        ''', (usuario, hashed_contraseña))
        conn.commit()
        return True  # Registro exitoso
    except sqlite3.IntegrityError:
        print("El usuario ya existe.")
    finally:
        conn.close()

# Función para autenticar usuario
def verificar_usuario(usuario, contraseña):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contraseña FROM Usuarios WHERE usuario = ?', (usuario,))
    row = cursor.fetchone()
    conn.close()

    if row:
        hashed_contraseña = row[0]
        return check_password_hash(hashed_contraseña, contraseña)  # Verificamos la contraseña
    
    return False  # Usuario no encontrado o contraseña incorrecta
