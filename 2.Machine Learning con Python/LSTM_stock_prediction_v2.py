import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import requests

# Configuración de la API de Polygon
API_KEY = 'your_api_key'
SYMBOL = 'AAPL'

# Función para obtener datos de la API de Polygon
def get_polygon_data(symbol, api_key):
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2020-01-01/2024-01-01?apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data['results'])

# Preprocesamiento de Datos
data = get_polygon_data(SYMBOL, API_KEY)
data['date'] = pd.to_datetime(data['t'], unit='ms')
data.set_index('date', inplace=True)
prices = data[['c']]  # Solo usamos el precio de cierre

# Escalado de datos
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(prices)

# Crear conjuntos de datos de entrenamiento y prueba
train_size = int(len(scaled_data) * 0.8)
test_size = len(scaled_data) - train_size
train_data, test_data = scaled_data[0:train_size,:], scaled_data[train_size:len(scaled_data),:]
time_step=60
# Función para crear dataset para LSTM
def create_dataset(dataset, time_step=60):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

# Crear los conjuntos de datos con el time_step fijo
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# Reshape de los datos para el modelo LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Construcción del Modelo LSTM
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenamiento del Modelo
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64, verbose=1)

# Predicciones
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inversión de la transformación para obtener los valores reales
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Preparar los datos para la visualización
train_plot = np.empty_like(scaled_data)
train_plot[:, :] = np.nan
train_plot[time_step:len(train_predict) + time_step, :] = train_predict

test_plot = np.empty_like(scaled_data)
test_plot[:, :] = np.nan
test_plot[len(train_predict) + (time_step*2) + 1:len(scaled_data) - 1, :] = test_predict

# Graficar los datos
plt.figure(figsize=(12, 6))
plt.plot(scaler.inverse_transform(scaled_data), label='Original Data')
plt.plot(train_plot, label='Training Predictions')
plt.plot(test_plot, label='Test Predictions')
plt.title('Stock Price Prediction using LSTM')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
