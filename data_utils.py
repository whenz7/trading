import pandas as pd
import ccxt
import numpy as np

def get_historical_from_db(exchange, symbol, timeframe, path="/database/"):
    symbol = symbol.replace('/','-')
    df = pd.read_csv(filepath_or_buffer=path+str(exchange.name)+"/"+timeframe+"/"+symbol+".csv")
    df = df.set_index(df['date'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['date']
    return df

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

def get_historical_from_path(path):
    df = pd.read_csv(filepath_or_buffer=path)
    df = df.set_index(df['date'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['date']
    return df

def load_historical_data(csv_file_path):
    data = pd.read_csv(csv_file_path)
    data['date'] = pd.to_datetime(data['date'], unit='ms')
    data.set_index('date', inplace=True)
    return data

def get_realtime_data(exchange, pair, timeframe, historical_data):
    # Vérifier si les données historiques sont vides
    if isinstance(historical_data, pd.DataFrame) and not historical_data.empty:
        # Récupérer la dernière bougie historique
        last_historical_candle = historical_data.iloc[-1]
        print(f"Données historiques OK {pair} . {last_historical_candle}")
        # Récupérer les données réelles pour la paire de devises
        current_candles = exchange.fetch_ohlcv(pair, timeframe)

        if current_candles:
            # Identifier les bougies manquantes
            if last_historical_candle.name == current_candles[0][0]:
                # Si la dernière bougie historique correspond à la première bougie réelle,
                # il n'y a pas de bougies manquantes
                missing_candles = []
            else:
                # Sinon, récupérer les bougies manquantes à partir de la dernière bougie historique
                last_close = last_historical_candle["close"]
                last_historical_timestamp = last_historical_candle.name.timestamp() * 1000
                missing_candles = []
                for candle in current_candles:
                    if candle[0] <= last_historical_timestamp:
                        # Ignorer les bougies déjà présentes dans les données historiques
                        continue
                    if candle[0] > last_historical_timestamp + int(timeframe[:-1]) * 60 * 1000:
                        # Si des bougies sont manquantes, récupérer les bougies manquantes à partir de la dernière bougie historique

                        missing_data = exchange.fetch_ohlcv(pair, timeframe, since=int(last_historical_timestamp))

                        missing_candles.extend(missing_data[:-1])
                    # Ajouter la bougie réelle
                    missing_candles.append(candle[0:6])

            # Ajouter les bougies manquantes aux données historiques
            missing_data = pd.DataFrame(missing_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
            missing_data["timestamp"] = pd.to_datetime(missing_data["timestamp"], unit="ms")
            missing_data.set_index("timestamp", inplace=True)
            historical_data = pd.concat([historical_data, missing_data], ignore_index=False)
            print(f"Nouvelle donnée en temps réel pour {pair} : {missing_data.index[-1]}")
            print(f"Dernière donnée historique pour {pair} : {last_historical_candle.name}")
            print(f"Nombre de données récupérées pour {pair}: {historical_data.shape[0]}")
        else:
            print(f"Pas de nouvelle donnée pour {pair}")
    else:
        print(f"Télécharger toutes les bougies {pair}")
        # Télécharger toutes les bougies
        historical_data = exchange.fetch_ohlcv(pair, timeframe)
        historical_data = pd.DataFrame(historical_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        historical_data["timestamp"] = pd.to_datetime(historical_data["timestamp"], unit="ms")
        historical_data.set_index("timestamp", inplace=True)

    return historical_data

def get_missing_data(exchange, pair, timeframe, last_historical_date, max_candles=500):
    # Récupérer la dernière bougie historique
    last_historical_timestamp = int(last_historical_date.timestamp() * 1000)

    # Récupérer les bougies manquantes à partir de la dernière bougie historique
    missing_candles = []
    while len(missing_candles) < max_candles:
        since_timestamp = last_historical_timestamp + (len(missing_candles) * timeframe)
        missing_candles.extend(exchange.fetch_ohlcv(pair, timeframe, since=since_timestamp))

    # Créer un DataFrame avec les bougies manquantes
    missing_data = pd.DataFrame(missing_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    missing_data["timestamp"] = pd.to_datetime(missing_data["timestamp"], unit='ms')
    missing_data.set_index("timestamp", inplace=True)

    return missing_data
