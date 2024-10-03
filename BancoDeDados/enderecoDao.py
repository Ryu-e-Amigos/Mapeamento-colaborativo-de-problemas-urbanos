from BancoDeDados import connection

newConnection = connection.create_server_connection('localhost', 'root')

class endereco():
    def salvarNovo(self, rua: str, cidade: str, nmr: int, comp: str):
        print('Salvando...')
        insert_endereco_query = """
        INSERT INTO banco.endereco (rua, cidade, numero, complemento) 
        VALUES (%s, %s, %s, %s)
        """
        cursor = newConnection.cursor()
        cursor.execute(insert_endereco_query, (rua, cidade, nmr, comp))
        newConnection.commit()  # commitar a transação
        print('OK')
        return cursor.lastrowid  # Pega o ID do endereço recém-criado