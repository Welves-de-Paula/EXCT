import os
import shutil
import time

from dotenv import load_dotenv
load_dotenv()

pasta_raiz = os.getenv('ROOT_DIR')
pasta_ignorar = os.getenv('IGNORE_DIR', 'SCRIPTS')

tempo_espera = 10
for i in range(tempo_espera, 0, -1):
    print(f"\rIniciando modificação em {i} segundos...", end='', flush=True)
    time.sleep(1)
print()

contador_movidos = 0

inicio = time.time()
print("\n")
print("Processamento iniciado em:", time.strftime('%H:%M:%S', time.localtime(inicio)))
print("\n")

for root, dirs, files in os.walk(pasta_raiz, topdown=False):
    if pasta_ignorar in root.split(os.sep):
        continue
    for nome_arquivo in files:
        if nome_arquivo.lower().endswith('.xml'):
            caminho_atual = os.path.join(root, nome_arquivo)
            caminho_destino = os.path.join(pasta_raiz, nome_arquivo)
            if root != pasta_raiz:
                try:
                    os.rename(caminho_atual, caminho_destino)
                    print(f'MOVIDO: {caminho_atual} -> {caminho_destino}')
                    contador_movidos += 1
                except Exception as e:
                    print(f'Erro ao mover {caminho_atual}: {e}')

fim = time.time()
tempo_decorrido = fim - inicio

print("\n")
print(f'Total de arquivos movidos: {contador_movidos}')
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
