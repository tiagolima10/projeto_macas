import mysql.connector
from mysql.connector import Error
from datetime import datetime
from models import Paciente, Maqueiro, Tarefa, SolicitacaoTransporte, Incidente

class Database:
    """
    Classe Database para gerenciar a conexão e operações com o banco de dados MySQL.

    Attributes:
        connection (mysql.connector.connection_cext.CMySQLConnection): Conexão com o banco de dados.
        cursor (mysql.connector.cursor_cext.CMySQLCursor): Cursor para executar comandos SQL.
    """

    def __init__(self, host, user, password, database):
        """
        Inicializa a conexão com o banco de dados.

        Args:
            host (str): Endereço do servidor do banco de dados.
            user (str): Nome de usuário para autenticação no banco de dados.
            password (str): Senha para autenticação no banco de dados.
            database (str): Nome do banco de dados a ser utilizado.
        """
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            print("Conexão com o banco de dados estabelecida.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def create_tables(self):
        """
        Cria as tabelas do sistema no banco de dados, se ainda não existirem.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pacientes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100),
            cpf VARCHAR(11) UNIQUE,
            localizacao VARCHAR(100),
            condicao VARCHAR(100),
            urgencia ENUM('Emergência', 'Alta', 'Média', 'Baixa'),
            transporte ENUM('Aguardando transporte', 'Em transporte', 'Chegou ao destino') DEFAULT 'Aguardando transporte',
            inicio_transporte DATETIME
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Maqueiros (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100),
            coren VARCHAR(12) UNIQUE,
            data_nascimento DATE,
            sexo ENUM('M', 'F'),
            login VARCHAR(50) UNIQUE,
            senha VARCHAR(100)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tarefas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            descricao VARCHAR(255),
            prioridade VARCHAR(50),
            status VARCHAR(50),
            paciente_id INT,
            localizacao VARCHAR(100),
            maqueiro_id INT,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY (maqueiro_id) REFERENCES Maqueiros(id)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Incidentes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            descricao VARCHAR(255),
            maqueiro_id INT,
            paciente_id INT,
            data_hora DATETIME,
            FOREIGN KEY (maqueiro_id) REFERENCES Maqueiros(id),
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS SolicitacoesTransporte (
            id INT PRIMARY KEY AUTO_INCREMENT,
            descricao VARCHAR(255),
            paciente_id INT,
            status VARCHAR(50),
            maqueiro_id INT,
            data_hora DATETIME,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY (maqueiro_id) REFERENCES Maqueiros(id)
        )""")

        self.connection.commit()

    def insert_paciente(self, paciente):
        """
        Insere um novo paciente na tabela de Pacientes.

        Args:
            paciente (Paciente): Objeto paciente a ser inserido no banco de dados.

        Returns:
            int: ID do paciente inserido, ou None se ocorrer um erro.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Pacientes (nome, cpf, localizacao, condicao, urgencia, transporte) VALUES (%s, %s, %s, %s, %s, %s)",
                (paciente.nome, paciente.cpf, paciente.localizacao, paciente.condicao, paciente.urgencia, paciente.transporte)
            )
            self.connection.commit()
            paciente_id = self.cursor.lastrowid
            return paciente_id
        except Error as e:
            print(f"Erro ao inserir paciente no banco de dados: {e}")
            return None

    def insert_tarefa(self, tarefa):
        """
        Insere uma nova tarefa na tabela de Tarefas.

        Args:
            tarefa (Tarefa): Objeto tarefa a ser inserido no banco de dados.

        Returns:
            int: ID da tarefa inserida, ou None se ocorrer um erro.
        """
        try:
            self.cursor.execute("INSERT INTO Tarefas (descricao, prioridade, status, paciente_id, localizacao, maqueiro_id) VALUES (%s, %s, %s, %s, %s, %s)",
                                (tarefa.descricao, tarefa.prioridade, tarefa.status, tarefa.paciente.id, tarefa.localizacao, tarefa.maqueiro.id if tarefa.maqueiro else None))
            self.connection.commit()
            tarefa_id = self.cursor.lastrowid
            return tarefa_id
        except Error as e:
            print(f"Erro ao inserir tarefa no banco de dados: {e}")
            return None

    def update_tarefa_status(self, tarefa_id, status):
        """
        Atualiza o status de uma tarefa na tabela de Tarefas.

        Args:
            tarefa_id (int): ID da tarefa a ser atualizada.
            status (str): Novo status da tarefa.
        """
        try:
            self.cursor.execute("UPDATE Tarefas SET status = %s WHERE id = %s", (status, tarefa_id))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao atualizar status da tarefa no banco de dados: {e}")

    def insert_incidente(self, incidente):
        """
        Insere um novo incidente na tabela de Incidentes.

        Args:
            incidente (Incidente): Objeto incidente a ser inserido no banco de dados.
        """
        try:
            self.cursor.execute("INSERT INTO Incidentes (descricao, maqueiro_id, paciente_id, data_hora) VALUES (%s, %s, %s, %s)",
                                (incidente.descricao, incidente.maqueiro.id, incidente.paciente.id, incidente.data_hora))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao inserir incidente no banco de dados: {e}")

    def listar_incidentes(self):
        """
        Lista todos os incidentes no banco de dados, ordenados do mais recente para o mais antigo.

        Returns:
            list: Lista de objetos Incidente.
        """
        try:
            self.cursor.execute("SELECT id, descricao, maqueiro_id, paciente_id, data_hora FROM Incidentes ORDER BY data_hora DESC")
            result = self.cursor.fetchall()
            incidentes = []
            for row in result:
                maqueiro = self.buscar_maqueiro_por_id(row[2])
                paciente = self.buscar_paciente_por_id(row[3])
                incidente = Incidente(row[0], row[1], maqueiro, paciente, row[4])
                incidentes.append(incidente)
            return incidentes
        except Error as e:
            print(f"Erro ao listar incidentes no banco de dados: {e}")
            return []

    def insert_solicitacao_transporte(self, solicitacao):
        """
        Insere uma nova solicitação de transporte na tabela de SolicitacoesTransporte.

        Args:
            solicitacao (SolicitacaoTransporte): Objeto solicitação de transporte a ser inserido no banco de dados.

        Returns:
            int: ID da solicitação inserida, ou None se ocorrer um erro.
        """
        try:
            self.cursor.execute("INSERT INTO SolicitacoesTransporte (descricao, paciente_id, status, maqueiro_id, data_hora) VALUES (%s, %s, %s, %s, %s)",
                                (solicitacao.descricao, solicitacao.paciente.id, solicitacao.status, solicitacao.maqueiro.id if solicitacao.maqueiro else None, solicitacao.data_hora))
            self.connection.commit()
            solicitacao_id = self.cursor.lastrowid
            return solicitacao_id
        except Error as e:
            print(f"Erro ao inserir solicitação de transporte no banco de dados: {e}")
            return None

    def buscar_paciente_por_cpf(self, cpf):
        """
        Busca um paciente no banco de dados pelo CPF.

        Args:
            cpf (str): CPF do paciente a ser buscado.

        Returns:
            Paciente: Objeto paciente encontrado, ou None se não encontrado.
        """
        self.cursor.execute("SELECT id, nome, cpf, localizacao, condicao, transporte FROM Pacientes WHERE cpf = %s", (cpf,))
        result = self.cursor.fetchone()
        if result:
            paciente = Paciente(result[1], result[2], result[3], result[4], result[5])
            paciente.definir_id(result[0])
            return paciente
        return None

    def buscar_maqueiro_por_login(self, login):
        """
        Busca um maqueiro no banco de dados pelo login.

        Args:
            login (str): Login do maqueiro a ser buscado.

        Returns:
            Maqueiro: Objeto maqueiro encontrado, ou None se não encontrado.
        """
        self.cursor.execute("SELECT id, nome, coren, data_nascimento, sexo, login, senha FROM Maqueiros WHERE login = %s", (login,))
        result = self.cursor.fetchone()
        if result:
            maqueiro = Maqueiro(result[0], result[1], result[2], result[3], result[4])
            maqueiro.login = result[5]
            maqueiro.senha = result[6]
            return maqueiro
        return None

    def listar_tarefas_pendentes(self):
        """
        Lista todas as tarefas pendentes no banco de dados.

        Returns:
            list: Lista de objetos Tarefa com o status pendente.
        """
        self.cursor.execute("SELECT id, descricao, prioridade, paciente_id, localizacao, maqueiro_id FROM Tarefas WHERE status = 'pendente'")
        result = self.cursor.fetchall()
        tarefas = []
        for row in result:
            paciente = self.buscar_paciente_por_id(row[3])
            maqueiro = self.buscar_maqueiro_por_id(row[5]) if row[5] else None
            tarefa = Tarefa(row[0], row[1], row[2], paciente, row[4], maqueiro)
            tarefas.append(tarefa)
        return tarefas

    def buscar_paciente_por_id(self, paciente_id):
        """
        Busca um paciente no banco de dados pelo ID.

        Args:
            paciente_id (int): ID do paciente a ser buscado.

        Returns:
            Paciente: Objeto paciente encontrado, ou None se não encontrado.
        """
        self.cursor.execute("SELECT id, nome, cpf, localizacao, condicao, transporte FROM Pacientes WHERE id = %s", (paciente_id,))
        result = self.cursor.fetchone()
        if result:
            paciente = Paciente(result[1], result[2], result[3], result[4], result[5])
            paciente.definir_id(result[0])
            return paciente
        return None

    def buscar_maqueiro_por_id(self, maqueiro_id):
        """
        Busca um maqueiro no banco de dados pelo ID.

        Args:
            maqueiro_id (int): ID do maqueiro a ser buscado.

        Returns:
            Maqueiro: Objeto maqueiro encontrado, ou None se não encontrado.
        """
        self.cursor.execute("SELECT id, nome, coren, data_nascimento, sexo, login, senha FROM Maqueiros WHERE id = %s", (maqueiro_id,))
        result = self.cursor.fetchone()
        if result:
            maqueiro = Maqueiro(result[0], result[1], result[2], result[3], result[4])
            maqueiro.login = result[5]
            maqueiro.senha = result[6]
            return maqueiro
        return None

    def listar_solicitacoes_pendentes(self):
        """
        Lista todas as solicitações de transporte pendentes ou recusadas no banco de dados.

        Returns:
            list: Lista de objetos SolicitacaoTransporte com o status pendente ou recusada.
        """
        try:
            self.cursor.execute("SELECT id, descricao, paciente_id, status, maqueiro_id, data_hora FROM SolicitacoesTransporte WHERE status IN ('pendente', 'recusada')")
            result = self.cursor.fetchall()
            solicitacoes = []
            for row in result:
                paciente = self.buscar_paciente_por_id(row[2])
                maqueiro = self.buscar_maqueiro_por_id(row[4]) if row[4] else None
                solicitacao = SolicitacaoTransporte(row[0], row[1], paciente, row[5], maqueiro)
                solicitacao.status = row[3]  # Atribuir o status corretamente
                solicitacoes.append(solicitacao)
            return solicitacoes
        except Error as e:
            print(f"Erro ao listar solicitações pendentes no banco de dados: {e}")
            return []

    def update_solicitacao_status(self, solicitacao_id, status, maqueiro_id):
        """
        Atualiza o status de uma solicitação de transporte no banco de dados.

        Args:
            solicitacao_id (int): ID da solicitação a ser atualizada.
            status (str): Novo status da solicitação.
            maqueiro_id (int): ID do maqueiro responsável.
        """
        try:
            self.cursor.execute("UPDATE SolicitacoesTransporte SET status = %s, maqueiro_id = %s WHERE id = %s", (status, maqueiro_id, solicitacao_id))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao atualizar status da solicitação de transporte no banco de dados: {e}")

    def listar_pacientes(self):
        """
        Lista todos os pacientes no banco de dados, ordenados por urgência.

        Returns:
            list: Lista de objetos Paciente.
        """
        self.cursor.execute("SELECT id, nome, cpf, localizacao, condicao, urgencia, transporte FROM Pacientes ORDER BY FIELD(urgencia, 'Emergência', 'Alta', 'Média', 'Baixa')")
        result = self.cursor.fetchall()
        pacientes = []
        for row in result:
            paciente = Paciente(row[1], row[2], row[3], row[4], row[6])
            paciente.definir_id(row[0])
            paciente.urgencia = row[5]
            pacientes.append(paciente)
        return pacientes
    
    def iniciar_transporte_paciente(self, paciente_id):
        """
        Inicia o transporte de um paciente, atualizando a condição e registrando o início do transporte.

        Args:
            paciente_id (int): ID do paciente a ser transportado.
        """
        try:
            self.cursor.execute("UPDATE Pacientes SET condicao = 'Em transporte', inicio_transporte = %s WHERE id = %s",
            (datetime.now(), paciente_id))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao iniciar transporte do paciente: {e}")

    def atualizar_status_transporte(self):
        """
        Atualiza o status de transporte dos pacientes em relação ao tempo de transporte.
        """
        try:
            self.cursor.execute("SELECT id, inicio_transporte FROM Pacientes WHERE condicao = 'Em transporte'")
            pacientes_em_transporte = self.cursor.fetchall()
            for paciente_id, inicio_transporte in pacientes_em_transporte:
                tempo_em_transporte = datetime.now() - inicio_transporte
                if tempo_em_transporte.total_seconds() > 3600:  # Exemplo: 1 hora em segundos
                    self.cursor.execute("UPDATE Pacientes SET transporte = 'Chegou ao destino' WHERE id = %s", (paciente_id,))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao atualizar status de transporte: {e}")

    def concluir_transporte_paciente(self, paciente_id):
        """
        Conclui o transporte de um paciente, atualizando os status.

        Args:
            paciente_id (int): ID do paciente cujo transporte foi concluído.
        """
        try:
            # Atualizar o status de transporte do paciente
            self.cursor.execute("UPDATE Pacientes SET transporte = 'Chegou ao destino', inicio_transporte = NULL WHERE id = %s", (paciente_id,))
            self.connection.commit()

            # Atualizar o status das solicitações de transporte associadas para "concluído"
            self.cursor.execute("UPDATE SolicitacoesTransporte SET status = 'concluído' WHERE paciente_id = %s", (paciente_id,))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao concluir transporte do paciente: {e}")

    def atualizar_transporte_paciente(self, paciente_id, status_transporte):
        """
        Atualiza o status de transporte de um paciente.

        Args:
            paciente_id (int): ID do paciente a ser atualizado.
            status_transporte (str): Novo status de transporte do paciente.
        """
        try:
            sql = "UPDATE Pacientes SET transporte = %s WHERE id = %s"
            values = (status_transporte, paciente_id)
            self.cursor.execute(sql, values)
            self.connection.commit()
        except Error as e:
            print(f"Erro ao atualizar transporte do paciente: {e}")

    def atualizar_localizacao_paciente(self, paciente_id, nova_localizacao):
        """
        Atualiza a localização de um paciente no banco de dados.

        Args:
            paciente_id (int): ID do paciente a ser atualizado.
            nova_localizacao (str): Nova localização do paciente.
        """
        try:
            self.cursor.execute("UPDATE Pacientes SET localizacao = %s WHERE id = %s", (nova_localizacao, paciente_id))
            self.connection.commit()
        except Error as e:
            print(f"Erro ao atualizar localização do paciente: {e}")
