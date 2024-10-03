from BancoDeDados import connection

newConnection = connection.create_server_connection('localhost', 'root')

class Report():
    def salvarNovo(self, corPin: int, endereco_id: int, usuario_id: int):
        insert_report_query = """
        INSERT INTO banco.report (situacao, endereco_id) 
        VALUES (%s, %s)
        """
        cursor = newConnection.cursor()
        cursor.execute(insert_report_query, (corPin, endereco_id))
        newConnection.commit()
        cursor.close()
        report_id = cursor.lastrowid  # Pega o ID do report recém-criado
        self._saveUsuarioReport(report_id, usuario_id)


    def _saveUsuarioReport(self, report_id: int, usuario_id: int):
        # Inserindo na tabela de relacionamento usuario_report
        insert_usuario_report_query = """
            INSERT INTO banco.usuario_report (usuario_id, report_id) 
            VALUES (%s, %s)
        """
        cursor = newConnection.cursor()
        cursor.execute(insert_usuario_report_query, (usuario_id, report_id))
        
        newConnection.commit()
        cursor.close()
