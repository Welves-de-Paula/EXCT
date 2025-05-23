import customtkinter as ctk
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
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.title("Assistente de Importação")
    root.geometry("420x240")
    root.resizable(False, False)
    root.configure(bg="#f5f6fa")

    container = ctk.CTkFrame(root, fg_color="transparent")
    container.place(relx=0.5, rely=0.5, anchor="center")

    label = ctk.CTkLabel(
        container,
        text="Bem-vindo ao Assistente de Importação!",
        font=("Segoe UI", 15, "bold"),
        text_color="#222",
        fg_color="transparent"
    )
    label.pack(pady=(0, 18))

    frame_selecao = ctk.CTkFrame(container, fg_color="transparent")
    frame_selecao.pack()

    selected_file = {"path": None}

    def on_select():
        abrir_arquivo(root, selected_file)

    select_button = ctk.CTkButton(
        frame_selecao,
        text="Selecionar Arquivo Excel",
        command=on_select,
        fg_color="#4CAF50",
        hover_color="#388e3c",
        text_color="white",
        font=("Segoe UI", 11, "bold"),
        corner_radius=16,
        height=40,
        width=200
    )
    select_button.pack(pady=5)

    footer = ctk.CTkLabel(
        root,
        text="© 2024 Assistente de Importação",
        font=("Segoe UI", 8),
        text_color="#888",
        fg_color="transparent"
    )
    footer.pack(side="bottom", pady=8)

    root.mainloop()
    return selected_file["path"]

if __name__ == "__main__":
    main()
