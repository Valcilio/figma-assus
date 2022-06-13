## Fonte dos Dados
Fonte de dados do BACEN (Não Acessível - API): [http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json](http://api.bcb.gov.br/dados/serie/bcdata.sgs.%7Bcodigo_bcb%7D/dados?formato=json)

Fonte de dados do Santander (Acessível - WebApp): <https://www.santander.com.br/analise-economica>
## Diagrama
![enter image description here](https://i.ibb.co/bNC3YYG/Doc-Diagrama-Indicadores-ETL.png)
## Explicando Arquivos de ETL
### Os principais arquivos do ETL são os seguintes:
- **notebooks** : contém o notebook do projeto.
  - **etl\_timeseries.ipynb** : arquivo notebook contendo todo o ETL em formato não-orientado a objeto, ideal para realizar testes.
- **reports** : contém o resultado final do notebook.
- **src** : contém os códigos usados no projeto.
  - **adj.py** : arquivo de integração das classes. É onde todas as classes são chamadas e possui as principais configurações de endereço.
  - **logger** : contém os códigos de log.
    - **logger\_msg.py** : código python contendo as bases dos alertas de log gerado que irão posteriormente aparecer na pasta "logs".
  - **etl** : contém os códigos do ETL orientados a objeto.
    - **bacen\_etl.py** : código python contendo as extrações e transformações dos dados do BACEN, PIB, IPCA alimentação e Custo Familiar.
    - **sant\_wg.py** : código python contendo os comandos de webscrapping, movimento e extração de zip dos dados do santander, trata de todo o processo de extração desses dados.
    - **santander\_etl.py** : código python contendo todas as transformações realizadas nos arquivos do santander que contém as projeções e dados já vigentes que o santander indica serem importantes para torná-los utilizáveis para futuras análises.
    - **data\_combine.py** : código python responsável por mesclar as bases de dados já limpas do BACEN e do Santander e salvar o conjunto final de dados.
## Observações Importantes:
1. É recomendado que sempre seja checado o arquivo excel do santander para haver o máximo de certeza de que os dados conferem.
1. O ETL, embora completo, precisa que o caminho de download do arquivo "src/adj.py" seja modificado para que seja possível mover o arquivo (ou não irá localizar o arquivo).
1. Todas os métodos das classes estão bem explicado com comentários nos próprios arquivos, caso deseje compreender para que cada um serve, basta abrir o arquivo e ler os comentários por código.
