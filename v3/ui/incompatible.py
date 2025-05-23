import customtkinter as ctk
from ui import start

def exibir_mensagem_incompativel():
    def abrir_novo_arquivo():
        root.destroy()
        start.main()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.title("Arquivo Incompatível")
    root.geometry("480x280")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, fg_color="transparent")  # Fundo transparente
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.8)

    label = ctk.CTkLabel(
        frame,
        text="O arquivo selecionado não é compatível com as regras de importação.",
        text_color="#c0392b",
        font=("Segoe UI", 16, "bold"),
        fg_color="transparent",
        wraplength=400,
        justify="center"
    )
    label.pack(pady=(20, 10), padx=10)

    btn_novo = ctk.CTkButton(
        frame,
        text="Abrir Novo Arquivo",
        command=abrir_novo_arquivo,
        fg_color="#4CAF50",
        hover_color="#388e3c",
        text_color="white",
        font=("Segoe UI", 12, "bold"),
        corner_radius=16,
        height=40,
        width=180
    )
    btn_novo.pack(pady=(0, 10))

    btn_fechar = ctk.CTkButton(
        frame,
        text="Fechar",
        command=root.destroy,
        fg_color="#e74c3c",
        hover_color="#c0392b",
        text_color="white",
        font=("Segoe UI", 12, "bold"),
        corner_radius=16,
        height=40,
        width=180
    )
    btn_fechar.pack(pady=(0, 18))

    footer = ctk.CTkLabel(
        root,
        text="© 2024 Assistente de Importação",
        font=("Segoe UI", 8),
        text_color="#888",
        fg_color="transparent"
    )
    footer.pack(side="bottom", pady=8)

    root.mainloop()
