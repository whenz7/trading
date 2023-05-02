from stratgeez import StratGeez
from data_utils import load_historical_data
from backtest import Backtest

csv_file_path = "database/Bybit/1m/BTCUSDT.csv"
historical_data = load_historical_data(csv_file_path)


strategy = StratGeez(
    pair="BTCUSDT",
    exchange=None,
    timeframe=None,
    )

backtest = Backtest(strategy, historical_data, pair="BTCUSDT")
trades, df = backtest.run()
final_wallet = strategy.position.wallet

num_trades = len(trades)
gain_or_loss = final_wallet - strategy.position.initial_wallet
percentage_change = (final_wallet - strategy.position.initial_wallet) / strategy.position.initial_wallet * 100

print(f"Nombre de trades effectués: {num_trades}")
print(f"Pourcentage de gain ou de perte réalisé(e) : {percentage_change:.2f}%")
print(f"Gain ou perte réalisé(e): {gain_or_loss:.2f}")
print(f"Valeur du portefeuille final: {final_wallet:.2f}")

