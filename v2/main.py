# -*- coding: utf-8 -*-
from tkinter import Tk
from interface import App
from utils import dividir_arquivo_excel, abrir_diretorio
import sys

def main():
    try:
        root = Tk()
        root.update_idletasks()  # Garante que a interface seja atualizada
        app = App(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao executar o programa: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


