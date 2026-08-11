import numpy as np
import matplotlib.pyplot as plt
import random



def simulate_true_values(steps, sigma, start): #unused function that live generates a random walk graph
    plt.ion()
    
    true_values = [start]
    historical_data = [start]

    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.set_xlabel('Step')
    ax1.set_ylabel('True Value')
    ax1.set_title('Live Random Walk')
    ax1.grid(True)

    line, = ax1.plot([0], true_values)

    ax2.set_xlabel('Step')
    ax2.set_ylabel('True Value')
    ax2.set_title('Historical Data')
    ax2.grid(True)

    history_line, = ax2.plot([0], historical_data)

    counter = 0

    for i in range(steps):

        new_value = true_values[-1] + np.random.normal(0, sigma)

        true_values.append(new_value)
        historical_data.append(new_value)

        if len(true_values) > 100:
            true_values.pop(0)
            counter += 1

        line.set_xdata(range(counter, counter + len(true_values)))
        line.set_ydata(true_values)

        ax1.relim()
        ax1.autoscale_view()
        
        history_line.set_xdata(range(len(historical_data)))
        history_line.set_ydata(historical_data)

        ax2.relim()
        ax2.autoscale_view()

        plt.pause(0.1)

    plt.ioff()
    plt.show()

    return true_values, historical_data

def simulate_next(sigma, true_values):
    true_values.append(true_values[-1] + np.random.normal(0, sigma))
    
    return true_values[-2], true_values[-1], true_values

def get_quote(spread, value, inventory, sigma, k):
    bid = value - spread/2 - k*sigma*inventory
    ask = value + spread/2 - k*sigma*inventory

    return bid, ask

def simulate_traders(show_prob, alpha, noise, bid, ask, true_values):
    if random.uniform(0, 1) <= show_prob:
        if random.uniform(0, 1) <= alpha:
            interval = true_values[-1] - true_values[-2]
            aware = np.random.normal(interval, noise)
            if aware > ask - true_values[-2]:
                return 'buy'
            elif aware < bid - true_values[-2]:
                return 'sell'
            else:
                return None
        else:
            return random.choice(['buy', 'sell'])
    else:
        return None


def run_simulation(start, length, show_prob, spread, sigma, alpha, noise, k):
    PnL = 0
    true_values = [start]

    n_trades = 0
    inventory = 0
    
    for i in range(length):
               
        last_value, true_value, true_values = simulate_next(sigma, true_values)
        bid, ask = get_quote(spread, last_value, inventory, sigma, k)
        trade = simulate_traders(show_prob, alpha, noise, bid, ask, true_values)
        
        if trade == 'buy':
            profit = ask - true_value
            n_trades += 1
            inventory -= 1
        elif trade == 'sell':
            profit = true_value - bid
            n_trades += 1
            inventory += 1
        else:
            profit = 0
            
        PnL += profit

    total_wealth = PnL + inventory*true_values[-1]
    
    return PnL, n_trades, total_wealth


fig1, k_mean_wealth = plt.subplots()
fig2, k_wealth_variance = plt.subplots()
fig3, mean_wealth_variance_wealth = plt.subplots()
fig4, PnL_per_n_trades_graph = plt.subplots()
fig5, sharpes_k_values = plt.subplots()

for spread in np.arange(0, 8, 1):
    wealth_means = []
    ks = []
    wealth_variances = []
    PnL_per_n_trades_means = []
    sharpes = []
    
    for k in np.arange(0, 5.25, 0.25):
        total_wealths = []
        PnL_per_n_trades = []
        
        for i in range(100):
            PnL, n_trades, total_wealth = run_simulation(100, 1000, 0.7, spread, 1, 0.5, 0.8, k)
            total_wealths.append(total_wealth)
            if n_trades != 0:
                PnL_per_n_trades.append(PnL/n_trades)

        
        mean_wealth = np.mean(total_wealths)
        variance_wealth = np.var(total_wealths)
        sharpe = mean_wealth/np.sqrt(variance_wealth)
        mean_PnL_per_n_trades = np.mean(PnL_per_n_trades)
        
        wealth_means.append(mean_wealth)
        wealth_variances.append(variance_wealth)
        ks.append(k)
        PnL_per_n_trades_means.append(mean_PnL_per_n_trades)
        sharpes.append(sharpe)
        
        print(f'for spread = {spread} and K value = {k} mean: {mean_wealth}, variance: {variance_wealth}')

    k_mean_wealth.plot(ks, wealth_means, label=f'spread = {spread:.2f}')
    k_wealth_variance.plot(ks, wealth_variances, label=f'spread = {spread:.2f}')
    mean_wealth_variance_wealth.plot(wealth_variances, wealth_means, label=f'spread = {spread:.2f}')
    PnL_per_n_trades_graph.plot(ks, PnL_per_n_trades_means, label=f'spread = {spread:.2f}')
    sharpes_k_values.plot(ks, sharpes, label=f'spread = {spread:.2f}')
    
k_mean_wealth.set_xlabel('K values')
k_mean_wealth.set_ylabel('Average Total Wealth')
k_mean_wealth.set_title('Average Total Wealth vs K values')
k_mean_wealth.grid(True)
k_mean_wealth.legend()

k_wealth_variance.set_xlabel('K values')
k_wealth_variance.set_ylabel('Total Wealth variance')
k_wealth_variance.set_title('Total Wealth variance vs K values')
k_wealth_variance.grid(True)
k_wealth_variance.legend()

mean_wealth_variance_wealth.set_xlabel('Wealth Variance')
mean_wealth_variance_wealth.set_ylabel('Average Total Wealth')
mean_wealth_variance_wealth.set_title('Average Total Wealth vs Wealth Variance')
mean_wealth_variance_wealth.grid(True)
mean_wealth_variance_wealth.legend()

PnL_per_n_trades_graph.set_xlabel('K values')
PnL_per_n_trades_graph.set_ylabel('Average PnL per trade')
PnL_per_n_trades_graph.set_title('Average PnL per trade vs K Values')
PnL_per_n_trades_graph.grid(True)
PnL_per_n_trades_graph.legend()

sharpes_k_values.set_xlabel('K values')
sharpes_k_values.set_ylabel('Sharpe Ratio')
sharpes_k_values.set_title('Sharpe Ratio vs K Values')
sharpes_k_values.grid(True)
sharpes_k_values.legend()
             
plt.show()
