import mysql.connector

conexao = mysql.connector.connect(
  host='localhost',
  user='root',
  password='Senha-1234',
)

cursor = conexao.cursor()
cursor.execute("SHOW DATABASES LIKE 'banco'")

resultado = cursor.fetchone()

if resultado:
    print("O banco de dados já existe.")
else:
    cursor.execute("CREATE DATABASE banco")

if not resultado:
    cursor.execute("CREATE DATABASE banco")


# cursor.execute("INSERT INTO clientes (nome, email) VALUES ('João', 'joao@email.com')")


# exemplo
# cursor = db.cursor()
# comando_sql = "INSERT INTO filmes (nome, gênero) VALUES (%s, %s)"
# dados = ("2001: A Space Odyssey", "Science Fiction")
# cursor.execute(comando_sql, dados)
# db.commit()
# print(cursor.rowcount, "registro inserido") # 1 registro inserido