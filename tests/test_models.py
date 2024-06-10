import sys
import os
import unittest
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Usuario, Maqueiro, Tarefa, Paciente, Incidente, SolicitacaoTransporte

class TestModels(unittest.TestCase):

    def test_usuario(self):
        usuario = Usuario(1, "Admin", "administrador")
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nome, "Admin")
        self.assertEqual(usuario.tipo, "administrador")

    def test_paciente(self):
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        self.assertEqual(paciente.nome, "João Silva")
        self.assertEqual(paciente.cpf, "12345678901")
        self.assertEqual(paciente.localizacao, "Sala 101")
        self.assertEqual(paciente.condicao, "Estável")
        self.assertEqual(paciente.transporte, "Aguardando transporte")
        self.assertEqual(paciente.urgencia, "Alta")

    def test_maqueiro(self):
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        self.assertEqual(maqueiro.id, 1)
        self.assertEqual(maqueiro.nome, "Carlos")
        self.assertEqual(maqueiro.coren, "123456")
        self.assertEqual(maqueiro.data_nascimento, "1980-01-01")
        self.assertEqual(maqueiro.sexo, "M")

    def test_tarefa(self):
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        tarefa = Tarefa(1, "Mover paciente", "Alta", paciente, "Sala 101", maqueiro)
        self.assertEqual(tarefa.id, 1)
        self.assertEqual(tarefa.descricao, "Mover paciente")
        self.assertEqual(tarefa.prioridade, "Alta")
        self.assertEqual(tarefa.paciente.nome, "João Silva")
        self.assertEqual(tarefa.maqueiro.nome, "Carlos")

    def test_incidente(self):
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        incidente = Incidente(1, "Queda de paciente", maqueiro, paciente, "2023-01-01 12:00:00")
        self.assertEqual(incidente.id, 1)
        self.assertEqual(incidente.descricao, "Queda de paciente")
        self.assertEqual(incidente.maqueiro.nome, "Carlos")
        self.assertEqual(incidente.paciente.nome, "João Silva")
        self.assertEqual(incidente.data_hora, "2023-01-01 12:00:00")

    def test_solicitacao_transporte(self):
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        maqueiro = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        solicitacao = SolicitacaoTransporte(1, "Transporte urgente", paciente, "2023-01-01 12:00:00", maqueiro)
        self.assertEqual(solicitacao.id, 1)
        self.assertEqual(solicitacao.descricao, "Transporte urgente")
        self.assertEqual(solicitacao.paciente.nome, "João Silva")
        self.assertEqual(solicitacao.maqueiro.nome, "Carlos")
        self.assertEqual(solicitacao.data_hora, "2023-01-01 12:00:00")

if __name__ == '__main__':
    unittest.main()
