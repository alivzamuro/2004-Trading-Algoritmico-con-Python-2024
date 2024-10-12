//@version=5
strategy("Estrategia con Bandas de Bollinger", overlay=true)

// Definir la fuente de datos
src = input(close, title="Fuente de datos")

// Definir los parámetros de las Bandas de Bollinger
len = input.int(200, "Longitud", minval=1, maxval=300)

mult = input.int(1.5,"Multiplicador", minval=1, maxval=5)

// Calcular las Bandas de Bollinger
sma = ta.sma(close, len)
basis = ta.sma(src, len)
dev = mult * ta.stdev(src, len)
upper = basis + dev
lower = basis - dev

// Calcular el valor RSI
//rsi_length = input.int(14, "Longitud RSI",minval=1)
//rsi_src = ta.rsi(src, rsi_length)

// Definir las señales de compra y venta
//long = ta.crossover(rsi_src, 30) and src < lower
//short = ta.crossunder(rsi_src, 70) and src > upper

long = src < lower
short = src > upper


// Definir la estrategia
if (long)
    strategy.entry("Long", strategy.long)
if (short)
    strategy.entry("Short", strategy.short)

// Definir las órdenes de salida
if (strategy.position_size > 0)
    strategy.close("Long")
if (strategy.position_size < 0)
    strategy.close("Short")

// Dibujar las Bandas de Bollinger y el valor RSI
plot(upper, color=color.blue, title="Upper")
plot(lower, color=color.blue, title="Lower")
plot(basis, color=color.white, title="Basis")
hline(30, color=color.red, linestyle=hline.style_dotted, title="Oversold")
hline(70, color=color.red, linestyle=hline.style_dotted, title="Overbought")
