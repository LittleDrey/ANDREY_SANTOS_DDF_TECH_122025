# 📚 Dicionário de Dados - Brazilian E-Commerce (Olist)

Este documento descreve as principais tabelas da camada **Bronze/Silver** utilizadas no Data Lake.

## 1. Tabela: `orders` (Pedidos)
Tabela central que conecta todas as outras informações. Cada linha representa um pedido único.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `order_id` | String | Identificador único do pedido. |
| `customer_id` | String | Chave para a tabela de clientes. |
| `order_status` | String | Status atual (delivered, shipped, canceled, etc.). |
| `order_purchase_timestamp` | Timestamp | Data e hora da compra. |
| `order_approved_at` | Timestamp | Data e hora da aprovação do pagamento. |
| `order_delivered_carrier_date` | Timestamp | Data e hora de entrega à transportadora. |
| `order_delivered_customer_date`| Timestamp | Data real de entrega ao cliente. |
| `order_estimated_delivery_date`| Timestamp | Data estimada de entrega (prometida). |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro na camada Bronze. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 2. Tabela: `order_items` (Itens do Pedido)
Tabela transacional com os detalhes dos produtos vendidos.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `order_id` | String | FK para a tabela de pedidos. |
| `order_item_id` | Integer | Número sequencial do item no pedido. |
| `product_id` | String | FK para a tabela de produtos. |
| `seller_id` | String | FK para a tabela de vendedores. |
| `shipping_limit_date` | Timestamp | Data limite para o vendedor postar o produto. |
| `price` | Double | Preço unitário do item. |
| `freight_value` | Double | Valor do frete rateado para este item. |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro na camada Bronze. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 3. Tabela: `products` (Produtos)
Cadastro de produtos vendidos no marketplace.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `product_id` | String | Identificador único do produto. |
| `product_category_name` | String | Categoria raiz do produto. |
| `product_name_lenght` | Integer | Tamanho do nome do produto. |
| `product_description_lenght` | Integer | Tamanho da descrição do produto. |
| `product_photos_qty` | Integer | Quantidade de fotos publicadas. |
| `product_weight_g` | Integer | Peso do produto em gramas. |
| `product_length_cm` | Integer | Comprimento do produto (cm). |
| `product_height_cm` | Integer | Altura do produto (cm). |
| `product_width_cm` | Integer | Largura do produto (cm). |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 4. Tabela: `order_reviews` (Avaliações)
Contém o feedback do cliente (Dados desestruturados para IA).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `review_id` | String | ID único da avaliação. |
| `order_id` | String | FK para o pedido avaliado. |
| `review_score` | Integer | Nota de 1 a 5 dada pelo cliente. |
| `review_comment_title` | String | Título do comentário (Ex: "Recomendo"). |
| `review_comment_message` | String | Comentário em texto livre. |
| `review_creation_date` | Timestamp | Data de envio da pesquisa. |
| `review_answer_timestamp` | String | Data/Hora da resposta (String na Bronze / Timestamp na Silver). |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 5. Tabela: `customers` (Clientes)
Cadastro de clientes (Compradores).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `customer_id` | String | Chave para linkar com Orders. |
| `customer_unique_id` | String | ID único real do cliente. |
| `customer_zip_code_prefix` | Integer | 5 primeiros dígitos do CEP do cliente. |
| `customer_city` | String | Cidade do cliente. |
| `customer_state` | String | Estado (UF) do cliente. |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 6. Tabela: `sellers` (Vendedores)
Cadastro dos vendedores parceiros (Essencial para Logística e Desempenho).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `seller_id` | String | Identificador único do vendedor. |
| `seller_zip_code_prefix` | Integer | 5 primeiros dígitos do CEP do vendedor (Origem). |
| `seller_city` | String | Cidade do vendedor. |
| `seller_state` | String | Estado (UF) do vendedor. |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |

## 7. Tabela: `geolocation` (Geolocalização)
Base de CEPs x Lat/Long (Essencial para mapas e cálculo de rotas).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `geolocation_zip_code_prefix` | Integer | 5 primeiros dígitos do CEP. |
| `geolocation_lat` | Double | Latitude. |
| `geolocation_lng` | Double | Longitude. |
| `geolocation_city` | String | Cidade. |
| `geolocation_state` | String | Estado. |
| `dt_ingestao` | Timestamp | Data e hora da ingestão do registro. |
| `arquivo_origem` | String | Nome do arquivo CSV de origem. |
