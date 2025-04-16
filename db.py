import sqlite3 # Importamos el modulo sqlite3

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
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
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

    conn.commit() # Guardamos los cambios
    conn.close() # Cerramos la conexión a la base de datos

    # Función para obtener todos los pacientes de la base de datos

def obtener_pacientes():

    conn = sqlite3.connect('data.db') # Conectamos a la base de datos
    cursor = conn.cursor() # Creamos un cursor para ejecutar comandos SQL
    cursor.execute('SELECT * FROM Pacientes')
    pacientes = cursor.fetchall() # Obtenemos todos los resultados
    conn.close() # Cerramos la conexión a la base de datos
    return pacientes # Retornamos la lista de pacientes