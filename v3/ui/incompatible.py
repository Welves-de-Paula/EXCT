import tkinter as tk

def main(msg="Arquivo incompatível."):
    root = tk.Tk()
    root.title("Arquivo Incompatível")
    label = tk.Label(root, text=msg, padx=20, pady=20, fg="red", font=("Arial", 14))
    label.pack()
    btn = tk.Button(root, text="Fechar", command=root.destroy)
    btn.pack(pady=(10, 20))
    root.mainloop()
