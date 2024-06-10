import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import Database
from notifications import SistemaDeNotificacoes
from interface import exibir_menu

def realizar_login(db, root, frame_login):
    """
    Realiza o login do maqueiro no sistema, solicitando login e senha.

    Args:
        db (Database): Instância do banco de dados.
        root (tk.Tk): Instância da janela principal do Tkinter.
        frame_login (tk.Frame): Frame do Tkinter onde os campos de login estão inseridos.

    Returns:
        None
    """
    login = login_entry.get()
    senha = senha_entry.get()

    maqueiro = db.buscar_maqueiro_por_login(login)
    if maqueiro and maqueiro.senha == senha:
        messagebox.showinfo("Login", f"Bem-vindo, {maqueiro.nome}!")
        # Remove login frame
        frame_login.pack_forget()
        frame_login.destroy()
        # Chama o menu principal
        exibir_menu(sistema_notificacoes, maqueiro, pacientes, maqueiros, tarefas, db, root)
    else:
        messagebox.showerror("Login", "Login ou senha incorretos. Tente novamente.")

def main():
    """
    Função principal do sistema que inicializa o banco de dados, 
    realiza o login e exibe o menu de opções.
    """
    global sistema_notificacoes, pacientes, maqueiros, tarefas, login_entry, senha_entry
    
    db = Database('localhost', 'root', '', 'projeto_macas')
    db.create_tables()
    sistema_notificacoes = SistemaDeNotificacoes()
    pacientes = []
    maqueiros = []
    tarefas = []

    # Inicializa a janela principal do Tkinter
    root = tk.Tk()
    root.title("Sistema de Gestão de Maqueiros")
    root.geometry("800x600")  # Define o tamanho da janela
    root.resizable(False, False)  # Desabilita o redimensionamento da janela

    root.iconbitmap('images/hosp-icon.ico')

    # Imagem do HGCA de fundo
    imagem = Image.open("images/hospital.png")
    largura, altura = 800, 600  # Define o tamanho da imagem para cobrir a janela
    imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)  # Redimensiona a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Canvas para exibir a imagem
    canvas = tk.Canvas(root, width=largura, height=altura)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)

    # Caixa branca transparente para o formulário de login
    frame_login = tk.Frame(root, bg="white", bd=5)
    canvas.create_window(largura // 2, altura // 2, window=frame_login, width=210, height=110)

    # Campos de entrada e os botões ao frame de login
    tk.Label(frame_login, text="Login:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    login_entry = tk.Entry(frame_login)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_login, text="Senha:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    senha_entry = tk.Entry(frame_login, show="*")
    senha_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = tk.Button(frame_login, text="Login", command=lambda: realizar_login(db, root, frame_login))
    login_button.grid(row=2, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
