import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import tkinter as tk

# Adiciona o diretório contendo validations.py ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import validations

class TestValidations(unittest.TestCase):

    def test_validar_cpf(self):
        self.assertTrue(validations.validar_cpf("12345678901"))
        self.assertTrue(validations.validar_cpf("123.456.789-01"))
        self.assertTrue(validations.validar_cpf("1234567890"))
        self.assertFalse(validations.validar_cpf("123456789"))
        self.assertFalse(validations.validar_cpf("123456789012"))

    @patch('tkinter.simpledialog.askstring', return_value="Entrada válida")
    @patch('tkinter.messagebox.showerror')
    def test_obter_input_valido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_input("Mensagem", parent=parent)
        self.assertEqual(resultado, "Entrada válida")
        mock_showerror.assert_not_called()

    @patch('tkinter.simpledialog.askstring', side_effect=["", " ", "Entrada válida"])
    @patch('tkinter.messagebox.showerror')
    def test_obter_input_invalido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_input("Mensagem", parent=parent)
        self.assertEqual(resultado, "Entrada válida")
        self.assertEqual(mock_showerror.call_count, 2)

    @patch('tkinter.simpledialog.askstring', return_value="3")
    @patch('tkinter.messagebox.showerror')
    def test_obter_nivel_urgencia_valido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_nivel_urgencia(parent=parent)
        self.assertEqual(resultado, {"nivel": "Média", "cor": "blue"})
        mock_showerror.assert_not_called()

    @patch('tkinter.simpledialog.askstring', side_effect=["5", "abc", "2"])
    @patch('tkinter.messagebox.showerror')
    def test_obter_nivel_urgencia_invalido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_nivel_urgencia(parent=parent)
        self.assertEqual(resultado, {"nivel": "Alta", "cor": "yellow"})
        self.assertEqual(mock_showerror.call_count, 2)

    @patch('tkinter.simpledialog.askstring', return_value="2")
    @patch('tkinter.messagebox.showerror')
    def test_obter_status_transporte_valido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_status_transporte(parent=parent)
        self.assertEqual(resultado, "Em transporte")
        mock_showerror.assert_not_called()

    @patch('tkinter.simpledialog.askstring', side_effect=["4", "abc", "1"])
    @patch('tkinter.messagebox.showerror')
    def test_obter_status_transporte_invalido(self, mock_showerror, mock_askstring):
        parent = tk.Tk()
        resultado = validations.obter_status_transporte(parent=parent)
        self.assertEqual(resultado, "Aguardando Transporte")
        self.assertEqual(mock_showerror.call_count, 2)

if __name__ == '__main__':
    unittest.main()
