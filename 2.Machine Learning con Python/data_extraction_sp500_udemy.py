import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Descargar datos históricos del S&P 500
import pandas as pd
import yfinance as yf

# Obtener la lista de símbolos del S&P 500
try:
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
except Exception as e:
    print(f"Error al obtener los símbolos: {e}")
    exit(1)

# Descargar datos desde Yahoo Finance
try:
    data = yf.download(list(tickers), start='2023-01-01', end='2023-12-31')['Adj Close']
except Exception as e:
    print(f"Error al descargar datos: {e}")
    exit(1)

# Guardar los datos en un archivo Excel en la carpeta actual
try:
    #data.to_excel('C:/Users/kevin/OneDrive/Desktop/youtube_scripts/datos_sp500.xlsx', index=False)
    #C:/Users/kevin/OneDrive/Desktop/youtube_scripts
    data.to_excel('C:/Users/kevin/OneDrive/Desktop/youtube_scripts/datos_sp500_2.xlsx', index=True)
    print("Datos guardados exitosamente en datos_sp500_1.xlsx")
except Exception as e:
    print(f"Error al guardar los datos en Excel: {e}")


'''
# Ruta del archivo Excel
archivo_excel = 'C:/Users/kevin/OneDrive/Desktop/youtube_scripts/datos_sp500_1.xlsx'

# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(archivo_excel)

# Verificar el contenido del DataFrame
print(df)
# Convertir la columna 'Date' en el índice datetime
df.set_index('Date', inplace=True)
returns = df.pct_change()
#returns.dropna(inplace=True)
returns.fillna(0, inplace=True)
print(returns)

'''
'''
# Estandarizar los retornos
scaler = StandardScaler()
returns_scaled = scaler.fit_transform(returns)

# Aplicar algoritmo de K-Means para clasificar empresas
num_clusters = 5  # Puedes ajustar el número de clústeres
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(returns_scaled)

# Agregar los resultados al DataFrame original
results = pd.DataFrame({'Ticker': tickers, 'Cluster': kmeans.labels_})

# Imprimir la clasificación
print(results)

# Visualizar los clústeres
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(returns_scaled)

plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_, cmap='viridis')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.title('Clasificación de Empresas del S&P 500')
plt.show()
'''