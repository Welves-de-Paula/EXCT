# Assistente de Importação EXCT

## Descrição
Ferramenta para importar, validar, comparar e dividir dados de arquivos Excel (.xlsx) para o sistema EXCT, com interface gráfica intuitiva e suporte a grandes volumes de dados.

## Estrutura do Projeto
- `rules/`: regras de validação para clientes e produtos.
- `data/`: arquivos de origem, saída, logs e comparação.
- `script/`: scripts de leitura, validação, identificação, comparação, divisão e armazenamento.
- `ui/`: interface gráfica (Tkinter).
- `tests/`: testes unitários automatizados.

## Requisitos
- Python 3.7+
- Bibliotecas: `pandas`, `openpyxl`, `tkinter`, `os`, `logging`

## Instalação
1. Instale as dependências:
   ```sh
   pip install pandas openpyxl
   ```
2. (Opcional) Para gerar executável:
   ```sh
   pip install pyinstaller
   pyinstaller --onefile --noconsole main.py
   ```

## Como usar
1. Execute o arquivo principal:
   ```sh
   python main.py
   ```
2. Siga o fluxo na interface:
   - Selecione o arquivo Excel.
   - Visualize, filtre, corrija e valide os dados.
   - Compare com outro arquivo, se desejar.
   - Divida em partes menores, se necessário.
   - Todas as operações são registradas em `data/logs/log.txt`.

## Testes
Execute todos os testes unitários:
```sh
python -m unittest discover -s tests
```

## Observações
- Todos os arquivos temporários são limpos ao fechar o assistente.
- O projeto é modular e fácil de manter/expandir.
- Para empacotar como executável, utilize o PyInstaller.

---
Desenvolvido seguindo as melhores práticas e as instruções do projeto.
