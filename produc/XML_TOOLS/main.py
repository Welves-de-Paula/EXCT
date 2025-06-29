# var .env
import os
import re
from lxml import etree
from dotenv import load_dotenv
load_dotenv()

import sys

try:
    import msvcrt
except ImportError:
    msvcrt = None

opcoes_menu = [
    "Alterar data de emissão (dhEmi)",
    "Extrair produtos de NFe",
    "Mover XMLs para raiz",
    "Ordenar XMLs por destinatário",
    "Ordenar XMLs por emitente",
    "Renomear XMLs por chave de acesso",
    "Sair"
]


# Limpa a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Menu interativo com setas (Windows) ou input manual (Linux/Mac)
def selecionar_opcao():
    idx = 0
    while True:
        limpar_tela()
        print("="*40)
        print("      FERRAMENTAS DE XML NFe")
        print("="*40)
        print("Use ↑/↓ para navegar e Enter para selecionar:\n")
        print("Pasta dos XMLs:", os.getenv('ROOT_DIR', 'Não definida'))
        for i, opcao in enumerate(opcoes_menu):
            if i == idx:
                print(f"> {opcao}")
            else:
                print(f"  {opcao}")
        print("-"*40)
        # Captura tecla
        if msvcrt:
            key = msvcrt.getch()
            if key == b'\xe0':  # Tecla especial (seta)
                key2 = msvcrt.getch()
                if key2 == b'H':  # Seta para cima
                    idx = (idx - 1) % len(opcoes_menu)
                elif key2 == b'P':  # Seta para baixo
                    idx = (idx + 1) % len(opcoes_menu)
            elif key == b'\r':  # Enter
                return str(idx + 1)
        else:
            # fallback para sistemas sem msvcrt (Linux/Mac)
            opcao = input("Digite o número da opção: ")
            return opcao


def main():
    # Validação do ROOT_DIR
    root_dir = os.getenv('ROOT_DIR')
    if not root_dir:
        print("\n")
        print("Erro: variável de ambiente ROOT_DIR não definida.")
        print("\n")
        print("Certifique-se de que a variável de ambiente ROOT_DIR está configurada corretamente.")
        print("Você pode definir ROOT_DIR no arquivo .env ou diretamente no ambiente.")
        sys.exit(1)
    if not os.path.isdir(root_dir):
        print("\n")
        print(f"Erro: diretório ROOT_DIR '{root_dir}' não existe.")
        print("\n")
        print("Certifique-se de que a variável de ambiente ROOT_DIR está configurada corretamente.")
        print("Você pode definir ROOT_DIR no arquivo .env ou diretamente no ambiente.")
        print("\n")
        sys.exit(1)

    try:
        while True:
            opcao = selecionar_opcao()
            limpar_tela()
            if opcao == '1':
                print("Você escolheu: Alterar data de emissão (dhEmi)\n")
                try:
                    import alterar_dhEmi
                except Exception as e:
                    print(f"Erro ao executar alterar_dhEmi: {e}")
            elif opcao == '2':
                print("Você escolheu: Extrair produtos de NFe\n")
                try:
                    import extrai_produtos_xml
                except Exception as e:
                    print(f"Erro ao executar extrai_produtos_xml: {e}")
            elif opcao == '3':
                print("Você escolheu: Mover XMLs para raiz\n")
                try:
                    import mover_xmls_para_raiz
                except Exception as e:
                    print(f"Erro ao executar mover_xmls_para_raiz: {e}")
            elif opcao == '4':
                print("Você escolheu: Ordenar XMLs por destinatário\n")
                try:
                    import organiza_xml_por_destinatario
                except Exception as e:
                    print(f"Erro ao executar organiza_xml_por_destinatario: {e}")
            elif opcao == '5':
                print("Você escolheu: Ordenar XMLs por emitente\n")
                try:
                    import organiza_xml_por_emitente
                except Exception as e:
                    print(f"Erro ao executar organiza_xml_por_emitente: {e}")
            elif opcao == '6':
                print("Você escolheu: Renomear XMLs por chave de acesso\n")
                try:
                    import renomeia_xml_por_chave
                except Exception as e:
                    print(f"Erro ao executar renomeia_xml_por_chave: {e}")
            elif opcao == '7':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário (Ctrl+C). Saindo...")

if __name__ == '__main__':
    main()




