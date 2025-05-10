# -*- coding: utf-8 -*-
import threading
from tkinter import filedialog, Toplevel, Label, Button, Text, Scrollbar, END, StringVar, messagebox, IntVar, Entry, Checkbutton, Frame
from tkinter.ttk import Progressbar
from utils import dividir_arquivo_excel, abrir_diretorio
import queue

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Divisor de Arquivos Excel")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")
        self.root.deiconify()  # Garante que a janela seja exibida

        self.running = False
        self.queue = queue.Queue()

        self.max_linhas_var = IntVar(value=1000)
        self.manter_formatacao_var = IntVar(value=1)
        self.clonar_cabecalho_var = IntVar(value=1)

        # ...existing code for UI components...

        self.atualizar_interface()

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if caminho_arquivo:
            self.queue.put(("log", f"Arquivo selecionado: {caminho_arquivo}"))
            threading.Thread(
                target=dividir_arquivo_excel,
                args=(
                    caminho_arquivo,
                    self.max_linhas_var.get(),
                    self.manter_formatacao_var.get(),
                    self.clonar_cabecalho_var.get(),
                    self.queue,
                ),
            ).start()
        else:
            self.queue.put(("log", "Nenhum arquivo selecionado."))

    def validar_max_linhas(self, event=None):
        try:
            valor = self.max_linhas_var.get()
            if valor <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror("Erro de Validação", "Por favor, insira um número inteiro positivo.")
            self.max_linhas_var.set(1000)

    def iniciar_divisao(self):
        try:
            self.validar_max_linhas()
            self.selecionar_arquivo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar a divisão: {e}")

    def atualizar_interface(self):
        try:
            while not self.queue.empty():
                tipo, valor = self.queue.get(False)
                if tipo == "log":
                    self.log(valor)
                elif tipo == "progresso":
                    self.progress["value"] = valor
                    self.progress_label.config(text=f"Progresso: {int(valor)}%")
                elif tipo == "final":
                    self.exibir_dialogo_final(*valor)
        except queue.Empty:
            pass
        self.root.after(100, self.atualizar_interface)

    def exibir_dialogo_final(self, total_itens, total_tabelas, diretorio_saida):
        messagebox.showinfo(
            "Processamento Concluído",
            f"Quantidade total de linhas escaneadas: {total_itens}\n"
            f"Quantidade de tabelas geradas: {total_tabelas}\n\n"
            f"Os arquivos foram salvos no diretório:\n{diretorio_saida}"
        )
        abrir_diretorio(diretorio_saida)

    def log(self, mensagem):
        self.log_area.config(state="normal")
        self.log_area.insert(END, mensagem + "\n")
        self.log_area.see(END)
        self.log_area.config(state="disabled")
