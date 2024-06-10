import unittest
import sys
import os
from unittest.mock import MagicMock
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from models import Paciente, Maqueiro, Tarefa, Incidente, SolicitacaoTransporte

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para cada teste
        self.db = Database('localhost', 'root', '', 'projeto_macas')
        self.db.cursor = MagicMock()
        self.db.connection = MagicMock()

    def test_insert_paciente(self):
        # Teste de inserção de paciente
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        self.db.insert_paciente(paciente)
        self.db.cursor.execute.assert_called_once_with(
            "INSERT INTO Pacientes (nome, cpf, localizacao, condicao, urgencia, transporte) VALUES (%s, %s, %s, %s, %s, %s)",
            (paciente.nome, paciente.cpf, paciente.localizacao, paciente.condicao, paciente.urgencia, paciente.transporte)
        )
        self.db.connection.commit.assert_called_once()

    def test_insert_tarefa(self):
        # Teste de inserção de tarefa
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        tarefa = Tarefa(1, "Mover paciente", "Alta", paciente, "Sala 101", maqueiro)
        self.db.insert_tarefa(tarefa)
        self.db.cursor.execute.assert_called_once_with(
            "INSERT INTO Tarefas (descricao, prioridade, status, paciente_id, localizacao, maqueiro_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (tarefa.descricao, tarefa.prioridade, tarefa.status, tarefa.paciente.id, tarefa.localizacao, tarefa.maqueiro.id)
        )
        self.db.connection.commit.assert_called_once()

    def test_buscar_paciente_por_cpf(self):
        # Teste de busca de paciente por CPF
        cpf = "12345678901"
        self.db.cursor.fetchone.return_value = (1, "João Silva", cpf, "Sala 101", "Estável", "Aguardando transporte")
        paciente = self.db.buscar_paciente_por_cpf(cpf)
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nome, "João Silva")
        self.db.cursor.execute.assert_called_once_with(
            "SELECT id, nome, cpf, localizacao, condicao, transporte FROM Pacientes WHERE cpf = %s",
            (cpf,)
        )

    def test_insert_incidente(self):
        # Teste de inserção de incidente
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        incidente = Incidente(None, "Queda do paciente", maqueiro, paciente, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.db.insert_incidente(incidente)
        self.db.cursor.execute.assert_called_once_with(
            "INSERT INTO Incidentes (descricao, maqueiro_id, paciente_id, data_hora) VALUES (%s, %s, %s, %s)",
            (incidente.descricao, incidente.maqueiro.id, incidente.paciente.id, incidente.data_hora)
        )
        self.db.connection.commit.assert_called_once()

    def test_listar_incidentes(self):
        # Teste de listagem de incidentes
        self.db.cursor.fetchall.return_value = [
            (1, "Queda do paciente", 1, 1, "2023-06-10 14:30:00")
        ]
        self.db.buscar_maqueiro_por_id = MagicMock(return_value=Maqueiro(1, "Carlos", "123456", "1980-01-01", "M"))
        self.db.buscar_paciente_por_id = MagicMock(return_value=Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta"))

        incidentes = self.db.listar_incidentes()
        self.assertEqual(len(incidentes), 1)
        self.assertEqual(incidentes[0].descricao, "Queda do paciente")
        self.assertEqual(incidentes[0].maqueiro.nome, "Carlos")
        self.assertEqual(incidentes[0].paciente.nome, "João Silva")
        self.db.cursor.execute.assert_called_once_with(
            "SELECT id, descricao, maqueiro_id, paciente_id, data_hora FROM Incidentes ORDER BY data_hora DESC"
        )

if __name__ == '__main__':
    unittest.main()
