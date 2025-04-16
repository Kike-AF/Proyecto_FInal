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

def obtener_pacientes():
    try:
        conn = sqlite3.connect('data.db') 
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM Pacientes')
        pacientes = cursor.fetchall() # Obtenemos todos los resultados
        conn.close() 
        return pacientes # Retornamos la lista de pacientes
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return []
    
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
