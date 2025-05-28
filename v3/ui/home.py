import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
import sys
import logging
from openpyxl import load_workbook

from script import validate as validate_module


class HomeApp(ctk.CTk):
    def __init__(self, excel_data, tipo):
        super().__init__()
        self.title('Assistente de Importação - Visualização de Dados')
        self.geometry('800x600')
        self.excel_data = excel_data
        self.tipo = tipo
        self.after_ids = []
        self.operacao_em_andamento = False
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.validation_errors = self._get_invalid_row_indices()
        self._sort_state = {}
        self.erro_ordenado = False
        self._original_rows = list(self.excel_data['rows'])
        self._setup_ui()

    def _get_invalid_row_indices(self):
        """Valida todas as linhas e retorna índices das inválidas."""
        rows = self.excel_data['rows']
        invalid_indices = set()
        for idx, row in enumerate(rows):
            errors = validate_module.validate(row, self.tipo, all_rows=rows)
            if errors:
                invalid_indices.add(idx)
        return invalid_indices

    def _setup_ui(self):
        """Cria e organiza os widgets da interface."""
        self._create_search_bar()
        self._create_error_sort_button()
        self._create_table_frame()

    def _create_search_bar(self):
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(search_frame, text='Buscar:').pack(side="left")
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind('<KeyRelease>', self._on_search)

    def _create_error_sort_button(self):
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=2)
        self.btn_erro = ctk.CTkButton(
            btn_frame,
            text="Ordenar por Erros",
            command=self._toggle_error_sort
        )
        self.btn_erro.pack(side="left")

    def _create_table_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        headers = [h['label'] for h in self.excel_data['headers']]
        normalized_headers = [h['key'] for h in self.excel_data['headers']]

        # Estilo para cabeçalho em negrito
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        self.tree = ttk.Treeview(
            frame, columns=normalized_headers, show='headings'
        )
        # Dicionário para armazenar larguras das colunas
        self._col_widths = {col_id: 120 for col_id in normalized_headers}

        def on_column_resize(event):
            # Atualiza o dicionário de larguras ao redimensionar
            for col_id in normalized_headers:
                self._col_widths[col_id] = self.tree.column(col_id, width=None)
            # Reaplica as larguras para manter as outras colunas fixas
            for col_id, width in self._col_widths.items():
                self.tree.column(col_id, width=width)

        self.tree.bind('<ButtonRelease-1>', on_column_resize)

        for idx, header in enumerate(headers):
            col_id = normalized_headers[idx]
            self.tree.heading(
                col_id,
                text=header,
                command=lambda c=col_id: self._sort_by_column(c)
            )
            self.tree.column(col_id, anchor="center", width=120)
        self.tree.tag_configure('invalid', background='#ffcccc')
        self.tree.tag_configure(
            'header_row', background='#e0e0e0')  # Removido o font bold aqui
        self.tree.pack(fill="both", expand=True)
        scrollbar_y = ctk.CTkScrollbar(
            frame, orientation="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ctk.CTkScrollbar(
            frame, orientation="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        self._populate_table(self._original_rows, normalized_headers)

    def _toggle_error_sort(self):
        headers = [h['key'] for h in self.excel_data['headers']]
        if not self.erro_ordenado:
            rows = sorted(self._original_rows,
                          key=lambda r: not self._is_row_invalid(r))
            self.btn_erro.configure(text="Restaurar Ordem")
            self.erro_ordenado = True
        else:
            rows = list(self._original_rows)
            self.btn_erro.configure(text="Ordenar por Erros")
            self.erro_ordenado = False
        self._populate_table(rows, headers)

    def _populate_table(self, rows, normalized_headers):
        self.tree.delete(*self.tree.get_children())
        original_rows = self.excel_data['rows']
        used_indices = set()
        for row in rows:
            values = [row.get(col, {}).get('value', '')
                      for col in normalized_headers]
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

    def _sort_by_column(self, col):
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
            sorted_rows = rows
        self._sort_state[col] = not reverse
        self._populate_table(sorted_rows, normalized_headers)

    def _on_search(self, event=None):
        filtro = self.search_var.get().lower()
        headers = [h['key'] for h in self.excel_data['headers']]
        filtered_rows = []
        for row in self.excel_data['rows']:
            values = [row.get(col, {}).get('value', '') for col in headers]
            if filtro in ' '.join(values).lower():
                filtered_rows.append(row)
        self._populate_table(filtered_rows, headers)

    def _is_row_invalid(self, row):
        idx = self.excel_data['rows'].index(row)
        return idx in self.validation_errors

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
        if self.operacao_em_andamento:
            if not messagebox.askyesno("Confirmação", "Uma operação está em andamento. Deseja realmente fechar e cancelar?"):
                return
        self.cancel_all_after()
        self.destroy()


def abrir_home_com_dados(excel_data, tipo):
    app = HomeApp(excel_data, tipo)
    app.mainloop()
