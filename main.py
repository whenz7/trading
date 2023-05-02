from stratgeez import StratGeez
from data_utils import *
from indicators import *
from position import *
from backtest import *

# Votre code pour exécuter le programme et utiliser les autres modules
csv_file_path = "database/Bybit/15m/BTCUSDT.csv"
historical_data = load_historical_data(csv_file_path)

strategy = StratGeez(
    historical_data=historical_data,
    pair="BTCUSDT",
    exchange=None,
    timeframe="5m",
    initial_wallet=10,
    knn_n_neighbors=1)

def get_metrics(df_trades, df_days):
    if len(df_trades) == 0:
        return -np.inf, 0, 0

    df_trades_copy = df_trades.copy()
    df_trades_copy['evolution'] = df_trades_copy['wallet'].diff()
    df_trades_copy['daily_return'] = df_trades_copy['evolution'] / df_trades_copy['wallet'].shift(1)

    mean_daily_return = df_trades_copy['daily_return'].mean()
    std_dev_daily_return = df_trades_copy['daily_return'].std()

    sharpe_ratio = (mean_daily_return / std_dev_daily_return) * np.sqrt(df_days)

    return sharpe_ratio, mean_daily_return, std_dev_daily_return

trades, df = strategy.run_historical_backtest(historical_data, verbose=False, pair="BTCUSDT", display_results=True)
num_trades = len(trades)
final_wallet = strategy.wallet
gain_or_loss = final_wallet - strategy.initial_wallet
percentage_change = (final_wallet - strategy.initial_wallet) / strategy.initial_wallet * 100
print(f"Nombre de trades effectués: {num_trades}")
print(f"Pourcentage de gain ou de perte réalisé(e) : {percentage_change:.2f}%")
print(f"Gain ou perte réalisé(e): {gain_or_loss:.2f}")
print(f"Valeur du portefeuille final: {final_wallet:.2f}")