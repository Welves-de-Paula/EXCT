import os
import json
import xml.etree.ElementTree as ET
import time

from dotenv import load_dotenv
load_dotenv()

pasta_raiz = os.getenv('ROOT_DIR')
pasta_ignorar = os.getenv('IGNORE_DIR', 'SCRIPTS')
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

produtos = {}

def extrair_produtos_de_xml(caminho_xml):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        infNFe = root.find('.//nfe:infNFe', ns)
        if infNFe is None:
            return

        for det in infNFe.findall('.//nfe:det', ns):
            prod = det.find('nfe:prod', ns)
            imposto = det.find('nfe:imposto', ns)
            icms = imposto.find('nfe:ICMS', ns) if imposto is not None else None

            cst = ''
            csosn = ''
            if icms is not None and len(icms):
                icms_tipo = list(icms)[0]
                cst = icms_tipo.findtext('nfe:CST', default='', namespaces=ns)
                csosn = icms_tipo.findtext('nfe:CSOSN', default='', namespaces=ns)

            codigo_barras = prod.findtext('nfe:cEAN', default='', namespaces=ns)
            if not codigo_barras:
                # Se não tem código de barras, cria uma chave genérica com código + descrição
                codigo_barras = f"SEM_CODBARRAS_{prod.findtext('nfe:cProd', default='', namespaces=ns)}"

            quantidade_str = prod.findtext('nfe:qCom', default='0', namespaces=ns)
            try:
                quantidade = float(quantidade_str)
            except:
                quantidade = 0

            if codigo_barras in produtos:
                # Soma quantidade se já existe
                produtos[codigo_barras]['quantidade'] += quantidade
            else:
                item = {
                    'codigo': prod.findtext('nfe:cProd', default='', namespaces=ns),
                    'descricao': prod.findtext('nfe:xProd', default='', namespaces=ns),
                    'quantidade': quantidade,
                    'unidade': prod.findtext('nfe:uCom', default='', namespaces=ns),
                    'valor_unitario': prod.findtext('nfe:vUnCom', default='', namespaces=ns),
                    'valor_total': prod.findtext('nfe:vProd', default='', namespaces=ns),
                    'codigo_barras': codigo_barras,
                    'ncm': prod.findtext('nfe:NCM', default='', namespaces=ns),
                     'cst': cst,
                    'csosn': csosn,
                    'unidade_tributavel': prod.findtext('nfe:uTrib', default='', namespaces=ns),
                    'valor_unitario_tributavel': prod.findtext('nfe:vUnTrib', default='', namespaces=ns),
                }
                produtos[codigo_barras] = item
    except Exception as e:
        print(f'Erro ao processar {caminho_xml}: {e}')

def processar_todos_os_xmls():
    for root, dirs, files in os.walk(pasta_raiz):
        for file in files:
            if file.lower().endswith('.xml'):
                caminho_xml = os.path.join(root, file)
                extrair_produtos_de_xml(caminho_xml)

if __name__ == '__main__':
    tempo_espera = 10
    for i in range(tempo_espera, 0, -1):
        print(f"\rIniciando modificação em {i} segundos...", end='', flush=True)
        time.sleep(1)
    print()

    contador_extraidos = 0

    inicio = time.time()
    print("\n")
    print("Processamento iniciado em:", time.strftime('%H:%M:%S', time.localtime(inicio)))
    print("\n")

    processar_todos_os_xmls()

    dir_script = os.path.dirname(os.path.abspath(__file__))
    caminho_saida = os.path.join(dir_script, 'produtos.json')

    # produtos é dicionário, precisa salvar só os valores
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(list(produtos.values()), f, ensure_ascii=False, indent=2)

    fim = time.time()
    tempo_decorrido = fim - inicio

    print(f'{len(produtos)} produtos únicos salvos em {caminho_saida}')
    print("\n")
    print(f'Total de arquivos processados: {contador_extraidos}')
    print(f"Processamento concluído em {time.strftime('%H:%M:%S')}")
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
