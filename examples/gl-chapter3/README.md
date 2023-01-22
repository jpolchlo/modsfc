The Simplest Model with Government Money
========================================

This is an example model following Godley & Lavoie, chapter 3.  This very simple model shows the general approach to stock/flow consistent (SFC) models: money flows in this case from government, is accumulated as private wealth, and is eliminated through taxation.  This simple economy is based on cash.

## Basic model

The total model equations are
```
Cs = Cd
Gs = Gd
Ts = Td
Ns = Nd
YD = (W * Ns) - Ts
Td = θ * W * Ns
Cd = α₁ * YD + α₂*Hh(-1)
Hs - Hs(-1) = Gd - Td
Hh - Hh(-1) = YD - Cd
Y = Cs + Gs
Nd = Y/W
```
with variables defined as

| Variable | Description                            |
|----------|----------------------------------------|
| Cd       | Consumption goods demand by households |
| Cs       | Consumption goods supply               |
| Gs       | Government goods, supply               |
| Hh       | Cash money held by households          |
| Hs       | Cash money supplied by the government  |
| Nd       | Demand for labor                       |
| Ns       | Supply of labor                        |
| Td       | Taxes, demand                          |
| Ts       | Taxes, supply                          |
| Y        | Income (GDP)                           |
| YD       | Disposable income of households        |

and parameters

| Parameter | Description (default value)             |
|-----------|-----------------------------------------|
| θ         | Taxation rate (0.2)                     |
| α₁        | Propensity to consume from income (0.6) |
| α₂        | Propensity to consume from wealth (0.4) |
| Gd        | Government demand for goods (20)        |
| W         | Wage rate (1)                           |

The `(-1)` notation indicates the lagged quantity from the previous period.

## Modular model

We break this monolithic model into parts as defined by which actor is responsible for setting or responding to the values.  See the corresponding source files for the definition.

### Government

Sets the tax rate, spends to acquire goods, receives tax payments.  The `Hs` variable above is an accounting term to track the total amount of cash released to the economy, net of tax receipts.

### Producers

The most substantive change to the model is the addition of an extra step in the protocol to communicate the wage from the producer and respond to a labor supply offer from the household sector.

### Households

Households supply as much labor as producers require and accumulate excess wealth in the form of cash.  The latter captures the `Hh` variable above.  There is also a slight deviation from the original model in that the equations above allow for income and spending to be simultaneously resolved; but when the sequencing of operations is introduced to separate responsibilities among the various actors, it's clear that consumption spending cannot occur before income arrives, and income cannot arrive before producers receive expenditures.


## References

Godley, W., & Lavoie, M. (2016). Monetary economics: an integrated approach to credit, money, income, production and wealth. Springer.
