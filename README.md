# Atividade_API
.


O objetivo desta API é montar uma solução capaz de limpar imagens que se encontram com diversos ruídos.

Foi disponibilizado um dataset um imagens com ruído, para treinamento e limpas. Na verdade o dataset disponibilizado faz parte de uma competição do Kaggle de 2015 Denoise Dirty Documents.

Para esta atividade a API deverá receber uma imagem codificada em base64 e retornar a mesma imagem limpa tambem em base64, além de gravá-la em uma tabela de banco de dados.

Para desenvolver esta solução foram executados os seguintes passos:

1. Analise do dataset.
    O problema de remoção de ruído consiste em desenvolver algoritmos que "limpem" as imagens deterioradas por uma série de fatores desde manchas de escaneamento até manchas de fluídos e dobras de papel. A tarefa consiste em limpar imagens: remover as manchas; remover as dobras de papel; melhorar o contraste; e deixar somente o texto, o mais legível possível. Temos uma série de imagens de treinamento, constituídas de uma imagem “limpa” e uma onde um ruído foi adicionado artificialmente. 
    Outra caracteŕistica das imagens disponibilizadas é o tamanho, ou seja , para analise dos algoritmos de maquina , precisamos redimensiona-las.
    
2. Analise das frameworks necessarias:
    Para o desenvolvimento foi utilizada a linguagem Python.
    Para a API foi utilizada a biblioteca Flask e Flask_restfull
    Para o Banco de Dados foi utilizado o SQLite - devido a sua simplicidade e portabilidade
    Para acesso ao banco de dados foi utilizado o SQLAlchemy - todo o acesso ao banco sem necessidade de conhecimento de instruções SQL
    
3. Analise do metodo a ser utilizado para a limpeza das imagens
  Como foi um desafio lançado pelo Kaggle,vários metodos foram apresentados desde então. Desde metodos simples até os que utilizam e exigem muitos recursos de         maquina. Após analise e teste de alguns metodos, pude concluir o seguinte:
    3.1 Desde o desafio, até a presente data, novos modelos vem surgindo e aprimorando os resultados (Não poderia ser diferente)
    3.2 Metodos como filtro de Mediana, Autoencoder, detecção das bordas e regressão linear, cada um tem uma melhor atuação em determinado tipo de mancha. Havendo         a utilização de mais de um metodo para melhoria no resultado.
    3.3 Ha bibliografia que pretende estudar os efeitos da combinação de técnicas de processamento de imagens e redes neurais. Técnicas de processamento de imagem         como limiarização, filtragem, detecção de bordas, operações morfológicas, etc. são aplicadas a imagens de pré-processamento para render maior precisão             de modelos de rede neural.
    3.4 Então, por entender que, para esta solução seria melhor um metodo com necessidade de pouco recurso e que melhor executasse a função dentro de suas                 limitações, foi selecionado o metodo de Background. Subtraimos o fundo da imagem e retiramos o primeiro plano .
    

A estrutura do diretorio:

    Projeto ----- dataset --- decode64
                              limpa_base64
                              limpa_decode
                              limpa_geral
                              ruido_base64
                              test
                              train
                              train_cleaned
                              
                  main.py           - aplicação
                  banco.py          - cria a estrutura do banco, inclui e consulta registros
                  background.py     - executa a limpeza 
                  
Funcionalidade:
a API carrega um arquivo selecionado codificado em base64, executa a limpeza , retorna o arquivo limpo e grava a imagem em base64 no banco .
Para executar esta API com arquivos codificados em base64, os arquivos originais foram codificados e estão na pasta /Projeto/dataset/ruido_base64
A imagem que esta em /

a pasta Projeto/dataset/ruido_base64, os arquivos a serem enviados deverão ser codificados em base64. Para esta solução foi criada a pasta ruido_base64.
Os arquivos para upload estao na pasta Projeto/
Para e execução foram incluidos 3 metodos:
        http://127.0.0.1:5000/upload/  metodo POST   - upload 
                              
                  
    
