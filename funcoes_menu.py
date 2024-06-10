import tkinter as tk
from tkinter import simpledialog, messagebox
from models import Paciente, Tarefa, SolicitacaoTransporte, Incidente
from validations import validar_cpf, obter_nivel_urgencia, obter_status_transporte
from datetime import datetime
import logging


# Funções de utilidade
def obter_input(prompt, parent=None):
    """
    Exibe uma caixa de diálogo para obter uma entrada do usuário.
    """
    dialog = simpledialog.askstring("Input", prompt, parent=parent)
    if dialog:
        return dialog.strip()
    return None

# Funções de operações
def cadastrar_paciente(db, pacientes, parent=None):
    """
    Cadastra um novo paciente no sistema.

    Args:
        db (Database): Instância do banco de dados.
        pacientes (list): Lista de pacientes cadastrados.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        nome = obter_input("Nome do paciente: ", parent)
        if not nome:
            return
        while True:
            cpf = obter_input("CPF do paciente: ", parent)
            if not cpf:
                return
            if not validar_cpf(cpf):
                messagebox.showerror("Erro", "CPF inválido. Tente novamente.", parent=parent)
                continue
            if db.buscar_paciente_por_cpf(cpf):
                messagebox.showerror("Erro", "CPF já cadastrado. Insira um CPF diferente.", parent=parent)
            else:
                break
        localizacao = obter_input("Localização do paciente: ", parent)
        if not localizacao:
            return
        condicao = obter_input("Condição do paciente: ", parent)
        if not condicao:
            return
        urgencia = obter_nivel_urgencia(parent)['nivel']
        transporte = obter_status_transporte(parent)
        paciente = Paciente(nome, cpf, localizacao, condicao, transporte, urgencia)
        paciente_id = db.insert_paciente(paciente)
        paciente.definir_id(paciente_id)
        pacientes.append(paciente)
        messagebox.showinfo("Sucesso", f"Paciente {paciente.nome} cadastrado com sucesso.", parent=parent)
    except Exception as e:
        logging.error(f"Erro ao cadastrar paciente: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao cadastrar o paciente. Verifique os logs para mais detalhes.", parent=parent)


def ver_status_pacientes(db, parent=None):
    """
    Exibe o status de todos os pacientes cadastrados na interface tkinter.
    """
    try:
        pacientes = db.listar_pacientes()
        
        if not pacientes:
            messagebox.showinfo("Informação", "Não há pacientes cadastrados.", parent=parent)
            return

        root = tk.Toplevel(parent)
        root.title("Status dos Pacientes")

        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for paciente in pacientes:
            paciente_info = f"ID: {paciente.id}\nNome: {paciente.nome}\nLocalização: {paciente.localizacao}\nCondição: {paciente.condicao}\nUrgência: {paciente.urgencia}\nStatus Transporte: {paciente.transporte}\n"
            tk.Label(scrollable_frame, text=paciente_info, justify=tk.LEFT, anchor="w").pack(fill="x", padx=10, pady=5)
            tk.Frame(scrollable_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill="x", padx=5, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        root.mainloop()
    except Exception as e:
        logging.error(f"Erro ao exibir status dos pacientes: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao exibir o status dos pacientes. Verifique os logs para mais detalhes.", parent=parent)

def adicionar_tarefa(db, tarefas, maqueiro_logado, parent=None):
    """
    Adiciona uma nova tarefa para um maqueiro.

    Args:
        db (Database): Instância do banco de dados.
        tarefas (list): Lista de tarefas.
        maqueiro_logado (Maqueiro): Maqueiro atualmente logado.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        descricao = obter_input("Descrição da tarefa: ", parent=parent)
        prioridade = obter_input("Prioridade da tarefa: ", parent=parent)
        cpf_paciente = obter_input("CPF do paciente: ", parent=parent)
        if not validar_cpf(cpf_paciente):
            messagebox.showerror("Erro", "CPF inválido. Tente novamente.", parent=parent)
            return
        paciente = db.buscar_paciente_por_cpf(cpf_paciente)
        if not paciente:
            messagebox.showerror("Erro", "Paciente não encontrado.", parent=parent)
            return
        localizacao = obter_input("Localização da tarefa: ", parent=parent)
        tarefa = Tarefa(None, descricao, prioridade, paciente, localizacao, maqueiro_logado)
        tarefa_id = db.insert_tarefa(tarefa)
        tarefa.id = tarefa_id
        tarefas.append(tarefa)
        messagebox.showinfo("Sucesso", f"Tarefa '{tarefa.descricao}' adicionada com sucesso.", parent=parent)
    except Exception as e:
        logging.error(f"Erro ao adicionar tarefa: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao adicionar a tarefa. Verifique os logs para mais detalhes.", parent=parent)

def concluir_tarefa(db, tarefas, parent=None):
    """
    Conclui uma tarefa existente.

    Args:
        db (Database): Instância do banco de dados.
        tarefas (list): Lista de tarefas.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        id_tarefa = int(obter_input("ID da tarefa a concluir: ", parent=parent))
        tarefa = next((t for t in tarefas if t.id == id_tarefa), None)
        if not tarefa:
            messagebox.showerror("Erro", "Tarefa não encontrada.", parent=parent)
            return
        tarefa.status = 'concluída'
        db.update_tarefa_status(tarefa.id, tarefa.status)
        messagebox.showinfo("Sucesso", f"Tarefa {tarefa.id} concluída com sucesso.", parent=parent)
    except Exception as e:
        logging.error(f"Erro ao concluir tarefa: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao concluir a tarefa. Verifique os logs para mais detalhes.", parent=parent)

def listar_tarefas_pendentes(db, parent=None):
    """
    Lista todas as tarefas pendentes.
    """
    try:
        tarefas_pendentes = db.listar_tarefas_pendentes()

        if not tarefas_pendentes:
            messagebox.showinfo("Informação", "Não há tarefas pendentes, no momento.", parent=parent)
            return

        tarefas_text = ""
        for tarefa in tarefas_pendentes:
            tarefas_text += f"ID: {tarefa.id}, Descrição: {tarefa.descricao}, Prioridade: {tarefa.prioridade}, Paciente: {tarefa.paciente.nome}, Localização: {tarefa.localizacao}\n"

        messagebox.showinfo("Tarefas Pendentes", tarefas_text, parent=parent)
    except Exception as e:
        logging.error(f"Erro ao listar tarefas pendentes: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao listar as tarefas pendentes. Verifique os logs para mais detalhes.", parent=parent)


def relatar_incidente(db, maqueiro_logado, parent=None):
    """
    Relata um novo incidente.

    Args:
        db (Database): Instância do banco de dados.
        maqueiro_logado (Maqueiro): Instância do maqueiro logado.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    descricao = obter_input("Descrição do incidente: ", parent)
    cpf_paciente = obter_input("CPF do paciente: ", parent)
    if not validar_cpf(cpf_paciente):
        messagebox.showerror("Erro", "CPF inválido. Tente novamente.", parent=parent)
        return
    paciente = db.buscar_paciente_por_cpf(cpf_paciente)
    if not paciente:
        messagebox.showerror("Erro", "Paciente não encontrado.", parent=parent)
        return
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    incidente = Incidente(None, descricao, maqueiro_logado, paciente, data_hora)
    db.insert_incidente(incidente)
    messagebox.showinfo("Sucesso", "Incidente registrado com sucesso.", parent=parent)

def relatorio_de_incidentes(db, parent=None):
    """
    Exibe um relatório de todos os incidentes registrados, ordenados do mais recente para o mais antigo.

    Args:
        db (Database): Instância do banco de dados.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        incidentes = db.listar_incidentes()

        if not incidentes:
            messagebox.showinfo("Informação", "Não há incidentes registrados.", parent=parent)
            return

        root = tk.Toplevel(parent)
        root.title("Relatório de Incidentes")

        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for incidente in incidentes:
            maqueiro = db.buscar_maqueiro_por_id(incidente.maqueiro.id)
            paciente = db.buscar_paciente_por_id(incidente.paciente.id)
            incidente_info = (f"Descrição: {incidente.descricao}\n"
                              f"Maqueiro: {maqueiro.nome}\n"
                              f"Paciente: {paciente.nome}\n"
                              f"Data/Hora: {incidente.data_hora}\n")
            tk.Label(scrollable_frame, text=incidente_info, justify=tk.LEFT, anchor="w").pack(fill="x", padx=10, pady=5)
            tk.Frame(scrollable_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill="x", padx=5, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        root.mainloop()
    except Exception as e:
        logging.error(f"Erro ao exibir relatório de incidentes: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao exibir o relatório de incidentes. Verifique os logs para mais detalhes.", parent=parent)


def solicitar_transporte(db, maqueiro_logado, solicitacoes_transporte, parent=None):
    """
    Solicita transporte para um paciente.

    Args:
        db (Database): Instância do banco de dados.
        maqueiro_logado (Maqueiro): Instância do maqueiro logado.
        solicitacoes_transporte (list): Lista de solicitações de transporte.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        descricao = obter_input("Descrição da solicitação: ", parent=parent)
        cpf_paciente = obter_input("CPF do paciente: ", parent=parent)
        if not validar_cpf(cpf_paciente):
            messagebox.showerror("Erro", "CPF inválido. Tente novamente.", parent=parent)
            return
        paciente = db.buscar_paciente_por_cpf(cpf_paciente)
        if not paciente:
            messagebox.showerror("Erro", "Paciente não encontrado.", parent=parent)
            return
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        solicitacao = SolicitacaoTransporte(None, descricao, paciente, data_hora, maqueiro_logado)
        solicitacao_id = db.insert_solicitacao_transporte(solicitacao)
        solicitacao.id = solicitacao_id
        solicitacoes_transporte.append(solicitacao)
        messagebox.showinfo("Sucesso", "Solicitação de transporte registrada com sucesso.", parent=parent)
    except Exception as e:
        logging.error(f"Erro ao solicitar transporte: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao solicitar transporte. Verifique os logs para mais detalhes.", parent=parent)

def ver_solicitacoes_transporte(db, parent=None):
    """
    Exibe todas as solicitações de transporte pendentes ou recusadas.

    Args:
        db (Database): Instância do banco de dados.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    try:
        solicitacoes_transporte = db.listar_solicitacoes_pendentes()

        if not solicitacoes_transporte:
            messagebox.showinfo("Informação", "Não há solicitações de transporte pendentes ou recusadas, no momento.", parent=parent)
            return

        solicitacoes_text = ""
        for solicitacao in solicitacoes_transporte:
            solicitacoes_text += f"ID: {solicitacao.id}, Descrição: {solicitacao.descricao}, Paciente: {solicitacao.paciente.nome}, Status: {solicitacao.status}\n"

        messagebox.showinfo("Solicitações de Transporte", solicitacoes_text, parent=parent)
    except Exception as e:
        logging.error(f"Erro ao exibir solicitações de transporte: {e}")
        messagebox.showerror("Erro", "Ocorreu um erro ao exibir as solicitações de transporte. Verifique os logs para mais detalhes.", parent=parent)

def aceitar_ou_recusar_solicitacao(db, solicitacoes_transporte, maqueiro_logado, parent=None):
    """
    Aceita ou recusa uma solicitação de transporte e, se aceita, exibe os detalhes do transporte.

    Args:
        db (Database): Instância do banco de dados.
        solicitacoes_transporte (list): Lista de solicitações de transporte.
        maqueiro_logado (Maqueiro): Instância do maqueiro logado.
        parent (tk.Tk): Janela pai para as caixas de diálogo.
    """
    id_solicitacao = int(obter_input("ID da solicitação a aceitar ou recusar: ", parent))
    solicitacao = next((s for s in solicitacoes_transporte if s.id == id_solicitacao), None)
    if not solicitacao:
        messagebox.showerror("Erro", "Solicitação não encontrada.", parent=parent)
        return
    acao = obter_input("Deseja aceitar (A) ou recusar (R) a solicitação? ", parent)
    if acao.upper() == 'A':
        solicitacao.status = 'aceita'
        db.update_solicitacao_status(solicitacao.id, solicitacao.status, maqueiro_logado.id)
        db.iniciar_transporte_paciente(solicitacao.paciente.id)
        exibir_detalhes_transporte(db, solicitacao, maqueiro_logado, parent)
        messagebox.showinfo("Sucesso", f"Solicitação {solicitacao.id} aceita com sucesso.", parent=parent)
    elif acao.upper() == 'R':
        solicitacao.status = 'recusada'
        db.update_solicitacao_status(solicitacao.id, solicitacao.status, maqueiro_logado.id)
        messagebox.showinfo("Sucesso", f"Solicitação {solicitacao.id} recusada com sucesso.", parent=parent)
    else:
        messagebox.showerror("Erro", "Ação inválida.", parent=parent)

def exibir_detalhes_transporte(db, solicitacao, maqueiro_logado, parent=None):
    """
    Exibe uma nova aba com os detalhes do paciente e a opção de finalizar o transporte.

    Args:
        db (Database): Instância do banco de dados.
        solicitacao (SolicitacaoTransporte): A solicitação de transporte aceita.
        maqueiro_logado (Maqueiro): Instância do maqueiro logado.
        parent (tk.Tk): Janela pai para a nova aba.
    """
    def finalizar_transporte():
        paciente_id = solicitacao.paciente.id
        db.concluir_transporte_paciente(paciente_id)
        db.atualizar_localizacao_paciente(paciente_id, nova_localizacao_entry.get())
        messagebox.showinfo("Sucesso", f"Transporte do paciente {solicitacao.paciente.nome} concluído com sucesso.", parent=details_window)
        details_window.destroy()

    details_window = tk.Toplevel(parent)
    details_window.title("Detalhes do Transporte")

    tk.Label(details_window, text="Nome do Paciente:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(details_window, text=solicitacao.paciente.nome).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(details_window, text="Localização Atual:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(details_window, text=solicitacao.paciente.localizacao).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(details_window, text="Nova Localização:").grid(row=2, column=0, padx=10, pady=5)
    nova_localizacao_entry = tk.Entry(details_window)
    nova_localizacao_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(details_window, text="Finalizar Transporte", command=finalizar_transporte).grid(row=3, columnspan=2, pady=10)

    details_window.mainloop()
