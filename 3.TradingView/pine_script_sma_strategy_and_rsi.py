//@version=5
start = timestamp(2016,1,1,0,0)
end = timestamp(2020,1,1,0,0)
strategy("Estrategia de cruce de medias móviles", overlay=true)
// ema = ta.ema(close, length)
// Definir medias móviles
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)

// Calcular el RSI
//rsi = ta.rsi(close, 14)

// Condiciones de entrada
longCondition = ta.crossover(ema50, ema200) 
shortCondition = ta.crossunder(ema50, ema200) 
// Comprar o vender según las condiciones de entrada
if (longCondition)
    strategy.entry("Compra", strategy.long)
if (shortCondition)
    strategy.entry("Venta", strategy.short)

// Establecer los niveles de stop loss y take profit
//stopLoss = ema50 * 0.98
//takeProfit = ema50 * 1.02

//strategy.exit("SL/TP", "Compra", stop=stopLoss, limit=takeProfit)
//strategy.exit("SL/TP", "Venta", stop=stopLoss, limit=takeProfit)

// Graficar las medias móviles y el RSI
plot(ema50, color=color.blue, title="EMA 50")
plot(ema200, color=color.red, title="EMA 200")
//plot(rsi, color=color.orange, title="RSI")
