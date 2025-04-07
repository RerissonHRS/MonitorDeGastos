import sqlite3
from datetime import datetime
import pandas as pd

# Caminho do banco (você pode alterar)
CAMINHO_BANCO = "banco_dados.db"

# Criação da tabela se não existir
def inicializar_banco():
    with sqlite3.connect(CAMINHO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                tipo TEXT,
                categoria TEXT,
                descricao TEXT,
                valor REAL
            )
        """)
        conn.commit()

# Classe orientada a objetos
class Transacao:
    def __init__(self, tipo, categoria, descricao, valor, data=None):
        self.tipo = tipo
        self.categoria = categoria
        self.descricao = descricao
        self.valor = float(valor)
        self.data = data or datetime.now().strftime("%Y-%m-%d %H:%M")

    def salvar(self):
        with sqlite3.connect(CAMINHO_BANCO) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transacoes (data, tipo, categoria, descricao, valor)
                VALUES (?, ?, ?, ?, ?)
            """, (self.data, self.tipo, self.categoria, self.descricao, self.valor))
            conn.commit()

# Carregar os dados como DataFrame
def carregar_dados():
    with sqlite3.connect(CAMINHO_BANCO) as conn:
        df = pd.read_sql_query("SELECT * FROM transacoes", conn)
    return df

# Inicializa o banco ao importar
inicializar_banco()

# Teste opcional
if __name__ == "__main__":
    exemplo = Transacao("Despesa", "Lazer", "Cinema", 45.00)
    exemplo.salvar()
    print(carregar_dados().tail())
