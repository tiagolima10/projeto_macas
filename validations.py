import re
from tkinter import simpledialog, messagebox

def validar_cpf(cpf):
    """
    Valida o CPF, permitindo tanto 10 quanto 11 dígitos.

    Args:
        cpf (str): O CPF a ser validado.

    Returns:
        bool: Retorna True se o CPF for válido, caso contrário, retorna False.
    """
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) > 11 or len(cpf) < 10:
        return False
    return True

def obter_input(mensagem, parent=None):
    """
    Exibe uma caixa de diálogo para obter uma entrada do usuário que não pode estar vazia.

    Args:
        mensagem (str): A mensagem a ser exibida ao solicitar a entrada do usuário.
        parent (tk.Tk): A janela pai para a caixa de diálogo.

    Returns:
        str: A entrada fornecida pelo usuário.
    """
    while True:
        entrada = simpledialog.askstring("Entrada", mensagem, parent=parent)
        if entrada and entrada.strip():  # Verifica se a entrada não está vazia
            return entrada.strip()
        else:
            messagebox.showerror("Erro", "Campo obrigatório. Por favor, insira uma informação válida.", parent=parent)

def obter_nivel_urgencia(parent=None):
    """
    Exibe uma caixa de diálogo para obter o nível de urgência a partir da entrada do usuário.

    Args:
        parent (tk.Tk): A janela pai para a caixa de diálogo.

    Returns:
        dict: O nível de urgência e a cor correspondente.
    """
    niveis_urgencia = {
        1: ("Emergência", "red"),
        2: ("Alta", "yellow"),
        3: ("Média", "blue"),
        4: ("Baixa", "green")
    }

    while True:
        try:
            urgencia = int(obter_input("Nível de urgência (1-Emergência, 2-Alta, 3-Média, 4-Baixa): ", parent))
            if urgencia in niveis_urgencia:
                nivel, cor = niveis_urgencia[urgencia]
                return {"nivel": nivel, "cor": cor}
            else:
                messagebox.showerror("Erro", "Por favor, escolha um número entre 1 e 4.", parent=parent)
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Por favor, insira um número.", parent=parent)

def obter_status_transporte(parent=None):
    """
    Exibe uma caixa de diálogo para obter o status do transporte a partir da entrada do usuário.

    Args:
        parent (tk.Tk): A janela pai para a caixa de diálogo.

    Returns:
        str: O status do transporte selecionado pelo usuário.
    """
    status_transporte = {
        1: "Aguardando Transporte",
        2: "Em transporte",
        3: "Chegou ao destino"
    }

    while True:
        try:
            transporte = int(obter_input("Status do Transporte (1-Aguardando Transporte, 2-Em transporte, 3-Chegou ao destino): ", parent))
            if transporte in status_transporte:
                return status_transporte[transporte]
            else:
                messagebox.showerror("Erro", "Por favor, escolha um número entre 1 e 3.", parent=parent)
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Por favor, insira um número.", parent=parent)
