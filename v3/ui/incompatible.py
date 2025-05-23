import customtkinter as ctk
from ui import start

class IncompatibleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.after_ids = []
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        self.title("Arquivo Incompatível")
        self.geometry("480x280")
        self.resizable(False, False)
        frame = ctk.CTkFrame(self, fg_color="transparent")
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
            command=self.abrir_novo_arquivo,
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
            command=self.on_closing,
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
            self,
            text="© 2024 Assistente de Importação",
            font=("Segoe UI", 8),
            text_color="#888",
            fg_color="transparent"
        )
        footer.pack(side="bottom", pady=8)

    def abrir_novo_arquivo(self):
        self.cancel_all_after()
        self.after(100, self._abrir_start_seguro)

    def _abrir_start_seguro(self):
        try:
            self.destroy()
        except Exception:
            pass
        try:
            start.main()
        except Exception as e:
            print(f"Erro ao abrir start: {e}")

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
            self.destroy()
        except Exception:
            pass

def exibir_mensagem_incompativel():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = IncompatibleApp()
    app.mainloop()
