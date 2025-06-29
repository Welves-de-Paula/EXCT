import os
import re
import time
from lxml import etree
import sys

# Pasta dos XMLs

from dotenv import load_dotenv
load_dotenv()

pasta_raiz = os.getenv('ROOT_DIR')
pasta_ignorar = os.getenv('IGNORE_DIR', 'SCRIPTS')

nova_data = '2099-05-03T10:12:18-03:00'

# Remove prefixos ns0:, ns1:, ds:, etc.
def limpar_prefixos(xml_str):
    xml_str = re.sub(r'\sxmlns(:\w+)?="[^"]+"', '', xml_str)
    xml_str = re.sub(r'(<\/?)(\w+:)', r'\1', xml_str)
    xml_str = re.sub(r'(\s)(\w+:)(\w+=)', r'\1\3', xml_str)
    return xml_str

tempo_espera = 10
for i in range(tempo_espera, 0, -1):
    print(f"\rIniciando modificação em {i} segundos...", end='', flush=True)
    time.sleep(1)
print()  # quebra de linha após a contagem

contador_atualizados = 0  # contador de arquivos atualizados

inicio = time.time()  # marca o início do processamento
print("\n")
print("Processamento iniciado em:", time.strftime('%H:%M:%S', time.localtime(inicio)))
print("\n")

for root, dirs, files in os.walk(pasta_raiz, topdown=False):
    if pasta_ignorar in root.split(os.sep):
        continue

    for nome_arquivo in files:
        if nome_arquivo.lower().endswith('.xml'):
            caminho_completo = os.path.join(root, nome_arquivo)

            try:
                with open(caminho_completo, 'rb') as f:
                    conteudo = f.read()

                # Verifica se tem cabeçalho <?xml
                if b'<?xml' not in conteudo:
                    # Adiciona o cabeçalho no início do arquivo
                    conteudo = b'<?xml version="1.0" encoding="utf-8"?>\n' + conteudo
                    print(f'Adicionado cabeçalho XML em: {caminho_completo}')

                parser = etree.XMLParser(recover=True, remove_blank_text=True)
                root_xml = etree.fromstring(conteudo, parser=parser)

                # Altera o dhEmi (primeiro encontrado)
                for elem in root_xml.iter():
                    if elem.tag.endswith('dhEmi'):
                        elem.text = nova_data
                        break

                # Salva temporariamente
                temp_path = caminho_completo + '.tmp'
                etree.ElementTree(root_xml).write(temp_path, encoding='utf-8', xml_declaration=True, pretty_print=False)

                # Limpa os namespaces e salva final
                with open(temp_path, 'r', encoding='utf-8') as f:
                    xml_limpo = limpar_prefixos(f.read())

                with open(caminho_completo, 'w', encoding='utf-8') as f:
                    f.write(xml_limpo)

                os.remove(temp_path)
                print(f'PROCESSANDO: {caminho_completo}')
                contador_atualizados += 1  # incrementa o contador

            except Exception as e:
                print(f'Erro em {caminho_completo}: {e}')

fim = time.time()  # marca o fim do processamento
tempo_decorrido = fim - inicio

print("\n")

print(f'Total de arquivos atualizados: {contador_atualizados}')
print(f"Processamento concluído em {time.strftime('%H:%M:%S')}")

# Exibe o tempo decorrido em formato adequado
if tempo_decorrido < 60:
    print(f"Tempo decorrido: {tempo_decorrido:.2f} segundos")
elif tempo_decorrido < 3600:
    minutos = int(tempo_decorrido // 60)
    segundos = tempo_decorrido % 60
    print(f"Tempo decorrido: {minutos} minutos e {segundos:.2f} segundos")
else:
    horas = int(tempo_decorrido // 3600)
    minutos = int((tempo_decorrido % 3600) // 60)
    segundos = tempo_decorrido % 60
    print(f"Tempo decorrido: {horas} horas, {minutos} minutos e {segundos:.2f} segundos")

print("\n")



tempo_espera = 10
for i in range(tempo_espera, 0, -1):
    print(f"\rVoltando ao início em {i} segundos...", end='', flush=True)
    time.sleep(1)
print() 

