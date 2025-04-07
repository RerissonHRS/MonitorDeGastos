import pandas as pd
from funcoes import Transacao

# Caminho do CSV antigo
CAMINHO_CSV = r"C:\Users\av1.VIRGINIA\Documents\ARQUIVO_DADOS\ARQUIVO_DADOS.csv"

# Carrega os dados do CSV
df = pd.read_csv(CAMINHO_CSV)

# Itera sobre o DataFrame e insere no banco
for _, linha in df.iterrows():
    transacao = Transacao(
        tipo=linha["Tipo"],
        categoria=linha["Categoria"],
        descricao=linha["Descrição"],
        valor=linha["Valor"],
        data=linha["Data"]  # usa a data original do CSV
    )
    transacao.salvar()

print("Importação finalizada com sucesso!")
