import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine, inspect, text

url_itens_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/itens_pedidos.csv'
url_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/pedidos.csv'
url_produto = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/produtos.csv'
url_vendedores = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/vendedores.csv'


dfIP= pd.read_csv(url_itens_pedidos)
dfPe=pd.read_csv(url_pedidos)
dfPr=pd.read_csv(url_produto)
dfVe=pd.read_csv(url_vendedores)

Engine = create_engine('sqlite:///:memory:')

dfIP.to_sql('Itens',Engine,index=False)
dfPe.to_sql('Pedidos',Engine,index=False)
dfPr.to_sql('Produto',Engine,index=False)
dfVe.to_sql('Vendedor',Engine,index=False)

inspector=inspect(Engine)
print(inspector.get_table_names())
