import tkinter as tk
from tkinter import messagebox
import os

def main(msg="Arquivo incompatível. Por favor, utilize apenas arquivos .xlsx válidos."):
    def on_close():
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            root.destroy()
            # Limpeza de arquivos temporários
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            for sub in ["origin", "output", "compare"]:
                subdir = os.path.join(data_dir, sub)
                if os.path.exists(subdir):
                    for f in os.listdir(subdir):
                        try:
                            os.remove(os.path.join(subdir, f))
                        except Exception:
                            pass
    root = tk.Tk()
    root.title("Arquivo Incompatível")
    root.geometry("400x150")
    root.resizable(False, False)
    label = tk.Label(root, text=msg, font=("Segoe UI", 12), fg="red")
    label.pack(pady=30)
    btn = tk.Button(root, text="Sair", command=on_close, bg="#d32f2f", fg="white", font=("Segoe UI", 10, "bold"))
    btn.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
