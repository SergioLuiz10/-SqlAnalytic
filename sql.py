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

print(dfIP.head(),dfPe.head(),dfPr.head(),dfVe.head())