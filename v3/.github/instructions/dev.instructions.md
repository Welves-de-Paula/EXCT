---
applyTo: "**"
---

name: "Instruções de Desenvolvimento do Assistente de Importação"

1 . **Introdução**

- O Assistente de Importação é uma ferramenta desenvolvida para facilitar a importação de dados de arquivos Excel para o sistema EXCT.
- O assistente é dividido em várias etapas, cada uma responsável por uma parte do processo de importação.
  2 . **Estrutura do Projeto**
- O projeto é organizado em várias pastas e arquivos, cada um com uma função específica.
- A pasta `rules` contém os arquivos de regras que definem como os dados devem ser importados.
- A pasta `data` contém os arquivos de origem, saída, logs e o de comparação que será utilizado na validação de duplicidade.
- A pasta `scripts` contém os scripts que realizam as operações de leitura, validação, identificação e importação, divisão de dados, entre outros.
- A pasta `ui` contém os arquivos de interface do usuário, incluindo o arquivo principal `ui/home.py`.

obs: alguns arquivos citados já existem, e possuem alumas partes já escritas, mas não estão completas, o assistente deve ser desenvolvido a partir do zero, mas utilizando os arquivos já existentes como base, e completando as partes que faltam, exceto os arquivo de regras que devem permanecer inalterados

3 . **Fluxo de Execução**

- O fluxo de execução do assistente é o seguinte:

  1. O usuário seleciona um arquivo Excel na interface do usuário, que é o `start.py` (responsável por abrir o gerenciador de arquivos).
  2. Após a seleção do arquivo, o deve criar uma cópia do arquivo na pasta `data/origin` com o nome do arquivo original, (use o script `script/store.py`).
  3. Após a cópia do arquivo, o assistente deve fechar a tela `start.py` e abrir a tela `ui/home.py`.
  4. O assistente deve ler o arquivo Excel na pasta `data/origin` usando o script `script/reading.py`.
  5. Após a leitura do arquivo, o assistente deve identificar se o arquivo é compatível ou não usando o script `script/identifier.py`, que compara as colunas e os rótulos do arquivo lido com os arquivos de regras `rules/customer.py` e `rules/product.py`.
  6. Se o arquivo for incompatível, o assistente deve exibir uma mensagem de erro usando o script `script/incompatible.py` e fornecer um botão para sair.
  7. Se o arquivo for compatível, o assistente deve validar os dados do arquivo lido com as regras de validação do arquivo de regras usando o script `script/validate.py`.
  8. Exiba os lidos e validados na tela `ui/home.py` usando uma tabela, onde o usuário pode visualizar os dados lidos e validados, realizar buscas e aplicar filtros e correções, na tabela onde os dados forem exibidos destaque a primeira linha (cabeçalho) e a primeira coluna (índice) para facilitar a visualização e as linhas que estão invalidas.
  9. Caso o usuário deseje, ele pode compara os dados lidos com os dados do arquivo de comparação (que será utilizado para validação de duplicidade) usando o script `script/compare.py`, para iso o assistente deve abrir uma tela de seleção de arquivo, copiar o arquivo selecionado para a pasta `data/compare` e realizar a comparação, exibindo os resultados em uma tabela na tela `ui/home.py`.
  10. Após a validação, o usuário pode optar por dividir os dados em partes menores, para isso o assistente deve abrir uma pop-up com as opções de divisão, onde o usuário pode escolher o número de linhas por parte, se deseja manter o cabeçalho e formatação do arquivo original, e o assistente deve usar o script `script/split.py` para dividir os dados em partes menores, antes da divisão o assistente solicitar o diretório onde o arquivo será salvo, o assistente deve criar uma cópia do arquivo original na pasta `data/output` com o nome do arquivo de saída e o diretório onde o arquivo será salvo.
  11. O nome do arquivo de saída deve ser o mesmo nome do arquivo original, mas com a extensão `.xlsx` e o sufixo `_[número da parte]` adicionado ao nome do arquivo, por exemplo, `arquivo_1.xlsx`, `arquivo_2.xlsx`, etc.
  12. Após a divisão, o assistente deve exibir uma mensagem de sucesso informando que os arquivos foram salvos na pasta `data/output` e o diretório onde os arquivos foram salvos.
  13. durante o processo de importação, o assistente deve registrar todas as operações realizadas em um arquivo de log na pasta `data/logs`, incluindo informações sobre o arquivo lido, os dados validados, os dados comparados e os arquivos divididos.
  14. O assistente deve ser capaz de lidar com erros e exceções, exibindo mensagens de erro apropriadas e permitindo que o usuário saia do assistente ou tente novamente.
  15. O assistente deve ser desenvolvido em Python e utilizar bibliotecas como `pandas`, `openpyxl`, `tkinter` e `os` para realizar as operações necessárias.
  16. O assistente deve ser testado em windows e deve ser compatível com versões recentes do Python (3.7 ou superior).
  17. O assistente deve ser documentado com comentários claros e concisos, explicando o funcionamento de cada parte do código e as bibliotecas utilizadas.
  18. O assistente deve ser desenvolvido seguindo as boas práticas de programação, incluindo a utilização de funções, classes e módulos para organizar o código e facilitar a manutenção.
  19. O assistente deve ser desenvolvido de forma modular, permitindo que novas funcionalidades sejam adicionadas facilmente no futuro.
  20. O assistente deve ser desenvolvido com foco na usabilidade, garantindo que a interface do usuário seja intuitiva e fácil de usar.
  21. O assistente deve ser desenvolvido com foco na performance, garantindo que as operações sejam realizadas de forma rápida e eficiente, mesmo com arquivos grandes.
  22. O assistente deve ser desenvolvido com foco na segurança, garantindo que não haja inconsistência nos dados e que os arquivos sejam manipulados de forma segura.
  23. O assistente deve ser desenvolvido com foco na escalabilidade, garantindo que o código seja capaz de lidar com grandes volumes de dados e que as operações sejam realizadas de forma eficiente.
  24. O assistente deve ser desenvolvido com foco de um executável, garantindo que o código seja capaz de ser executado em qualquer máquina sem a necessidade de instalação de dependências.
  25. durante os processos de leitura, validação, comparação e divisão de dados, o assistente deve exibir uma barra de progresso na tela `ui/home.py`, informando o usuário sobre o andamento das operações, essa barra de progresso deve ser atualizada em tempo real e deve ser capaz de lidar com operações longas, permitindo que o usuário saiba que o assistente está em execução e não travou.
  26. Quando o assistente for fechado, ele deve deletar os arquivos temporários criados durante o processo de importação, incluindo os arquivos de origem, saída e comparação, para garantir que não haja arquivos desnecessários ocupando espaço no disco.
  27. Se o assistente for fechado antes do término de uma operação, ele deve exibir uma mensagem de confirmação perguntando se o usuário deseja realmente fechar o assistente e cancelar a operação em andamento.
  28. Realizar testes unitários para garantir que cada parte do código funcione corretamente e que não haja erros ou exceções durante a execução do assistente.
  29. O assistente deve ser desenvolvido seguindo as boas práticas de programação, incluindo a utilização de funções, classes e módulos para organizar o código e facilitar a manutenção.

4 . **Requisitos**

- Python 3.7 ou superior
- Bibliotecas: `pandas`, `openpyxl`, `tkinter`, `os`, `logging`
