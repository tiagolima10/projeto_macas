import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import funcoes_menu
import logging

def exibir_menu(sistema_notificacoes, maqueiro_logado, pacientes, maqueiros, tarefas, db, root):
    """
    Exibe o menu de opções e executa as ações correspondentes com base na entrada do usuário usando Tkinter.

    Args:
        sistema_notificacoes (SistemaDeNotificacoes): Instância do sistema de notificações.
        maqueiro_logado (Maqueiro): Instância do maqueiro atualmente logado.
        pacientes (list): Lista de pacientes cadastrados.
        maqueiros (list): Lista de maqueiros cadastrados.
        tarefas (list): Lista de tarefas.
        db (Database): Instância do banco de dados.
        root (tk.Tk): Instância da janela principal do Tkinter.
    """
    solicitacoes_transporte = db.listar_solicitacoes_pendentes()

    def chamar_funcao(opcao):
        try:
            if opcao == 1:
                funcoes_menu.cadastrar_paciente(db, pacientes, parent=root)
            elif opcao == 2:
                funcoes_menu.ver_status_pacientes(db, parent=root)
            elif opcao == 3:
                funcoes_menu.adicionar_tarefa(db, tarefas, maqueiro_logado, parent=root)
            elif opcao == 4:
                funcoes_menu.concluir_tarefa(db, tarefas, parent=root)
            elif opcao == 5:
                funcoes_menu.listar_tarefas_pendentes(db, parent=root)
            elif opcao == 6:
                funcoes_menu.relatar_incidente(db, maqueiro_logado, parent=root)
            elif opcao == 7:
                funcoes_menu.relatorio_de_incidentes(db, parent=root)
            elif opcao == 8:
                funcoes_menu.solicitar_transporte(db, maqueiro_logado, solicitacoes_transporte, parent=root)
            elif opcao == 9:
                funcoes_menu.ver_solicitacoes_transporte(db, parent=root)
            elif opcao == 10:
                funcoes_menu.aceitar_ou_recusar_solicitacao(db, solicitacoes_transporte, maqueiro_logado, parent=root)
            elif opcao == 0:
                root.destroy()
            else:
                messagebox.showerror("Erro", "Opção inválida. Tente novamente.")
        except Exception as e:
            logging.error(f"Erro no menu de opções: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro. Verifique os logs para mais detalhes.")

    # Remove todos os widgets da janela principal
    for widget in root.winfo_children():
        widget.destroy()

    # Carrega a imagem de fundo
    fundo_imagem = Image.open("images/fundo.webp")
    fundo_imagem = fundo_imagem.resize((800, 600), Image.Resampling.LANCZOS)
    fundo_imagem_tk = ImageTk.PhotoImage(fundo_imagem)

    # Cria um canvas para exibir a imagem de fundo
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=fundo_imagem_tk)

    def criar_borda_arredondada(canvas, x, y, width, height, radius, color):
        points = [
            x + radius, y,
            x + width - radius, y,
            x + width, y, x + width, y + radius,
            x + width, y + height - radius,
            x + width, y + altura, x + width - radius, y + altura,
            x + radius, y + altura,
            x, y + altura, x, y + altura - radius,
            x, y + radius,
            x, y, x + radius, y
        ]
        return canvas.create_polygon(points, smooth=True, fill=color, outline='')

    # Adiciona uma caixa branca transparente para o menu
    largura = 420
    altura = 470
    x_centro = 400
    y_centro = 300

    # Cria a borda arredondada
    criar_borda_arredondada(canvas, x_centro - largura // 2, y_centro - altura // 2, largura, altura, 20, "white")

    # Frame do menu (sobre a imagem de fundo e a borda arredondada)
    frame_menu = tk.Frame(canvas, bg="white")
    canvas.create_window(x_centro, y_centro, window=frame_menu, width=largura - 20, height=altura - 20)

    # Título do menu
    tk.Label(frame_menu, text="Menu de Opções", font=("Arial", 14), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    # Botões do menu
    botoes = [
        ("Cadastrar paciente", 1),
        ("Ver status dos pacientes", 2),
        ("Adicionar nova tarefa", 3),
        ("Concluir tarefa", 4),
        ("Listar tarefas pendentes", 5),
        ("Relatar incidente", 6),
        ("Relatório de Incidentes", 7),
        ("Solicitar transporte de paciente", 8),
        ("Ver solicitações de transporte", 9),
        ("Aceitar ou recusar solicitações de transporte", 10),
        ("Sair", 0),
    ]

    for i, (text, opcao) in enumerate(botoes):
        tk.Button(frame_menu, text=text, command=lambda opcao=opcao: chamar_funcao(opcao)).grid(row=i+1, column=0, columnspan=2, sticky="ew", pady=5)

    # Configurar colunas para expandir igualmente
    frame_menu.grid_columnconfigure(0, weight=1)
    frame_menu.grid_columnconfigure(1, weight=1)

    root.mainloop()

def input_senha(prompt):
    """
    Solicita ao usuário que insira uma senha de forma segura usando uma caixa de diálogo Tkinter.

    Args:
        prompt (str): A mensagem a ser exibida ao usuário solicitando a senha.

    Returns:
        str: A senha inserida pelo usuário.
    """
    senha = tk.simpledialog.askstring("Senha", prompt, show='*')
    return senha
