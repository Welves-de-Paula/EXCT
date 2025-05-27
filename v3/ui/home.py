import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
import sys  # Import garantido no topo
import logging
from openpyxl import load_workbook

# Importa o módulo de validação
from script import validate as validate_module


class HomeApp(tk.Tk):
    def __init__(self, excel_data, tipo):
        super().__init__()
        self.title('Assistente de Importação - Visualização de Dados')
        self.geometry('250x250')
        self.excel_data = excel_data
        self.tipo = tipo
        self.after_ids = []
        self.operacao_em_andamento = False
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.validation_errors = self.validar_linhas(excel_data, tipo)
        self.create_widgets()

    def validar_linhas(self, excel_data, tipo):
        rows = excel_data['rows']
        invalid_indices = set()
        for idx, row in enumerate(rows):
            errors = validate_module.validate(row, tipo, all_rows=rows)
            # print(errors)  # Log de erros para depuração
            if errors:
                invalid_indices.add(idx)
        return invalid_indices

    def create_widgets(self):
        # Corrigido: use 'label' e 'key' conforme o formato do reading.py
        headers = [h['label'] for h in self.excel_data['headers']]
        normalized_headers = [h['key'] for h in self.excel_data['headers']]
        rows = self.excel_data['rows']

        # Barra de busca (agora no topo)
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text='Buscar:').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.filtrar_tabela)

        # Botão para ordenar por erro
        self.erro_ordenado = False  # Estado da ordenação por erro
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=2)
        self.btn_erro = ttk.Button(
            btn_frame,
            text="Ordenar por Erros",
            command=self.toggle_erro_ordem
        )
        self.btn_erro.pack(side=tk.LEFT)

        # Frame para tabela (corrigido)
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Tabela
        self.tree = ttk.Treeview(
            frame, columns=normalized_headers, show='headings')
        self._sort_state = {}  # Armazena o estado de ordenação por coluna

        for idx, header in enumerate(headers):
            col_id = normalized_headers[idx]
            self.tree.heading(
                col_id,
                text=header,
                command=lambda c=col_id: self.sort_by_column(c)
            )
            self.tree.column(col_id, anchor=tk.CENTER, width=120)

        self._original_rows = list(rows)  # Guarda a ordem original
        self.populate_table(rows, normalized_headers)

        # Destacar cabeçalho, índice e linhas inválidas
        self.tree.tag_configure('invalid', background='#ffcccc')
        self.tree.tag_configure(
            'header_row', background='#e0e0e0', font=('Arial', 10, 'bold'))
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = ttk.Scrollbar(
            frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

    def toggle_erro_ordem(self):
        # Alterna entre ordenar por erro e restaurar ordem original
        headers = [h['key'] for h in self.excel_data['headers']]
        if not self.erro_ordenado:
            # Ordena: linhas inválidas primeiro
            rows = sorted(self._original_rows,
                          key=lambda r: not self.is_row_invalid(r))
            self.btn_erro.config(text="Restaurar Ordem")
            self.erro_ordenado = True
        else:
            # Restaura ordem original
            rows = list(self._original_rows)
            self.btn_erro.config(text="Ordenar por Erros")
            self.erro_ordenado = False
        self.populate_table(rows, headers)

    def populate_table(self, rows, normalized_headers):
        # Limpa e preenche a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Corrigir para lidar com linhas duplicadas
        original_rows = self.excel_data['rows']
        used_indices = set()
        for row in rows:
            values = [row.get(col, {}).get('value', '')
                      for col in normalized_headers]
            # Busca o índice da linha no conjunto original, considerando duplicatas
            idx_original = next((i for i, r in enumerate(original_rows)
                                 if r == row and i not in used_indices), None)
            if idx_original is not None:
                used_indices.add(idx_original)
            tags = []
            if idx_original in self.validation_errors:
                tags.append('invalid')
            if idx_original == 0:
                tags.append('header_row')
            self.tree.insert('', 'end', values=values, tags=tuple(tags))

    def sort_by_column(self, col):
        # Alterna entre ascendente e descendente
        rows = self.excel_data['rows']
        normalized_headers = [h['key'] for h in self.excel_data['headers']]
        reverse = self._sort_state.get(col, False)
        try:
            sorted_rows = sorted(
                rows,
                key=lambda r: (r.get(col, {}).get('value', '')
                               if r.get(col, {}) is not None else ''),
                reverse=reverse
            )
        except Exception:
            sorted_rows = rows  # fallback
        self._sort_state[col] = not reverse
        self.populate_table(sorted_rows, normalized_headers)

    def filtrar_tabela(self, event=None):
        filtro = self.search_var.get().lower()
        headers = [h['key'] for h in self.excel_data['headers']]
        filtered_rows = []
        for i, row in enumerate(self.excel_data['rows']):
            values = [row.get(col, {}).get('value', '') for col in headers]
            if filtro in ' '.join(values).lower():
                filtered_rows.append(row)
        self.populate_table(filtered_rows, headers)

    def is_row_invalid(self, row):
        # Considera inválido se o índice da linha estiver em self.validation_errors
        idx = self.excel_data['rows'].index(row)
        return idx in self.validation_errors

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


def abrir_home_com_dados(excel_data, tipo):
    app = HomeApp(excel_data, tipo)
    app.mainloop()

# Exemplo de uso:
# from script.reading import read_excel
# excel_data = read_excel('data/origin/SEU_ARQUIVO.xlsx')
# abrir_home_com_dados(excel_data)
