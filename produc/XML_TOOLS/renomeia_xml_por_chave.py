import os
import xml.etree.ElementTree as ET
import time

# Diretório onde está o script
dir_script = os.path.dirname(os.path.abspath(__file__))

from dotenv import load_dotenv
load_dotenv()

pasta_raiz = os.getenv('ROOT_DIR')
pasta_ignorar = os.getenv('IGNORE_DIR', 'SCRIPTS')

ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
ignorados = []
erros = []

tempo_espera = 10
for i in range(tempo_espera, 0, -1):
    print(f"\rIniciando modificação em {i} segundos...", end='', flush=True)
    time.sleep(1)
print()

contador_renomeados = 0

inicio = time.time()
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
                tree = ET.parse(caminho_completo)
                infNFe = tree.find('.//nfe:infNFe', ns)
                if infNFe is None:
                    motivo = f'{caminho_completo} | Motivo: infNFe não encontrada'
                    ignorados.append(motivo)
                    print(motivo)
                    continue

                chave = infNFe.attrib.get('Id', '')[3:]
                if not chave.isdigit() or len(chave) != 44:
                    motivo = f'{caminho_completo} | Motivo: chave inválida'
                    ignorados.append(motivo)
                    print(motivo)
                    continue

                novo_nome = f'{chave}.xml'
                novo_caminho = os.path.join(root, novo_nome)

                if os.path.abspath(caminho_completo) == os.path.abspath(novo_caminho):
                    motivo = f'{caminho_completo} | Motivo: já está com o nome correto'
                    ignorados.append(motivo)
                    print(motivo)
                    continue

                i = 1
                while os.path.exists(novo_caminho):
                    novo_nome = f'{chave}_({i}).xml'
                    novo_caminho = os.path.join(root, novo_nome)
                    i += 1

                os.rename(caminho_completo, novo_caminho)
                print(f'Renomeado: {nome_arquivo} -> {novo_nome}')
                contador_renomeados += 1

            except Exception as e:
                erro_msg = f'{caminho_completo} | Erro: {str(e)}'
                erros.append(erro_msg)
                print(erro_msg)

fim = time.time()
tempo_decorrido = fim - inicio

# Salva log no diretório do script
log_path = os.path.join(dir_script, 'relatorio_ignorados.txt')
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('Arquivos ignorados:\n')
    for item in ignorados:
        f.write(f'{item}\n')
    f.write('\nArquivos com erro:\n')
    for item in erros:
        f.write(f'{item}\n')

# Resumo final
print('\nResumo:')
print(f'Total de XMLs processados: {contador_renomeados + len(ignorados) + len(erros)}')
print(f'Total renomeados: {contador_renomeados}')
print(f'Total ignorados: {len(ignorados)}')
print(f'Total com erro: {len(erros)}')
print(f'Arquivo de log gerado: {log_path}')
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
