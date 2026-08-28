from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# Clave para proteger la sesión
app.secret_key = "biblioteca-clave-123"

# Credenciales 
USUARIO = "datos"
CONTRASENA = "datos123"


# base de datos
def crear_base_datos():

    conexion = sqlite3.connect("biblioteca.db")

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            año INTEGER NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


crear_base_datos()

# login
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        if usuario == USUARIO and contraseña == CONTRASENA:

            session["logueado"] = True

            return redirect("/libros")

        return "Usuario o contraseña incorrectos"

    return render_template("login.html")


# libros
@app.route("/libros")
def libros():

    if "logueado" not in session:
        return redirect("/")

    conexion = sqlite3.connect("biblioteca.db")

    libros = conexion.execute(
        "SELECT * FROM libros"
    ).fetchall()

    conexion.close()

    return render_template(
        "libros.html",
        libros=libros
    )

# agregar
@app.route("/agregar", methods=["POST"])
def agregar():

    if "logueado" not in session:
        return redirect("/")

    titulo = request.form["titulo"]
    autor = request.form["autor"]
    año = request.form["año"]

    if titulo == "" or autor == "" or año == "":
        return "Todos los campos son obligatorios"

    conexion = sqlite3.connect("biblioteca.db")

    conexion.execute(
        """
        INSERT INTO libros
        (titulo, autor, año)
        VALUES (?, ?, ?)
        """,
        (titulo, autor, año)
    )

    conexion.commit()
    conexion.close()

    return redirect("/libros")

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):

    if "logueado" not in session:
        return redirect("/")

    titulo = request.form["titulo"]
    autor = request.form["autor"]
    año = request.form["año"]

    if titulo == "" or autor == "" or año == "":
        return "Todos los campos son obligatorios"

    conexion = sqlite3.connect("biblioteca.db")

    conexion.execute(
        """
        UPDATE libros
        SET titulo = ?, autor = ?, año = ?
        WHERE id = ?
        """,
        (titulo, autor, año, id)
    )

    conexion.commit()
    conexion.close()

    return redirect("/libros")

# eliminar
@app.route("/eliminar/<int:id>")
def eliminar(id):

    if "logueado" not in session:
        return redirect("/")

    conexion = sqlite3.connect("biblioteca.db")

    conexion.execute(
        "DELETE FROM libros WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect("/libros")

# cerrar sesion
@app.route("/salir")
def salir():

    session.clear()

    return redirect("/")

# ejecutar
if __name__ == "__main__":
    app.run()