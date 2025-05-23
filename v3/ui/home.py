import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
import sys  # Import garantido no topo
import logging
from openpyxl import load_workbook

def get_latest_file_from_origin():
    origin_dir = os.path.join(os.path.dirname(__file__), "..", "data", "origin")
    if not os.path.isdir(origin_dir):
        return None
    files = [os.path.join(origin_dir, f) for f in os.listdir(origin_dir) if os.path.isfile(os.path.join(origin_dir, f))]
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def main(filepath=None, title="Assistente de Importação"):
    # Configuração de logging
    logs_dir = os.path.join(os.path.dirname(__file__), "..", "data", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(logs_dir, "log.txt"), level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Se filepath não for passado, tenta pegar o arquivo mais recente de data/origin
    if filepath is None:
        filepath = get_latest_file_from_origin()

    file_content = ""
    table_data = []
    table_headers = []
    file_is_compatible = False  # Flag para compatibilidade

    # Variável para armazenar o resultado do identifier
    identifier_result = None

    if filepath and os.path.isfile(filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".xlsx":
            try:
                # Usa o script/reading.py para ler o arquivo Excel corretamente
                import importlib.util
                reading_path = os.path.join(os.path.dirname(__file__), "..", "script", "reading.py")
                spec = importlib.util.spec_from_file_location("reading", reading_path)
                reading = importlib.util.module_from_spec(spec)
                sys.modules["reading"] = reading
                spec.loader.exec_module(reading)
                table_headers, table_data = reading.read_excel(filepath)
                # Validação rigorosa do cabeçalho
                validate_path = os.path.join(os.path.dirname(__file__), "..", "script", "validate.py")
                spec = importlib.util.spec_from_file_location("validate", validate_path)
                validate = importlib.util.module_from_spec(spec)
                sys.modules["validate"] = validate
                spec.loader.exec_module(validate)
                table_type = validate.identify_table_type(table_headers)
                if table_type is None:
                    file_is_compatible = False
                    file_content = "Arquivo incompatível: o cabeçalho não corresponde exatamente ao layout esperado (Clientes ou Produtos).\n\nColunas encontradas:\n" + ", ".join(table_headers)
                else:
                    file_is_compatible = True
            except Exception as e:
                file_content = f"Erro ao ler arquivo Excel: {e}"
        else:
            file_content = "Arquivo não suportado. Por favor, utilize apenas arquivos .xlsx."

    # Se o arquivo não for compatível, abre o incompatible.py imediatamente
    if not file_is_compatible:
        import importlib.util
        incompatible_path = os.path.join(os.path.dirname(__file__), "incompatible.py")
        spec = importlib.util.spec_from_file_location("incompatible", incompatible_path)
        incompatible = importlib.util.module_from_spec(spec)
        import sys  # Garante que sys está disponível no escopo local
        sys.modules["incompatible"] = incompatible
        spec.loader.exec_module(incompatible)
        if hasattr(incompatible, "main"):
            incompatible.main(file_content or "Arquivo incompatível. Por favor, utilize apenas arquivos .xlsx válidos.")
        return  # Não segue para a interface principal

    def on_validar():
        print("Botão Validar clicado!")
        if filepath:
            print(f"Arquivo recebido: {filepath}")
        if file_is_compatible:            # Corrige o caminho do identifier.py para ../script/identifier.py
            identifier_path = os.path.join(os.path.dirname(__file__), "..", "script", "identifier.py")
            spec = importlib.util.spec_from_file_location("identifier", identifier_path)
            identifier = importlib.util.module_from_spec(spec)
            import sys  # Garante que sys está disponível no escopo local
            sys.modules["identifier"] = identifier
            spec.loader.exec_module(identifier)
            # Supondo que identifier.py tenha uma função 'main' que recebe headers e dados
            if hasattr(identifier, "main"):
                identifier.main(table_headers, table_data)
        else:
            # Abre incompatible.py com mensagem
            incompatible_path = os.path.join(os.path.dirname(__file__), "incompatible.py")
            spec = importlib.util.spec_from_file_location("incompatible", incompatible_path)
            incompatible = importlib.util.module_from_spec(spec)
            sys.modules["incompatible"] = incompatible
            spec.loader.exec_module(incompatible)
            # Supondo que incompatible.py tenha uma função 'main' que recebe uma mensagem
            if hasattr(incompatible, "main"):
                incompatible.main("Arquivo incompatível. Por favor, utilize apenas arquivos .xlsx válidos.")

    # Botão para comparar dados
    def on_comparar():
        compare_file = filedialog.askopenfilename(title="Selecione o arquivo para comparação", filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")])
        if compare_file:
            # Copia para data/compare
            store_path = os.path.join(os.path.dirname(__file__), "..", "script", "store.py")
            spec = importlib.util.spec_from_file_location("store", store_path)
            store = importlib.util.module_from_spec(spec)
            sys.modules["store"] = store
            spec.loader.exec_module(store)
            store.store(compare_file, "compare")
            # Chama script/compare.py
            compare_path = os.path.join(os.path.dirname(__file__), "..", "script", "compare.py")
            spec = importlib.util.spec_from_file_location("compare", compare_path)
            compare = importlib.util.module_from_spec(spec)
            sys.modules["compare"] = compare
            spec.loader.exec_module(compare)
            duplicados, exclusivos1, exclusivos2 = compare.compare_data(filepath, compare_file)
            # Exibe resultados em nova janela
            resultado_win = tk.Toplevel(root)
            resultado_win.title("Resultado da Comparação")
            resultado_win.geometry("900x600")
            tabs = ttk.Notebook(resultado_win)
            tabs.pack(fill="both", expand=True)
            def criar_tabela(tab, dados, titulo):
                frame = tk.Frame(tab)
                frame.pack(fill="both", expand=True)
                if not dados:
                    tk.Label(frame, text="Nenhum dado encontrado.").pack()
                    return
                tree = ttk.Treeview(frame, columns=table_headers, show="headings")
                for col in table_headers:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center")
                for row in dados:
                    tree.insert("", "end", values=row)
                tree.pack(fill="both", expand=True)
            tab1 = tk.Frame(tabs)
            tab2 = tk.Frame(tabs)
            tab3 = tk.Frame(tabs)
            tabs.add(tab1, text="Duplicados")
            tabs.add(tab2, text="Exclusivos Origem")
            tabs.add(tab3, text="Exclusivos Comparação")
            criar_tabela(tab1, duplicados, "Duplicados")
            criar_tabela(tab2, exclusivos1, "Exclusivos Origem")
            criar_tabela(tab3, exclusivos2, "Exclusivos Comparação")
            logging.info(f"Comparação realizada entre {filepath} e {compare_file}")

    # Botão para dividir dados
    def on_dividir():
        popup = tk.Toplevel()
        popup.title("Dividir Arquivo")
        tk.Label(popup, text="Linhas por parte:").pack()
        linhas_entry = tk.Entry(popup)
        linhas_entry.insert(0, "1000")
        linhas_entry.pack()
        manter_cabecalho = tk.BooleanVar(value=True)
        tk.Checkbutton(popup, text="Manter cabeçalho", variable=manter_cabecalho).pack()
        manter_formatacao = tk.BooleanVar(value=True)
        tk.Checkbutton(popup, text="Manter formatação", variable=manter_formatacao).pack()
        def executar_divisao():
            try:
                linhas = int(linhas_entry.get())
                output_dir = filedialog.askdirectory(title="Selecione o diretório de saída")
                if not output_dir:
                    return
                split_path = os.path.join(os.path.dirname(__file__), "..", "script", "split.py")
                spec = importlib.util.spec_from_file_location("split", split_path)
                split = importlib.util.module_from_spec(spec)
                sys.modules["split"] = split
                spec.loader.exec_module(split)
                arquivos = split.split_excel(filepath, output_dir, linhas, manter_cabecalho.get(), manter_formatacao.get())
                messagebox.showinfo("Divisão Concluída", f"Arquivos salvos em: {output_dir}\n{arquivos}")
                logging.info(f"Divisão realizada: {arquivos}")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao dividir arquivo: {e}")
                logging.error(f"Erro ao dividir arquivo: {e}")
        tk.Button(popup, text="Dividir", command=executar_divisao).pack(pady=10)

    # Estilo moderno para a interface
    root = tk.Tk()
    root.title(title)
    root.state('zoomed')
    root.configure(bg="#f5f6fa")
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
        background="#f5f6fa",
        foreground="#222",
        rowheight=28,
        fieldbackground="#f5f6fa",
        font=("Segoe UI", 11)
    )
    style.configure("Treeview.Heading",
        background="#1976d2",
        foreground="white",
        font=("Segoe UI", 12, "bold")
    )
    style.map("Treeview",
        background=[('selected', '#90caf9')],
        foreground=[('selected', '#222')]
    )
    style.configure("TButton",
        font=("Segoe UI", 11, "bold"),
        padding=8,
        background="#1976d2",
        foreground="white"
    )
    style.map("TButton",
        background=[('active', '#1565c0')],
        foreground=[('active', 'white')]
    )
    # Container centralizado
    container = tk.Frame(root, bg="#f5f6fa")
    container.pack(expand=True, fill="both")
    # Título
    tk.Label(container, text="Assistente de Importação", font=("Segoe UI", 22, "bold"), bg="#f5f6fa", fg="#1976d2").pack(pady=(20, 10))
    # Botões
    btn_frame = tk.Frame(container, bg="#f5f6fa")
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Validar", command=on_validar).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="Comparar Dados", command=on_comparar).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="Dividir Arquivo", command=on_dividir).pack(side="left", padx=8)
    # Correção manual de células
    def on_corrigir():
        # Busca o widget treeview criado em exibir_tabela
        for widget in display_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                tree = widget
                break
        else:
            messagebox.showwarning("Tabela", "Tabela não encontrada.")
            return
        item = tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione uma linha para corrigir.")
            return
        valores = tree.item(item, 'values')
        popup = tk.Toplevel()
        popup.title("Corrigir Dados")
        entries = []
        for i, (col, val) in enumerate(zip(table_headers, valores)):
            tk.Label(popup, text=col).grid(row=i, column=0)
            e = tk.Entry(popup)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries.append(e)
        def salvar():
            novos_valores = [e.get() for e in entries]
            tree.item(item, values=novos_valores)
            popup.destroy()
        tk.Button(popup, text="Salvar", command=salvar).grid(row=len(table_headers), column=0, columnspan=2)
    ttk.Button(btn_frame, text="Corrigir Seleção", command=on_corrigir, style="TButton").pack(side="left", padx=8)
    # Botão para testar barra de progresso
    ttk.Button(btn_frame, text="Testar Progresso", command=operacao_longa).pack(side="left", padx=8)
    # Busca
    search_frame = tk.Frame(container, bg="#f5f6fa")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Buscar:", font=("Segoe UI", 11), bg="#f5f6fa").pack(side="left")
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 11), width=30).pack(side="left", padx=5)
    # Barra de progresso
    progress = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(container, variable=progress, maximum=100, style="TProgressbar")
    progress_bar.pack(fill="x", padx=20, pady=10)
    # Área de exibição
    display_frame = tk.Frame(container, bg="#f5f6fa")
    display_frame.pack(fill="both", expand=True, padx=20, pady=10)
    # Rodapé
    tk.Label(root, text="© 2024 Assistente de Importação", font=("Segoe UI", 9), bg="#f5f6fa", fg="#888").pack(side="bottom", pady=8)

    # Função para atualizar a barra de progresso
    def atualizar_progresso(valor):
        progress.set(valor)
        root.update_idletasks()

    # Exemplo de uso da barra de progresso durante operações longas
    def operacao_longa():
        for i in range(101):
            atualizar_progresso(i)
            root.after(5)  # Simula processamento
        messagebox.showinfo("Concluído", "Operação longa finalizada!")
        atualizar_progresso(0)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    btn_validar = tk.Button(frame, text="Validar", command=on_validar)
    btn_validar.pack(side="left")

    # Correção manual de células
    def on_corrigir():
        # Busca o widget treeview criado em exibir_tabela
        for widget in display_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                tree = widget
                break
        else:
            messagebox.showwarning("Tabela", "Tabela não encontrada.")
            return
        item = tree.focus()
        if not item:
            messagebox.showwarning("Seleção", "Selecione uma linha para corrigir.")
            return
        valores = tree.item(item, 'values')
        popup = tk.Toplevel()
        popup.title("Corrigir Dados")
        entries = []
        for i, (col, val) in enumerate(zip(table_headers, valores)):
            tk.Label(popup, text=col).grid(row=i, column=0)
            e = tk.Entry(popup)
            e.insert(0, val)
            e.grid(row=i, column=1)
            entries.append(e)
        def salvar():
            novos_valores = [e.get() for e in entries]
            tree.item(item, values=novos_valores)
            popup.destroy()
        tk.Button(popup, text="Salvar", command=salvar).grid(row=len(table_headers), column=0, columnspan=2)
    tk.Button(btn_frame, text="Corrigir Seleção", command=on_corrigir, bg="#fbc02d", fg="black").pack(side="left", padx=5)

    # Exibe apenas mensagem de erro se houver, não exibe tabela
    display_frame = tk.Frame(root, padx=20, pady=20)
    display_frame.pack(fill="both", expand=True)

    if file_content:
        text_widget = tk.Text(display_frame, wrap="none")
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", file_content)
        text_widget.config(state="disabled")

    # Exemplo seguro de uso do after:
    def safe_after():
        if root.winfo_exists():
            # ...código que precisa ser executado periodicamente...
            root.after(100, safe_after)
    # safe_after()  # Descomente se precisar usar after

    # Após identificar o tipo de tabela, validar os dados
    validation_errors = []
    table_type = None
    if file_is_compatible and table_headers and table_data:
        # Importa validate.py dinamicamente
        import importlib.util
        import sys
        validate_path = os.path.join(os.path.dirname(__file__), "..", "script", "validate.py")
        spec = importlib.util.spec_from_file_location("validate", validate_path)
        validate = importlib.util.module_from_spec(spec)
        sys.modules["validate"] = validate
        spec.loader.exec_module(validate)
        # Identifica o tipo de tabela
        table_type = validate.identify_table_type(table_headers)
        if table_type == "customer":
            from rules.customer import RULES as RULES_TO_USE
        elif table_type == "product":
            from rules.product import RULES as RULES_TO_USE
        else:
            RULES_TO_USE = []
        # Monta os dados como lista de dicts para validação
        data_dicts = [dict(zip(table_headers, row)) for row in table_data]
        validation_errors = validate.validate_rows(data_dicts, rules=RULES_TO_USE)

    # Exibe a tabela com destaques
    def exibir_tabela():
        if not table_headers or not table_data:
            return
        tree = ttk.Treeview(display_frame, columns=table_headers, show="headings")
        for idx, col in enumerate(table_headers):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        # Destaca cabeçalho e índice
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#e0e0e0")
        # Adiciona linhas
        for i, row in enumerate(table_data):
            tags = []
            # Destaca linhas inválidas
            if any(err['row'] == i+1 for err in validation_errors):
                tags.append("invalid")
            tree.insert("", "end", values=row, tags=tags)
        tree.tag_configure("invalid", background="#ffcccc")
        tree.pack(fill="both", expand=True)

        # Busca e filtro na tabela
        search_var = tk.StringVar()
        def filtrar_tabela(*args):
            termo = search_var.get().lower()
            for item in tree.get_children():
                valores = tree.item(item, 'values')
                if any(termo in str(v).lower() for v in valores):
                    tree.reattach(item, '', 'end')
                else:
                    tree.detach(item)
        search_var.trace_add('write', filtrar_tabela)
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar:").pack(side="left")
        tk.Entry(search_frame, textvariable=search_var).pack(side="left")

    # Limpa widgets antigos e exibe tabela
    for widget in display_frame.winfo_children():
        widget.destroy()
    exibir_tabela()

    def on_close():
        if messagebox.askokcancel("Sair", "Deseja realmente sair e cancelar a operação em andamento?"):
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
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()