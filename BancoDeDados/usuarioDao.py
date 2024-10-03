from flask import flash, redirect, url_for
from BancoDeDados import connection

newConnection = connection.create_server_connection('localhost', 'root')

class Usuario():
    def salvarNovo(self, usuario: str, senha: str):
        cursor = newConnection.cursor()
        # Verifica se o usuário já existe no banco
        result = self._verificarSeUserExist(usuario)

        if result:
            flash("Nome de usuário já existe!")
            return redirect(url_for("cadastro"))
        
        # Insere o novo usuário
        insert_query = "INSERT INTO banco.usuario (login, senha) VALUES (%s, %s)"
        cursor.execute(insert_query, (usuario, senha))
        newConnection.commit()
        cursor.close()
        # return result
    
    def _verificarSeUserExist(self, usuario: str):
        query = "SELECT * FROM banco.usuario WHERE login = %s"
        cursor = newConnection.cursor()
        cursor.execute(query, (usuario,))
        return cursor.fetchone()
    
    def verificaLogin(self, usuario_login: str, senha_login: str):
        query = "SELECT * FROM banco.usuario WHERE login = %s AND senha = %s"
        cursor = newConnection.cursor()
        cursor.execute(query, (usuario_login, senha_login))
        result = cursor.fetchone()
        cursor.close()
        return result

    
