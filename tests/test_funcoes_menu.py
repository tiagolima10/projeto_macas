import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes_menu import (
    cadastrar_paciente,
    ver_status_pacientes,
    adicionar_tarefa,
    concluir_tarefa,
    listar_tarefas_pendentes,
    relatar_incidente,
    solicitar_transporte,
    ver_solicitacoes_transporte,
    aceitar_ou_recusar_solicitacao,
    exibir_detalhes_transporte
)
from models import Paciente, Maqueiro, Tarefa, Incidente, SolicitacaoTransporte
from validations import validar_cpf, obter_nivel_urgencia, obter_status_transporte

class TestFuncoesMenu(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.pacientes = []
        self.tarefas = []
        self.solicitacoes_transporte = []
        self.maqueiro_logado = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")

    @patch('funcoes_menu.obter_input', side_effect=["João Silva", "12345678901", "Sala 101", "Estável"])
    @patch('funcoes_menu.validar_cpf', return_value=True)
    @patch('funcoes_menu.obter_nivel_urgencia', return_value={'nivel': 'Alta'})
    @patch('funcoes_menu.obter_status_transporte', return_value='Aguardando transporte')
    @patch('tkinter.messagebox.showinfo')
    def test_cadastrar_paciente(self, mock_showinfo, mock_obter_status_transporte, mock_obter_nivel_urgencia, mock_validar_cpf, mock_obter_input):
        self.db.buscar_paciente_por_cpf.return_value = None
        self.db.insert_paciente.return_value = 1
        
        cadastrar_paciente(self.db, self.pacientes)
        
        self.db.insert_paciente.assert_called_once()
        mock_showinfo.assert_called_once_with("Sucesso", "Paciente João Silva cadastrado com sucesso.", parent=None)
        self.assertEqual(len(self.pacientes), 1)
        self.assertEqual(self.pacientes[0].nome, "João Silva")

    @patch('tkinter.Toplevel')
    @patch('tkinter.Canvas')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.Frame')
    def test_ver_status_pacientes(self, mock_frame, mock_scrollbar, mock_canvas, mock_toplevel):
        self.db.listar_pacientes.return_value = [
            Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        ]
        
        ver_status_pacientes(self.db)
        
        self.db.listar_pacientes.assert_called_once()
        mock_toplevel.assert_called_once()

    @patch('tkinter.messagebox.showinfo')
    def test_listar_tarefas_pendentes(self, mock_showinfo):
        tarefa = Tarefa(1, "Mover paciente", "Alta", Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta"), "Sala 101", self.maqueiro_logado)
        self.db.listar_tarefas_pendentes.return_value = [tarefa]
        
        listar_tarefas_pendentes(self.db)
        
        self.db.listar_tarefas_pendentes.assert_called_once()
        mock_showinfo.assert_called_once()

    @patch('funcoes_menu.obter_input', side_effect=["Queda do paciente", "12345678901"])
    @patch('funcoes_menu.validar_cpf', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    def test_relatar_incidente(self, mock_showinfo, mock_validar_cpf, mock_obter_input):
        paciente = Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta")
        self.db.buscar_paciente_por_cpf.return_value = paciente
        
        relatar_incidente(self.db, self.maqueiro_logado)
        
        self.db.insert_incidente.assert_called_once()
        mock_showinfo.assert_called_once_with("Sucesso", "Incidente registrado com sucesso.", parent=None)

    @patch('tkinter.messagebox.showinfo')
    def test_ver_solicitacoes_transporte(self, mock_showinfo):
        solicitacao = SolicitacaoTransporte(1, "Solicitação de transporte", Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta"), "2023-06-10 14:30:00", self.maqueiro_logado)
        self.db.listar_solicitacoes_pendentes.return_value = [solicitacao]
        
        ver_solicitacoes_transporte(self.db)
        
        self.db.listar_solicitacoes_pendentes.assert_called_once()
        mock_showinfo.assert_called_once()

    @patch('funcoes_menu.obter_input', side_effect=["1", "A"])
    @patch('tkinter.messagebox.showinfo')
    def test_aceitar_ou_recusar_solicitacao_aceitar(self, mock_showinfo, mock_obter_input):
        solicitacao = SolicitacaoTransporte(1, "Solicitação de transporte", Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta"), "2023-06-10 14:30:00", self.maqueiro_logado)
        self.solicitacoes_transporte.append(solicitacao)
        
        aceitar_ou_recusar_solicitacao(self.db, self.solicitacoes_transporte, self.maqueiro_logado)
        
        self.db.update_solicitacao_status.assert_called_once_with(1, 'aceita', 1)
        self.db.iniciar_transporte_paciente.assert_called_once_with(solicitacao.paciente.id)
        mock_showinfo.assert_any_call("Sucesso", f"Transporte do paciente {solicitacao.paciente.nome} concluído com sucesso.", parent=unittest.mock.ANY)
        mock_showinfo.assert_any_call("Sucesso", "Solicitação 1 aceita com sucesso.", parent=None)
        self.assertEqual(solicitacao.status, 'aceita')

    @patch('funcoes_menu.obter_input', side_effect=["1", "R"])
    @patch('tkinter.messagebox.showinfo')
    def test_aceitar_ou_recusar_solicitacao_recusar(self, mock_showinfo, mock_obter_input):
        solicitacao = SolicitacaoTransporte(1, "Solicitação de transporte", Paciente("João Silva", "12345678901", "Sala 101", "Estável", "Aguardando transporte", "Alta"), "2023-06-10 14:30:00", self.maqueiro_logado)
        self.solicitacoes_transporte.append(solicitacao)
        
        aceitar_ou_recusar_solicitacao(self.db, self.solicitacoes_transporte, self.maqueiro_logado)
        
        self.db.update_solicitacao_status.assert_called_once_with(1, 'recusada', 1)
        mock_showinfo.assert_called_once_with("Sucesso", "Solicitação 1 recusada com sucesso.", parent=None)
        self.assertEqual(solicitacao.status, 'recusada')

if __name__ == '__main__':
    unittest.main()
