from BancoDeDados import connection

newConnection = connection.create_server_connection('localhost', 'root', connection.pw)

class endereco():
    def salvarNovo(self, lat: float, lon: float, comp: str):
        print('Salvando...')
        insert_endereco_query = """
        INSERT INTO banco.endereco (latitude, longitude, complemento) 
        VALUES (%s, %s, %s)
        """
        cursor = newConnection.cursor()
        cursor.execute(insert_endereco_query, (lat, lon, comp))
        newConnection.commit()  # commitar a transação
        
        print('OK')
        return cursor.lastrowid  # Pega o ID do endereço recém-criado