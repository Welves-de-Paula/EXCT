import os
import shutil
import xml.etree.ElementTree as ET
import time

from dotenv import load_dotenv
load_dotenv()

pasta_raiz = os.getenv('ROOT_DIR')
pasta_ignorar = os.getenv('IGNORE_DIR', 'SCRIPTS')

# Namespace NFe
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

def formatar_cpf(cpf: str) -> str:
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}' if len(cpf) == 11 else cpf

def formatar_cnpj(cnpj: str) -> str:
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}-{cnpj[8:12]}-{cnpj[12:]}' if len(cnpj) == 14 else cnpj

def esta_vazia(pasta: str) -> bool:
    return not any(os.scandir(pasta))

tempo_espera = 10
for i in range(tempo_espera, 0, -1):
    print(f"\rIniciando modificação em {i} segundos...", end='', flush=True)
    time.sleep(1)
print()

contador_organizados = 0

inicio = time.time()
print("\n")
print("Processamento iniciado em:", time.strftime('%H:%M:%S', time.localtime(inicio)))
print("\n")

# Percorre todos os arquivos e pastas
for root, dirs, files in os.walk(pasta_raiz, topdown=False):
    if pasta_ignorar in root.split(os.sep):
        continue

    for nome_arquivo in files:
        if nome_arquivo.lower().endswith('.xml'):
            caminho_completo = os.path.join(root, nome_arquivo)
            try:
                # Verifica e insere cabeçalho XML se necessário
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()

                if not conteudo.strip().startswith('<?xml'):
                    conteudo = '<?xml version="1.0" encoding="utf-8"?>\n' + conteudo
                    with open(caminho_completo, 'w', encoding='utf-8') as f:
                        f.write(conteudo)
                    print(f'Cabeçalho XML adicionado: {caminho_completo}')

                tree = ET.parse(caminho_completo)
                root_xml = tree.getroot()

                # Tenta localizar <dest> com e sem namespace
                dest = root_xml.find('.//nfe:dest', ns)
                if dest is None:
                    dest = root_xml.find('.//dest')

                identificador = 'CONSUMIDOR FINAL'

                if dest is not None:
                    cnpj_tag = dest.find('nfe:CNPJ', ns)
                    if cnpj_tag is None:
                        cnpj_tag = dest.find('CNPJ')

                    cpf_tag = dest.find('nfe:CPF', ns)
                    if cpf_tag is None:
                        cpf_tag = dest.find('CPF')

                    if cnpj_tag is not None and cnpj_tag.text:
                        identificador = formatar_cnpj(cnpj_tag.text.strip())
                    elif cpf_tag is not None and cpf_tag.text:
                        identificador = formatar_cpf(cpf_tag.text.strip())

                pasta_destino = os.path.join(pasta_raiz, identificador)
                os.makedirs(pasta_destino, exist_ok=True)

                novo_caminho = os.path.join(pasta_destino, nome_arquivo)

                # Evita sobrescrever
                i = 1
                base_nome, ext = os.path.splitext(nome_arquivo)
                while os.path.exists(novo_caminho):
                    novo_caminho = os.path.join(pasta_destino, f"{base_nome}_{i}{ext}")
                    i += 1

                shutil.move(caminho_completo, novo_caminho)
                print(f'Movido: {caminho_completo} -> {novo_caminho}')

                contador_organizados += 1

            except Exception as e:
                print(f'Erro ao processar {caminho_completo}: {e}')

    # Remove pastas vazias
    if root != pasta_raiz and root.split(os.sep)[-1] != pasta_ignorar and esta_vazia(root):
        try:
            os.rmdir(root)
            print(f'Pasta removida: {root}')
        except Exception as e:
            print(f'Erro ao remover pasta {root}: {e}')

fim = time.time()
tempo_decorrido = fim - inicio

print("\n")
print(f'Total de arquivos organizados: {contador_organizados}')
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
