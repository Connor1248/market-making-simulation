# Quantitative Strategy Backtester: MA Crossover & RSI State Machine

A lightweight Python backtesting framework that evaluates classic trend-following and momentum strategies against buy-and-hold benchmarks across multi-asset benchmarks (equities, ETFs, bonds, and gold) using historical daily market data from 2010 to 2026.

---

## Overview

This repository backtests two fundamental algorithmic trading strategies against a multi-asset universe:
1. **50/200 Moving Average Crossover**: A trend-following strategy that generates long signals when the 50-day Simple Moving Average (SMA) exceeds the 200-day SMA.
2. **14-Period RSI Mean-Reversion State Machine**: A long-only momentum strategy that enters positions when 14-day RSI drops below 30 (oversold) and holds until RSI crosses above 70 (overbought).

---

## Asset Universe

The strategy evaluates performance across major US asset classes:

| Ticker | Asset Class / Description |
| :--- | :--- |
| `^GSPC` | S&P 500 Index |
| `SPY` | SPDR S&P 500 ETF Trust |
| `QQQ` | Invesco QQQ Trust (Nasdaq-100) |
| `IWM` | iShares Russell 2000 ETF |
| `GLD` | SPDR Gold Shares |
| `TLT` | iShares 20+ Year Treasury Bond ETF |
| `AAPL` | Apple Inc. |
| `NVDA` | NVIDIA Corporation |

---

## Strategy Methodology & Mathematics

### Benchmark & CAGR Calculation
All strategy returns are compared against a standard Buy-and-Hold benchmark using the average yearly percentage growth.

### 1. Moving Average Crossover (`moving_avg`)
* **Signal Generation**: Long signal active ($S_t = 1$) when $\text{SMA}_{50, t} > \text{SMA}_{200, t}$, otherwise cash ($S_t = 0$).
* **Execution**: Signal is shifted by 1 day ($S_{t-1}$) to eliminate lookahead bias.

### 2. Relative Strength Index State Machine (`RSI`)
* **Indicator Calculation**:
  * $\text{RS} = \frac{\text{SMA}_{14}(\text{Gains})}{\text{SMA}_{14}(\text{Losses})}$
  * $\text{RSI}_t = 100 - \frac{100}{1 + \text{RS}}$
* **State Engine Logic**:
  * **Entry**: Buy on day $t$ if $\text{RSI}_{t-1} < 30$ and not currently in position.
  * **Exit**: Sell on day $t$ if $\text{RSI}_{t-1} > 70$ and currently in position.
  * **Holding**: Maintain active position state during intermediate steps.
