from flask import *
import mysql.connector
from datetime import datetime
import openpyxl

app = Flask(__name__)
app.secret_key = 'secreta'

def conectar_db():
    conn = mysql.connector.connect(
        host="b4ogxjpclwt26y70k5gq-mysql.services.clever-cloud.com",
        user="uumtgeq1tnwb4iox",
        password="4qMfeI5WpDuh5RHRhcv1",
        database="b4ogxjpclwt26y70k5gq"
    )
    return conn

@app.route('/conf', methods=['GET'])
def hello_world():
    return '¡Flask está funcionando!'

@app.route('/consulta', methods=['GET'])
def index():
   
    conn = conectar_db()
    if conn is None:
        return "No se pudo conectar a la base de datos"
    
   
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()

   
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    print(fecha_actual)
    cursor.execute("""
        SELECT num_lista, nombres, apellidos, fecha, hora 
        FROM asistencia 
        WHERE fecha = %s
        """, (fecha_actual,))

# Obtener los resultados de la consulta
    asistencias = cursor.fetchall()


    cursor.close()
    conn.close()

    
    return render_template('consulta.html', alumnos=alumnos, asistencias=asistencias)

@app.route('/formulario', methods=['GET'])
def formulario():
    


    return render_template('agregar_alumno.html')

@app.route('/agregar_alumno', methods=['POST'])
def agregar_alumno():
    try:
        id = request.form['id']
        num_lista = request.form['num_lista']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        codigo = request.form['codigo']

        # Conectar a la base de datos
        conn = conectar_db()
        cursor = conn.cursor()

        # Verificar si el número de lista ya existe
        query_check = "SELECT * FROM alumnos WHERE num_lista = %s"
        cursor.execute(query_check, (num_lista,))
        alumno_existente = cursor.fetchone()

        if alumno_existente:
            # Cerrar la conexión si el número de lista ya existe
            cursor.close()
            conn.close()
            flash("Error: El número de lista ya está en uso.", "error")
            return redirect(url_for('formulario'))
        # Consulta SQL para insertar un nuevo alumno
        query_insert = """
        INSERT INTO alumnos (id, num_lista, nombres, apellidos, codigo)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (id, num_lista, nombres, apellidos, codigo))
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        return redirect('/consulta')  # Redirige a la página de consulta después de agregar el alumno

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/verificar_asistencia', methods=['POST'])
def verificar_asistencia(): 
    try:
        data = request.json
        id = data['id']
        fecha = data['fecha']

        conn = conectar_db()
        cursor = conn.cursor()

        # Verificar si el alumno existe en la tabla 'alumnos'
        query = "SELECT * FROM alumnos WHERE id = %s"
        cursor.execute(query, (id,))
        alumno = cursor.fetchone()

        if alumno:
            # Verificar si ya ha registrado asistencia el día actual
            query_asistencia = "SELECT * FROM asistencia WHERE id = %s AND fecha = %s"
            cursor.execute(query_asistencia, (id, fecha))
            asistencia = cursor.fetchone()

            if asistencia:
                return jsonify({"mensaje": "Asistencia ya registrada para hoy."}), 500
            else:
                # Insertar la asistencia en la base de datos
                id = alumno[0]
                num_lista = alumno[1]  # Asumiendo que el campo 'num_lista' es el primero
                nombres = alumno[2]  # Asumiendo que el campo 'nombres' es el segundo
                apellidos = alumno[3]  # Asumiendo que el campo 'apellidos' es el tercero
                codigo = alumno[4]  # Asumiendo que el campo 'codigo_alumno' es el cuarto
                hora = datetime.now().strftime('%H:%M:%S')

                query_insert = """
                INSERT INTO asistencia (id, num_lista, nombres, apellidos, codigo, fecha, hora)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_insert, (id, num_lista, nombres, apellidos, codigo, fecha, hora))
                conn.commit()

                # Agregar la asistencia al archivo Excel
                agregar_a_excel(id, num_lista, nombres, apellidos, codigo, fecha, hora)

                return jsonify({"mensaje": "Asistencia registrada correctamente."}), 200
        else:
            return jsonify({"mensaje": "Alumno no encontrado."}), 404
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500


def agregar_a_excel(id, num_lista, nombres, apellidos, codigo, fecha, hora):
    # Nombre del archivo Excel
    archivo_excel = "lista_asistencias.xlsx"

    try:
        # Intentar cargar el archivo existente, si no existe, crearlo
        try:
            workbook = openpyxl.load_workbook(archivo_excel)
            hoja = workbook.active
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            hoja = workbook.active
            # Crear encabezados si el archivo no existía
            hoja.append(["ID", "Número de Lista", "Nombres", "Apellidos", "Código", "Fecha", "Hora"])

        # Agregar la nueva fila con los datos de asistencia
        hoja.append([id, num_lista, nombres, apellidos, codigo, fecha, hora])

        # Guardar el archivo Excel
        workbook.save(archivo_excel)
    except Exception as e:
        print(f"Error al escribir en el archivo Excel: {str(e)}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
