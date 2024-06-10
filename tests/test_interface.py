import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

# Adiciona o diretório raiz do projeto ao sys.path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface import exibir_menu, input_senha
from models import Maqueiro

class TestInterface(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.db = MagicMock()
        self.sistema_notificacoes = MagicMock()
        self.maqueiro_logado = Maqueiro(1, "Carlos", "123456", "1980-01-01", "M")
        self.pacientes = []
        self.maqueiros = []
        self.tarefas = []
        self.solicitacoes_transporte = []
        self.root_closed = False  # Indicador de fechamento da janela

    def close_root(self):
        self.root_closed = True
        self.root.destroy()

    @patch('tkinter.simpledialog.askstring', return_value="senha123")
    def test_input_senha(self, mock_askstring):
        senha = input_senha("Digite sua senha:")
        mock_askstring.assert_called_once_with("Senha", "Digite sua senha:", show='*')
        self.assertEqual(senha, "senha123")

if __name__ == '__main__':
    unittest.main()
