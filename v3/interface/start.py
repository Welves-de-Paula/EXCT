import tkinter as tk
from tkinter import filedialog
from script.store import store

def abrir_arquivo(root, selected_file):
    filepath = filedialog.askopenfilename(
        title="Selecione um arquivo Excel",
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )
    if filepath:
        print(f"Arquivo selecionado: {filepath}")
        selected_file["path"] = filepath
        # Chama a função store para processar o arquivo Excel e salvar no SQLite
        store(filepath, 'origin')
        root.quit()
        root.destroy()  # Fecha a janela imediatamente após seleção

def main():
    root = tk.Tk()
    root.title("Assistente de Importação")
    root.geometry("420x240")
    root.resizable(False, False)
    root.configure(bg="#f5f6fa")

    container = tk.Frame(root, bg="#f5f6fa")
    container.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(
        container,
        text="Bem-vindo ao Assistente de Importação!",
        font=("Segoe UI", 15, "bold"),
        bg="#f5f6fa",
        fg="#222"
    )

    label.pack(pady=(0, 18))

    frame_selecao = tk.Frame(container, bg="#f5f6fa")
    frame_selecao.pack()

    selected_file = {"path": None}

    def on_select():
        abrir_arquivo(root, selected_file)

    select_button = tk.Button(
        frame_selecao,
        text="Selecionar Arquivo Excel",
        command=on_select,
        bg="#4CAF50",
        activebackground="#388e3c",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0,
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2"
    )

    select_button.pack(pady=5)

    footer = tk.Label(
        root,
        text="© 2024 Assistente de Importação",
        font=("Segoe UI", 8),
        bg="#f5f6fa",
        fg="#888"
    )
    footer.pack(side="bottom", pady=8)

    root.mainloop()
    return selected_file["path"]

if __name__ == "__main__":
    main()
