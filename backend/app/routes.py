from flask import Blueprint, jsonify, request
from . import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return "Hello, World!"

""" this is for login interactions """

@main.route('/users')
def get_users():
	try:
		cur = mysql.connection.cursor()
		cur.execute("SELECT u.nombre, apellido, correo, contraseña, r.nombre FROM usuarios as u INNER JOIN roles as r WHERE u.id_rol = r.id")
		rv = cur.fetchall()
		
		payload = []
		for i in rv:
			payload.append({"name": i[0], "lastName": i[1], "email": i[2], "password": i[3],"role": i[4]})
			
		return jsonify(payload)
	except Exception as e:
		print(e)
		return jsonify({"msg": e})

""" this is for the postulation interactions """

@main.route('/postulations/<string:status>')
def get_postulaciones(status):
	try:
		cur = mysql.connection.cursor()
		cur.execute(""" 
			SELECT CONCAT(p.nombre, " ", apellido) AS nombre, correo, c.nombre as carrera, cuatrimestre, promedio, tipo_monitoria, COALESCE(m.nombre, a.nombre) as area 
			FROM postulaciones p 
			INNER JOIN carreras c ON p.id_carrera = c.id
			LEFT JOIN areas_administracion a ON p.id_area_administracion = a.id 
			LEFT JOIN materias m ON p.id_materia = m.id
			WHERE p.estado = %s """, (status,))
		
		rv = cur.fetchall()

		payload = []

		for i in rv: 
			payload.append({"nombre": i[0], "correo": i[1], "carrera": i[2], "cuatrimestre": i[3], "promedio": i[4], "tipo": i[5], "area": i[6]})
			
		return jsonify(payload)
	except Exception as e:
		print(e)
		return jsonify({"msg": e})

@main.route('/add_postulacion', methods=['POST'])
def add_postulacion():
	try:
		data = request.get_json()
		username = data['name']
		last_name = data['lname']
		email = data['email']
		type_apply = data["career"]
		average = data["avg"]
		cuatrimestre = data["cicle"]
		id_materia = data["id_materia"]
		id_career = data['carrer']
		id_area = data["apply_admin"]

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO postulaciones(nombre, apellido, correo, tipo_monitoria, estado, promedio, cuatrimestre, id_materia, id_carrera, id_area_administracion) VALUES(%s, %s , %s, %s, %s, %s, %s, %s, %s, %s)", (username, last_name, email, type_apply, 'en espera', average, cuatrimestre, id_materia, id_career, id_area))
		""" estado solo puede tener 3 estados: "en espera", "aceptada", "rechazada" """
		mysql.connection.commit()
		return jsonify({'message': 'User added successfully'})
	
	except Exception as e:
		print(e)
		return jsonify({"msg": e})

@main.route('/setPostulationStatus/<string:email>/<string:status>', methods=["PUT"])
def setPostulationStatus(email, status):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE postulaciones
            SET estado = %s
            WHERE correo = %s
        """, (status, email))
        
        mysql.connection.commit()
        return jsonify({"msg": "User updated successfully"})
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500


""" this is for the admin interactions """

@main.route('/users_admin')
def get_users_admin():
	try:
		cur = mysql.connection.cursor()
		cur.execute("SELECT u.id, u.nombre, apellido, correo, contraseña, r.nombre FROM usuarios as u INNER JOIN roles as r WHERE u.id_rol = r.id ORDER BY u.id ASC")
		rv = cur.fetchall()
		
		payload = []
		for i in rv:
			payload.append({
				"id": i[0], 
				"nombre": i[1], 
				"apellido": i[2], 
				"correo": i[3],
				"contraseña": i[4], 
				"rol": i[5]
			})
			
		return jsonify(payload)
	except Exception as e:
		print(e)
		return jsonify({"msg": e})

@main.route('/add_user', methods=["POST"])
def add_user():
	try:
		data = request.get_json()
		name = data["name"]
		last_name = data["lname"]
		email = data["email"]
		password = data["pass"]
		role = data["role"]

		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
		res = cur.fetchone()

		if res:
			return jsonify({"msg": "El usuario ya existe"})

		cur.execute("INSERT INTO usuarios(nombre, apellido, correo, contraseña, id_rol) VALUES(%s, %s, %s, %s, %s)", (name, last_name, email, password, role))
		mysql.connection.commit()
		return jsonify({'message': 'User added successfully'})
	
	except Exception as e:
		print(e)
		return jsonify({"msg": e})
	

@main.route('/deleteUser/<int:id>', methods=["DELETE"])
def delete_user(id):
	try:
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM usuarios WHERE id = %s", (id, ))
		mysql.connection.commit()
		return jsonify({"msg": "Usuario eliminado con exito"})
	except Exception as e:
		print(e)
		return jsonify({"msg": "Error al eliminar usuario"})
	

@main.route('/editUser/<int:id>', methods=["PUT"])
def edit_user(id):
	try:
		data = request.get_json()
		name = data["name"]
		last_name = data["lname"]
		email = data["email"]
		password = data["pass"]
		role = data["role"]
		
		cur = mysql.connection.cursor()
		cur.execute("UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, contraseña = %s, id_rol = %s WHERE id = %s ", (name, last_name, email, password, role, id))
		mysql.connection.commit()
		return jsonify({"msg": "Succesfully edited"})

	except Exception as e:
		print(e)
		return jsonify({"msg": "Error while trying to edit the current user"})