import unittest
import os
import pandas as pd
from script.reading import read_excel
from script.validate import validate_rows
from script.split import split_excel
from script.compare import compare_data

class TestAssistenteImportacao(unittest.TestCase):
    def setUp(self):
        # Cria um arquivo Excel de teste temporário
        self.test_file = os.path.join(os.path.dirname(__file__), '../data/origin/teste.xlsx')
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        df = pd.DataFrame({
            'NOME': ['João', 'Maria', 'José'],
            'CPF': ['12345678901', '23456789012', '34567890123'],
            'EMAIL': ['joao@email.com', 'maria@email.com', 'jose@email.com']
        })
        df.to_excel(self.test_file, index=False)

    def tearDown(self):
        # Remove o arquivo de teste após os testes
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_read_excel(self):
        # Testa leitura de arquivo Excel
        headers, data = read_excel(self.test_file)
        self.assertIsInstance(headers, list)
        self.assertIsInstance(data, list)
        self.assertIn('NOME', headers)

    def test_validate_rows(self):
        # Testa validação de dados
        headers, data = read_excel(self.test_file)
        data_dicts = [dict(zip(headers, row)) for row in data]
        errors = validate_rows(data_dicts)
        self.assertIsInstance(errors, list)

    def test_split_excel(self):
        # Testa divisão de arquivo
        output_dir = os.path.join(os.path.dirname(__file__), '../data/output')
        arquivos = split_excel(self.test_file, output_dir, linhas_por_parte=2)
        self.assertTrue(len(arquivos) > 0)
        # Limpa arquivos gerados
        for arq in arquivos:
            if os.path.exists(arq):
                os.remove(arq)

    def test_compare_data(self):
        # Testa comparação de arquivos
        duplicados, exclusivos1, exclusivos2 = compare_data(self.test_file, self.test_file)
        self.assertIsInstance(duplicados, list)
        self.assertIsInstance(exclusivos1, list)
        self.assertIsInstance(exclusivos2, list)

if __name__ == '__main__':
    unittest.main()
