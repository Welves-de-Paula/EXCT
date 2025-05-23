import customtkinter as ctk
from tkinter import filedialog
from script.store import store

class StartApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Assistente de Importação")
        self.geometry("420x240")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")
        self.selected_file = {"path": None}
        self.after_ids = []
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
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

        select_button = ctk.CTkButton(
            frame_selecao,
            text="Selecionar Arquivo Excel",
            command=self.on_select,
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
            self,
            text="© 2024 Assistente de Importação",
            font=("Segoe UI", 8),
            text_color="#888",
            fg_color="transparent"
        )
        footer.pack(side="bottom", pady=8)

    def on_select(self):
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )
        if filepath:
            self.selected_file["path"] = filepath
            store(filepath, 'origin')
            self.cancel_all_after()
            self.on_closing()  # Garante fechamento seguro

    def safe_after(self, delay, callback):
        if self.winfo_exists():
            after_id = self.after(delay, callback)
            self.after_ids.append(after_id)
            return after_id
        return None

    def cancel_all_after(self):
        for after_id in self.after_ids:
            try:
                self.after_cancel(after_id)
            except Exception:
                pass
        self.after_ids.clear()

    def on_closing(self):
        self.cancel_all_after()
        try:
            self.quit()  # Para o mainloop imediatamente
        except Exception:
            pass
        try:
            self.destroy()  # Destroi a janela
        except Exception:
            pass

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = StartApp()
    app.mainloop()
    return app.selected_file["path"]

if __name__ == "__main__":
    main()
