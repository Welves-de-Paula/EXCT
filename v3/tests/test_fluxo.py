# Teste de integração do fluxo principal do assistente
import unittest
import os
from script.store import store
from script.reading import read_excel
from script.identifier import identify_table_type
from script.validate import validate_rows
from script.split import split_excel
from script.compare import compare_data

class TestFluxoPrincipal(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join(os.path.dirname(__file__), '../data/origin/teste.xlsx')
        # Aqui você pode criar um arquivo Excel de teste usando pandas se desejar

    def test_fluxo_completo(self):
        # Simula o fluxo: store -> read -> identify -> validate -> split -> compare
        store(self.test_file, 'origin')
        headers, data = read_excel(self.test_file)
        tipo = identify_table_type(headers, '../rules/product.py', '../rules/customer.py')
        data_dicts = [dict(zip(headers, row)) for row in data]
        erros = validate_rows(data_dicts)
        output_dir = os.path.join(os.path.dirname(__file__), '../data/output')
        arquivos = split_excel(self.test_file, output_dir, linhas_por_parte=2)
        duplicados, exclusivos1, exclusivos2 = compare_data(self.test_file, self.test_file)
        self.assertIn(tipo, ['produtos', 'clientes', 'desconhecido'])
        self.assertIsInstance(erros, list)
        self.assertTrue(len(arquivos) > 0)
        self.assertIsInstance(duplicados, list)

if __name__ == '__main__':
    unittest.main()
