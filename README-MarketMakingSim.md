# Market Making & Inventory Risk Simulation

A Python simulation modeling how market maker profitability, inventory risk, and Sharpe ratio depend on bid-ask spread width, inventory-skewing strength ($k$), and adverse selection ($\alpha$).

---

## Motivation

In basic market-making models assuming pure noise traders, wider spreads trivially lead to higher expected profits, and inventory risk is ignored. In practice, market makers face two main risks:
1. **Inventory Risk**: Holding unhedged directional positions during market moves.
2. **Adverse Selection**: Trading against informed participants who hold private signals or superior timing.

This simulation models a discrete-time market maker using an inventory-skewing rule (similar to Avellaneda-Stoikov inventory control) under varying levels of toxic/informed order flow ($\alpha = 0.25$ vs. $\alpha = 1.0$).

---

## Model Setup

1. **Asset Price**: The fair value $V_t$ follows a standard arithmetic random walk:
   $$V_{t+1} = V_t + \epsilon_t, \quad \epsilon_t \sim \mathcal{N}(0, \sigma^2)$$

2. **Quotes**: The market maker posts symmetric spreads around fair value, adjusted for current inventory position $I_t$:
   $$\text{Bid}_t = V_t - \frac{\text{Spread}}{2} - k \cdot \sigma \cdot I_t$$
   $$\text{Ask}_t = V_t + \frac{\text{Spread}}{2} - k \cdot \sigma \cdot I_t$$
   Where $k$ parameterizes inventory aversion.

3. **Order Flow & Adverse Selection**:
   * **Informed Traders** (probability $\alpha$): Receive a noisy signal of the next step's price move: $S_t \sim \mathcal{N}(\Delta V_{t+1}, \sigma_{\text{noise}}^2)$. They only cross the spread if expected profit is positive ($S_t > \text{Ask}_t - V_t$ for buys, $S_t < \text{Bid}_t - V_t$ for sells).
   * **Noise Traders** (probability $1 - \alpha$): Execute buy/sell orders with equal 50/50 probability.

4. **Simulation Protocol**: Runs 100 Monte Carlo iterations of 1,000 steps per parameter configuration across spreads $\{0, 1, \dots, 7\}$ and inventory penalty weights $k \in [0, 5]$.

---

## Key Results & Analysis

### 1. Low Adverse Selection ($\alpha = 0.25$)

With order flow mostly comprising noise traders:
* **Variance Control**: Setting even a small inventory penalty ($k \approx 0.25$) drastically reduces portfolio variance compared to unhedged market making ($k = 0$).
* **Sharpe Optimization**: Because spread capture is mostly profitable, Sharpe ratio exhibits a clear maximum around $k \in [1.0, 2.0]$. Beyond this point, aggressive quote skewing reduces trade execution frequency and lowers net PnL.

| Figure | Description |
| :--- | :--- |
| <img width="766" height="547" alt="Screenshot 2026-08-09 140422" src="https://github.com/user-attachments/assets/df9000e7-8546-41e6-be13-c33d5b2b6a67" /> | **Average Total Wealth vs $k$**: Wealth peaks at small $k$ values before decaying from excessive quoting drag. |
| <img width="762" height="561" alt="Screenshot 2026-08-09 140412" src="https://github.com/user-attachments/assets/e12d8292-7950-43f6-9ec4-07b148f4704b" /> | **Wealth Variance vs $k$**: Variance drops exponentially as soon as inventory penalty $k > 0$ is introduced. |
| <img width="768" height="561" alt="Screenshot 2026-08-09 140215" src="https://github.com/user-attachments/assets/786302c6-8082-4a80-a520-85d72a9acde7" /> | **Sharpe Ratio vs $k$**: Parabolic trade-off between inventory risk reduction and profit drag. |

---

### 2. High Adverse Selection ($\alpha = 1.0$)

When all incoming trades originate from informed traders:
* **Minimum Viable Spread**: Tighter spreads ($\text{Spread} < 4.0$) yield strictly negative expected wealth because trades are systematically adverse.
* **Inventory Drag Acceleration**: Increasing $k$ shifts quotes into informed flow, causing linear decay in average PnL per trade as the market maker gets picked off more frequently on inventory reduction quotes.

| Figure | Description |
| :--- | :--- |
| <img width="750" height="552" alt="Screenshot 2026-08-09 141458" src="https://github.com/user-attachments/assets/aa02ca71-a830-4072-a1ea-bafd68917582" /> | **Average Total Wealth vs $k$**: Requires wider spreads ($\ge 4.0$) to maintain positive expectancy against toxic flow. |
| <img width="761" height="561" alt="Screenshot 2026-08-09 141426" src="https://github.com/user-attachments/assets/ae9bd84f-18fa-4afb-8671-8bf63ca02c64" /> | **PnL per Trade vs $k$**: Monotonic decrease in trade profitability as $k$ increases under purely toxic flow. |
| <img width="758" height="560" alt="Screenshot 2026-08-09 141404" src="https://github.com/user-attachments/assets/4db33c69-9d4a-4783-8414-6fd20725e325" /> | **Sharpe Ratio vs $k$**: Heavily suppressed Sharpe ratios due to persistent adverse selection. |

---

## Conclusions

1. **Inventory Management**: Unhedged market making ($k=0$) leads to unbounded position variance over longer horizons. Introducing inventory skewing $k > 0$ effectively stabilizes mark-to-market variance.
2. **Impact of Toxic Flow**: Market makers cannot rely solely on inventory management; quote width must be calibrated dynamically to account for the proportion of informed traders ($\alpha$).
