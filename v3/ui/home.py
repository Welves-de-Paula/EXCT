import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
import sys  # Import garantido no topo
import logging
from openpyxl import load_workbook

class HomeApp(tk.Tk):
    def __init__(self, excel_data):
        # print(excel_data)
        # prinr nos headers
        print(excel_data['headers'])
        super().__init__()
        self.title('Assistente de Importação - Visualização de Dados')
        self.geometry('1000x600')
        self.excel_data = excel_data
        self.after_ids = []  # Lista para armazenar IDs de callbacks after
        self.operacao_em_andamento = False  # Flag para operações longas
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        headers = [h['name'] for h in self.excel_data['headers']]
        normalized_headers = [h['value'] for h in self.excel_data['headers']]
        rows = self.excel_data['rows']

        # Frame para tabela
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Tabela
        self.tree = ttk.Treeview(frame, columns=normalized_headers, show='headings')
        for idx, header in enumerate(headers):
            self.tree.heading(normalized_headers[idx], text=header)
            self.tree.column(normalized_headers[idx], anchor=tk.CENTER, width=120)

        # Inserir dados
        for i, row in enumerate(rows):
            values = [row.get(col, '') for col in normalized_headers]
            tag = 'invalid' if self.is_row_invalid(row) else ''
            # Destaca a primeira coluna (índice) usando tag
            if i == 0:
                tag = tag + ' header_row'
            self.tree.insert('', 'end', values=values, tags=(tag,))

        # Destacar cabeçalho, índice e linhas inválidas
        self.tree.tag_configure('invalid', background='#ffcccc')
        self.tree.tag_configure('header_row', background='#e0e0e0', font=('Arial', 10, 'bold'))
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Busca e filtro (campo de busca)
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text='Buscar:').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.filtrar_tabela)

    def filtrar_tabela(self, event=None):
        filtro = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        headers = [h['value'] for h in self.excel_data['headers']]
        for i, row in enumerate(self.excel_data['rows']):
            values = [row.get(col, '') for col in headers]
            if filtro in ' '.join(values).lower():
                tag = 'invalid' if self.is_row_invalid(row) else ''
                if i == 0:
                    tag = tag + ' header_row'
                self.tree.insert('', 'end', values=values, tags=(tag,))

    def is_row_invalid(self, row):
        # Exemplo: considere inválido se algum campo estiver vazio
        return any(v == '' for v in row.values())

    def safe_after(self, delay, callback):
        # Agendamento seguro de callbacks
        if self.winfo_exists():
            after_id = self.after(delay, callback)
            self.after_ids.append(after_id)
            return after_id
        return None

    def cancel_all_after(self):
        # Cancela todos os callbacks agendados
        for after_id in self.after_ids:
            try:
                self.after_cancel(after_id)
            except Exception:
                pass
        self.after_ids.clear()

    def on_closing(self):
        if self.operacao_em_andamento:
            if not messagebox.askyesno("Confirmação", "Uma operação está em andamento. Deseja realmente fechar e cancelar?"):
                return
        self.cancel_all_after()
        self.destroy()

# Função para abrir a tela Home com os dados lidos

def abrir_home_com_dados(excel_data):
    app = HomeApp(excel_data)
    app.mainloop()

# Exemplo de uso:
# from script.reading import read_excel
# excel_data = read_excel('data/origin/SEU_ARQUIVO.xlsx')
# abrir_home_com_dados(excel_data)
