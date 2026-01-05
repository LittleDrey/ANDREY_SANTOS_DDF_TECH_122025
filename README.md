## 4. Análise de Qualidade de Dados (Insights)

Utilizando a biblioteca **Sweetviz**, foram gerados relatórios de perfilamento (profiling) sobre a camada Bronze. Abaixo, destacam-se 3 achados principais que guiarão o tratamento na camada Silver:

### 🚨 Insight 1: Inconsistência de Grafia em Cidades
**Tabela:** `customers`
**Diagnóstico:** Identificada duplicidade de registros para a mesma cidade devido a variações de acentuação e grafia.
- **Evidência:** O relatório aponta alta cardinalidade na coluna `customer_city`, com variações como `sao paulo` e `são paulo` para a mesma localidade.
- **Ação na Silver:** Aplicação de funções de normalização (Lower, Trim e remoção de acentos) para garantir a integridade dos agrupamentos geográficos.

### 🚨 Insight 2: Baixa Completude em Dados Desestruturados
**Tabela:** `order_reviews`
**Diagnóstico:** As colunas de texto livre (`review_comment_message` e `review_comment_title`) apresentam alta taxa de valores nulos (Missing).
- **Evidência:** O perfilamento indica que mais de 58% dos registros nessas colunas estão vazios ou nulos (barras vermelhas no relatório).
- **Ação na Silver:** Tratamento de nulos com preenchimento padrão ("Não Informado") para evitar erros em modelos de NLP, além da sanitização de caracteres especiais (quebras de linha).

### 🚨 Insight 3: Registros Logísticos Incompletos (Nulls)
**Tabela:** `orders`
**Diagnóstico:** Campos cruciais para cálculo de frete e SLA, como `order_delivered_customer_date`, possuem valores nulos.
- **Evidência:** O relatório aponta *Missing Values* nas datas de entrega, correspondentes a pedidos com status `invoiced`, `processing` ou `canceled`.
- **Ação na Silver/Gold:** Filtragem de status ou tratamento condicional ao calcular métricas de "Tempo de Entrega" (Lead Time), garantindo que apenas pedidos finalizados componham o indicador de performance.

### 📊 Evidências de Qualidade (Relatórios HTML)
Os relatórios detalhados gerados pelo Sweetviz estão disponíveis na pasta `docs`. Você pode baixá-los para visualizar a análise completa:

* [Relatório de Clientes (Customers)](./docs/report_customers.html)
* [Relatório de Pedidos (Orders)](./docs/report_orders.html)
* [Relatório de Avaliações (Reviews)](./docs/report_order_reviews.html)
* [Acessar pasta completa](./docs)

* Nota: Como o GitHub não renderiza arquivos HTML nativamente, é necessário clicar no arquivo desejado e selecionar a opção "Download raw file" (ou ícone de download) para visualizar o dashboard interativo no seu navegador.
