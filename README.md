# Sprint 2 – Prototipagem e Aplicação de Business Analytics & Governança de IA

## Integrantes do Grupo

- **Herbertt Di Franco Marques:** RM556640
- **Sandron Oliveira Silva:** RM557172
- **Lorena Bauer Nogueira:** RM555272
- **Nickolas Ferraz:** RM558458
- **Paulo Carvalho:** RM554562
- **Marcos Paolucci Salamondac:** RM554941

## Objetivo

Este projeto visa transformar os insights sobre produtos falsificados em ações tangíveis, com foco na prototipagem de uma ferramenta analítica (dashboard), um modelo preditivo para detecção de fraudes e a elaboração de diretrizes práticas de governança de IA.

## Estrutura do Projeto

O repositório está organizado da seguinte forma:

- **/data**: Contém os dados sintéticos gerados (`synthetic_data.csv`) e o arquivo de mapa (`uf.json`).
- **/dashboard**: Contém a aplicação do dashboard interativo (`app.py`) construída com Streamlit.
- **/model**: Contém o script Python (`fraud_detection_rules.py`) que gera os dados e aplica o modelo de detecção baseado em regras.
- **/reports**: Contém os documentos detalhados sobre o Plano de Governança e o Plano de Educação.
- `requirements.txt`: Lista de todas as bibliotecas Python necessárias para executar o projeto.

---

## Entregáveis da Sprint 2

### 1. Protótipo de Dashboard Interativo

Foi desenvolvido um protótipo funcional de um dashboard interativo utilizando **Python** com a biblioteca **Streamlit**. A aplicação, localizada em `dashboard/app.py`, inclui:

- **KPIs Dinâmicos:** Métricas de NPS (Net Promoter Score) para cartuchos originais, genéricos e falsificados, calculados em tempo real.
- **Insights Rápidos:** Um resumo textual gerado dinamicamente que destaca a região com maior incidência de falsificações e o comparativo de NPS.
- **Volume de Chamados:** Gráfico de barras que compara o volume de chamados por tipo de cartucho em cada região do Brasil.
- **Mapa de Calor de Falsificação:** Um mapa do Brasil (Choropleth) que exibe a concentração de chamados sobre produtos falsificados por estado, destacando as áreas mais críticas.
- **Gráficos de Tendência:** Gráfico de linhas que mostra a evolução do número de chamados e devoluções ao longo do tempo.
- **Filtros Interativos:** Caixas de seleção que permitem ao usuário filtrar os dados por Estado e por tipo de cartucho.

### 2. Modelo de Detecção de Falsificação (Esboço)

Foi implementado um modelo de detecção baseado em regras, localizado em `model/fraud_detection_rules.py`. Este script gera os dados sintéticos e aplica a seguinte lógica para classificar os chamados:

- **Variáveis de Entrada (Inputs):**
  - `ID_Cliente`: Identificador único do cliente.
  - `Frequencia_Chamados_6_meses`: Número de chamados abertos nos últimos 6 meses.
  - `Tipo_Erro_Reportado`: Categoria do erro (ex: "vazamento de tinta", "falha de reconhecimento").
  - `Cartucho_Registrado`: Booleano (Sim/Não) que indica se o cartucho está no sistema oficial.

- **Lógica do Modelo (Baseado em Regras):**
  O modelo aplica um sistema de pontuação para gerar um "Score de Risco de Falsificação":
  - **Regra 1 (Frequência):** SE `Frequencia_Chamados_6_meses` > 2, adicione **30 pontos**.
  - **Regra 2 (Tipo de Erro):**
    - SE `Tipo_Erro_Reportado` = "vazamento de tinta" OU "danificou a impressora", adicione **40 pontos**.
    - SE `Tipo_Erro_Reportado` = "falha de reconhecimento", adicione **20 pontos**.
  - **Regra 3 (Registro):** SE `Cartucho_Registrado` = Não, adicione **30 pontos**.

- **Classificação Final:**
  - **Score > 70:** "Alta Probabilidade de Falsificação".
  - **Score entre 40 e 70:** "Suspeita Moderada".
  - **Score < 40:** "Baixa Probabilidade".

### 3. Plano de Governança de IA

Para garantir que o uso de IA seja ético e eficaz, a HP implementará as seguintes diretrizes:

- **Transparência:** Para cada produto ou vendedor marcado como suspeito pelo "Digital Brand Protection Squad", o sistema deve registrar a "justificativa da decisão". Por exemplo: "Este anúncio foi marcado como suspeito devido a: (1) preço 70% abaixo da média de mercado; (2) imagem da embalagem inconsistente com o padrão oficial." Esta justificativa será acessível em auditorias internas.
- **Responsabilidade:** Um Comitê de Ética em IA, formado por membros dos departamentos Jurídico, de Analytics e de Produto, será responsável por supervisionar o desempenho dos modelos trimestralmente. Eles revisarão os relatórios de acurácia, falsos positivos e os impactos das decisões automatizadas.
- **Privacidade:** Os dados dos clientes utilizados no modelo de detecção serão anonimizados sempre que possível. O acesso aos dados brutos será restrito à equipe de Business Analytics e protegido por múltiplos fatores de autenticação. Os dados nunca serão compartilhados com terceiros.
- **Mitigação de Vieses:** O modelo será treinado e testado com dados de todas as regiões do Brasil de forma balanceada. Além disso, o Comitê de Ética analisará se há uma concentração desproporcional de marcações de "alta probabilidade" em regiões de menor renda ou com menor acesso a revendedores oficiais, ajustando o modelo para evitar penalizações injustas e focar em padrões de fraude, não em perfis demográficos.

*(O documento completo pode ser encontrado em `reports/plano_governanca_ia.md`)*

### 4. Plano de Educação ao Cliente

Foi desenvolvido um plano de engajamento proativo para educar o consumidor e fortalecer a confiança na marca:

- **Campanha Digital: "HP Original: Na Dúvida, Não Use"**
  - **Peças:** Vídeos curtos (Reels/TikTok) e infográficos para redes sociais mostrando como identificar sinais de falsificação em 3 passos: Selo de Segurança, QR Code, Embalagem e Preço.
  - **Parcerias:** Colaborar com influenciadores de tecnologia para que demonstrem o processo de verificação.

- **Programa de Fidelidade "HP Original+" (Detalhado):**
  - **Cadastro:** Ao escanear o QR Code de um produto original, o cliente é convidado a entrar para o clube.
  - **Benefícios:** Acúmulo de pontos que podem ser trocados por descontos, extensões de garantia ou acesso antecipado a promoções.
  - **Gamificação:** Desafios como "Registre 3 cartuchos seguidos e ganhe um brinde".

- **App de Verificação "HP Protege":**
  - **Funcionalidade Principal:** Leitor de QR Code que se conecta ao banco de dados da HP e retorna uma confirmação instantânea de autenticidade.

*(O documento completo pode ser encontrado em `reports/plano_educacao_cliente.md`)*

### 5. Simulação de Impacto Futuro (com ou sem ação)

Diretamente no dashboard, foi incluída uma seção que simula o impacto das medidas propostas. Ela apresenta gráficos comparativos que estimam dois cenários para os próximos 12 meses:
- **"Com Ação":** Uma projeção otimista que mostra a redução potencial em devoluções e chamados de suporte após a implementação das soluções de IA e educação.
- **"Sem Ação":** Uma projeção que mostra o crescimento esperado do problema caso nenhuma medida seja tomada.

---

## Tecnologias e Conceitos Utilizados

- **Business Analytics:** Dashboards, relatórios comparativos, KPIs.
- **IA e Machine Learning:** Modelo preditivo baseado em regras.
- **Governança de IA:** Ética, transparência, privacidade e controle de viés.
- **Data Storytelling:** Visualizações de dados orientadas à tomada de decisão.
- **Bibliotecas Python:** `Pandas`, `Streamlit`, `Plotly`, `TopoJSON`.

---

## Como Executar o Projeto

Para visualizar o dashboard interativo, siga os passos abaixo:

1.  **Clone o repositório (se aplicável) e navegue até a pasta do projeto.**

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Gere os dados sintéticos:**
    Este comando cria o arquivo `data/synthetic_data.csv` que alimenta o dashboard.
    ```bash
    python model/fraud_detection_rules.py
    ```

4.  **Execute a aplicação do dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```

Após executar o último comando, um link local será exibido no seu terminal. Abra-o em seu navegador para acessar o dashboard. 