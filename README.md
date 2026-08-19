# TrabalhoPos

Repositório com dois trabalhos da minha pós-graduação em **Ciências de Dados e Inteligência Artificial**. O objetivo deste repositório é mostrar como eu estruturo problemas, justifico escolhas metodológicas e transformo análise em entrega técnica reproduzível.

## Visão geral

Este projeto está dividido em duas frentes:

- **Trabalho 1 — Mineração de dados aplicada ao futebol**
- **Trabalho 2 — Aprendizado de máquina clássico aplicado a diagnóstico de diabetes**

Os dois trabalhos foram desenvolvidos em Python, com foco em análise exploratória, preparação de dados, modelagem e geração de relatórios.

## Trabalho 1 — Mineração de dados no futebol

Pasta: `trabalho 1/`

### Problema

Construir uma base analítica de jogadores a partir de múltiplas fontes e usá-la para identificar perfis e padrões de desempenho.

### O que foi feito

- Coleta e consolidação de dados do **FBRef** e do **Transfermarkt**
- Web scraping com `requests` e `BeautifulSoup`
- Limpeza, padronização e integração de dados
- Análise exploratória com visualizações
- Agrupamento de jogadores com **K-Means**
- Redução de dimensionalidade com **PCA**
- Geração de tabelas-resumo por cluster
- Classificação com métricas salvas em CSV

### Evidências do projeto

- Notebook principal: `trabalho 1/trabalho_mineracao_dados.ipynb`
- Notebook de resultados: `trabalho 1/trabalho_mineracao_dados_resultados.ipynb`
- Pipeline adicional: `trabalho 1/pipeline/trabalho_mineracao_dados.ipynb`
- Relatórios e figuras: `trabalho 1/relatorio/`
- Saídas principais:
  - `trabalho 1/dados/clusters_resumo.csv`
  - `trabalho 1/dados/metricas_classificacao.csv`
  - `trabalho 1/dados/dataset_final.csv`

### Destaques técnicos

- Integração de fontes diferentes com tratamento de inconsistências de dados
- Uso de **K-Means** para descoberta de perfis de jogadores
- Uso de **PCA** para visualização dos agrupamentos
- Organização de artefatos analíticos em notebooks, scripts e arquivos de saída

## Trabalho 2 — Classificação de diabetes

Pasta: `trabalho 2/`

### Problema

Comparar modelos clássicos de aprendizado de máquina para apoio ao diagnóstico precoce de diabetes, priorizando **recall** para reduzir falsos negativos.

### Modelos comparados

- Árvore de Decisão
- Naive Bayes Gaussiano
- K-Nearest Neighbors (KNN)

### O que foi feito

- Preparação de dados do dataset **Pima Indians Diabetes**
- Imputação de valores e uso de `Pipeline` para evitar vazamento de informação
- Validação cruzada estratificada com **10 folds**
- Otimização de hiperparâmetros com **GridSearchCV**
- Comparação de métricas: acurácia, precision, recall, F1 e AUC
- Avaliação final em hold-out
- Geração de resumo expandido em PDF

### Resultado principal

O modelo recomendado foi a **Árvore de Decisão**, com os seguintes resultados no hold-out:

- **Accuracy:** 0.792
- **Precision:** 0.696
- **Recall:** 0.722
- **F1-score:** 0.709
- **AUC:** 0.805
- **Falsos negativos:** 15

Hiperparâmetros selecionados:

- `criterion = gini`
- `max_depth = 4`
- `min_samples_leaf = 20`
- `min_samples_split = 2`

### Evidências do projeto

- Notebook principal: `trabalho 2/Caso_01_ML_Classico.ipynb`
- Script do experimento: `trabalho 2/experimento_diabetes.py`
- Geração do resumo: `trabalho 2/gerar_resumo_expandido.py`
- Resultados:
  - `trabalho 2/resultados/resumo_experimento.json`
  - `trabalho 2/resultados/metricas_holdout.csv`
  - `trabalho 2/resultados/metricas_cv_otimizados.csv`
  - `trabalho 2/resultados/melhores_hiperparametros.json`

### Destaques técnicos

- Escolha da métrica alinhada ao contexto de negócio: priorização de **recall**
- Comparação crítica entre modelos, em vez de uso automático do mais comum
- Preocupação com validade metodológica, incluindo pipeline e validação cruzada
- Tradução dos resultados para interpretação prática

## Stack utilizada

- **Python**
- **pandas**
- **numpy**
- **scikit-learn**
- **matplotlib**
- **seaborn**
- **BeautifulSoup**
- **requests**
- **fpdf / fpdf2**

## Como este repositório deve ser lido

Este não é um repositório de produto web; é um repositório de trabalho analítico e acadêmico. O principal valor aqui está em:

- como os dados foram estruturados;
- como as decisões metodológicas foram justificadas;
- como os resultados foram organizados para comunicação técnica.

Se quiser começar pelo material mais representativo:

1. Leia este `README`
2. Abra `trabalho 2/Caso_01_ML_Classico.ipynb`
3. Veja `trabalho 2/resultados/resumo_experimento.json`
4. Depois explore `trabalho 1/trabalho_mineracao_dados.ipynb`

## Autor

**Jesus Gabriel Leiva Conessa**  
GitHub: [@JesusGabriel4002](https://github.com/JesusGabriel4002)
