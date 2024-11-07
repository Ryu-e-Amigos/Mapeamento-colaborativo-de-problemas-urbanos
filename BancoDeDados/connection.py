import mysql.connector
from mysql.connector import Error
import pandas as pd

db = "projdsin"
pw = ''
#------------------------------------------------------------------------
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database conectado com sucesso")
    except Error as err:
        print(f"Error: '{err}'")

    return connection 

#------------------------------------------------------------------------

connection = create_server_connection('localhost', 'root', pw)

#------------------------------------------------------------------------

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database criado com sucesso")
    except Error as err:
        print("Database já existe")

create_database_query = "CREATE DATABASE projdsin"

#------------------------------------------------------------------------

create_database(connection, create_database_query)

#------------------------------------------------------------------------

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database conectado com sucesso")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
#------------------------------------------------------------------------

connection = create_db_connection("localhost", "root", pw, db) # Connect to the Database

#------------------------------------------------------------------------
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
#------------------------------------------------------------------------

# execute_query(connection, create_teacher_table) # Execute our defined query

#------------------------------------------------------------------------

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#------------------------------------------------------------------------

#------------------------------------------------------------------------

# TABELAS
#------------------------------------------------------------------------
# USUARIO
create_usuario_table = """
    CREATE TABLE usuario (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        login VARCHAR(40) NOT NULL,
        senha VARCHAR(40) NOT NULL
    );
    """
#------------------------------------------------------------------------
# ENDERECO
create_endereco_table = """
    CREATE TABLE endereco (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        latitude DECIMAL(10, 8) NOT NULL,
        longitude DECIMAL(11, 8) NOT NULL,
        rua VARCHAR(40) NOT NULL,
        cidade VARCHAR(40) NOT NULL,
        numero INT,
        complemento VARCHAR(40)
    );
    """
#------------------------------------------------------------------------
# REPORT
create_report_table = """
    CREATE TABLE report (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        situacao INT NOT NULL,
        foto VARCHAR(255),
        endereco_id INT,
        FOREIGN KEY (endereco_id) REFERENCES endereco(Id)
    );
    """
#------------------------------------------------------------------------
# TABELA DE RELACIONAMENTO: USUARIO_REPORT
create_usuario_report_table = """
    CREATE TABLE usuario_report (
        usuario_id INT,
        report_id INT,
        PRIMARY KEY (usuario_id, report_id),
        FOREIGN KEY (usuario_id) REFERENCES usuario(Id),
        FOREIGN KEY (report_id) REFERENCES report(Id)
    );
    """
#------------------------------------------------------------------------

execute_query(connection, create_usuario_table)

execute_query(connection, create_endereco_table) # Execute our defined query

execute_query(connection, create_report_table) # Execute our defined query

execute_query(connection, create_usuario_report_table) # Execute our defined query

#------------------------------------------------------------------------

# cursor.execute("INSERT INTO clientes (nome, email) VALUES ('João', 'joao@email.com')")


# exemplo
# cursor = db.cursor()
# comando_sql = "INSERT INTO filmes (nome, gênero) VALUES (%s, %s)"
# dados = ("2001: A Space Odyssey", "Science Fiction")
# cursor.execute(comando_sql, dados)
# db.commit()
# print(cursor.rowcount, "registro inserido") # 1 registro inserido

def mostrandoReports():
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT r.situacao, e.latitude, e.longitude 
            FROM projdsin.report r
            INNER JOIN projdsin.endereco e
            ON e.Id = r.endereco_id;
        """
    )

    colunas = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=colunas)
    cursor.close()

    return df

def buscaReports():
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT rua, cidade, numero, complemento
            FROM endereco
            ORDER BY rua;
        """
    )

    colunas = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=colunas)
    cursor.close()

    return df