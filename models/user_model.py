import mysql.connector
from mysql.connector import Error

class UserModel:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="185.232.14.52",
                database="u760464709_tst_sep",
                user="u760464709_tst_sep_usr",
                password="dJ0CIAFF="
            )
            if self.con.is_connected():
                print("Conexión a la base de datos exitosa")
        except Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            self.con = None
    
    def verificar_conexion(self):
        if not self.con or not self.con.is_connected():
            try:
                self.con.reconnect(attempts=3, delay=5)
            except Error as e:
                print(f"Error al intentar reconectar: {e}")
                self.con = None

    def obtener_usuarios(self):
        if not self.con or not self.con.is_connected():
            return []

        self.verificar_conexion()
        try:
            with self.con.cursor() as cursor:
                cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
                return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def guardar_usuario(self, usuario, contrasena):
        if not self.con or not self.con.is_connected():
            return

        self.verificar_conexion()
        try:
            with self.con.cursor() as cursor:
                sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
                cursor.execute(sql, (usuario, contrasena))
                self.con.commit()
                print("Usuario guardado correctamente")
        except Error as e:
            print(f"Error al guardar usuario: {e}")

    def actualizar_usuario(self, id, usuario, contrasena):
        if not self.con or not self.con.is_connected():
            return

        self.verificar_conexion()
        try:
            with self.con.cursor() as cursor:
                sql = "UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s"
                cursor.execute(sql, (usuario, contrasena, id))
                self.con.commit()
                print("Usuario actualizado correctamente")
        except Error as e:
            print(f"Error al actualizar usuario: {e}")

    def eliminar_usuario(self, id):
        if not self.con or not self.con.is_connected():
            return

        self.verificar_conexion()
        try:
            with self.con.cursor() as cursor:
                sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
                cursor.execute(sql, (id,))
                self.con.commit()
                print("Usuario eliminado correctamente")
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
