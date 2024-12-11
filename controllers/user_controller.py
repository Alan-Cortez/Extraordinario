from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import UserModel
import pusher

user_routes = Blueprint("user_routes", __name__)

# Instancia del modelo
user_model = UserModel()

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1767934',
    key='ffa9ea426828188c22c1',
    secret='628348e447718a9eec1f',
    cluster='us2',
    ssl=True
)

@user_routes.route("/")
def index():
    # Obtener todos los usuarios desde el modelo
    usuarios = user_model.obtener_usuarios()
    return render_template("app.html", usuarios=usuarios)

@user_routes.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    # Obtener datos del formulario
    usuario = request.form.get("txtUsuario")
    contrasena = request.form.get("txtContrasena")

    if usuario and contrasena:
        # Guardar el usuario en la base de datos
        user_model.guardar_usuario(usuario, contrasena)

        # Notificar mediante Pusher
        try:
            pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
                "usuario": usuario,
                "contrasena": contrasena
            })
        except Exception as e:
            flash("Hubo un error al enviar la notificación en tiempo real", "error")

        flash("Usuario creado exitosamente", "success")
    else:
        flash("Debe llenar todos los campos", "error")

    return redirect(url_for("user_routes.index"))

@user_routes.route("/usuarios/actualizar/<int:id>", methods=["POST"])
def usuarios_actualizar(id):
    # Obtener datos del formulario
    usuario = request.form.get("txtUsuario")
    contrasena = request.form.get("txtContrasena")

    if usuario and contrasena:
        # Actualizar el usuario en la base de datos
        user_model.actualizar_usuario(id, usuario, contrasena)
        flash("Usuario actualizado exitosamente", "success")
    else:
        flash("Debe llenar todos los campos", "error")

    return redirect(url_for("user_routes.index"))

@user_routes.route("/usuarios/eliminar/<int:id>", methods=["POST"])
def usuarios_eliminar(id):
    # Eliminar el usuario de la base de datos
    user_model.eliminar_usuario(id)

    # Emitir un evento de Pusher para notificar la eliminación
    try:
        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
            "id_usuario": id
        })
    except Exception as e:
        flash("Hubo un error al enviar la notificación en tiempo real", "error")

    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for("user_routes.index"))

