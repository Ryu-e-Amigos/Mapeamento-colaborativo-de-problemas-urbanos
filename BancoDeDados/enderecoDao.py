from BancoDeDados import connection

newConnection = connection.create_server_connection('localhost', 'root', connection.pw)

class endereco():
    def salvarNovo(self, lat: float, lon: float, rua: str, cid: str, num: int, comp: str):
        print('Salvando...')
        insert_endereco_query = """
        INSERT INTO projdsin.endereco (latitude, longitude, rua, cidade, numero, complemento) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = newConnection.cursor()
        cursor.execute(insert_endereco_query, (lat, lon, rua, cid, num, comp))
        newConnection.commit()  # commitar a transação
        
        print('OK')
        return cursor.lastrowid  # Pega o ID do endereço recém-criado