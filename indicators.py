import pandas as pd
import numpy as np
import ta
import ta.volume as volume
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from custom_indicators import SuperTrend


class Indicator:
    def __init__(self):
        pass
    
    def calculate_knn(self, df, n_neighbors=5, features=['close', 'volume']):
        scaler = StandardScaler()

        # Remplacer les valeurs non numériques par NaN
        df_numeric = df[features].apply(pd.to_numeric, errors='coerce')

        # Imputer les valeurs manquantes avec la moyenne de chaque colonne
        imputer = SimpleImputer(strategy='mean')
        df_numeric = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)
        X = df_numeric.values
        X_scaled = scaler.fit_transform(X)

        # Calculer le pourcentage de variation de 'close', supprimer les NaN et les remplacer par la moyenne
        y = np.sign(df['close'].pct_change().values)
        y = np.where(np.isnan(y), np.nanmean(y), y)

        # Supprimer la première valeur NaN dans y pour correspondre à la taille de X_scaled
        y = y[1:]
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        knn.fit(X_scaled[:-1], y)

        df['knn_signal'] = knn.predict(X_scaled)
        return df

    def calculate_obv(self, df):
        df['obv'] = volume.on_balance_volume(df['close'], df['volume'])
        return df

    def calculate_rsi(self, df):
        df['rsi'] = ta.momentum.rsi(close=df['close'], window=14)
        return df

    def calculate_super_trend(self, df, high, low, close, atr_window, atr_multiplier):
        super_trend = SuperTrend(high, low, close, atr_window, atr_multiplier)
        df['super_trend_direction'] = super_trend.super_trend_direction()
        return df

    def calculate_ema(self, df, short_ema_window, long_ema_window):
        df['ema_short'] = ta.trend.ema_indicator(close=df['close'], window=short_ema_window)
        df['ema_long'] = ta.trend.ema_indicator(close=df['close'], window=long_ema_window)
        return df

    def calculate_macd_crossover(self, df):
        macd_indicator = ta.trend.MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()
        df['macd_cross'] = 'none'
        previous_macd = df['macd'].shift(1)
        previous_macd_signal = df['macd_signal'].shift(1)
        for i in range(1, len(df)):
            if previous_macd[i] < previous_macd_signal[i] and df['macd'][i] > df['macd_signal'][i]:
                df.loc[df.index[i], 'macd_cross'] = 'bullish'
            elif previous_macd[i] > previous_macd_signal[i] and df['macd'][i] < df['macd_signal'][i]:
                df.loc[df.index[i], 'macd_cross'] = 'bearish'
            else:
                df.loc[df.index[i], 'macd_cross'] = 'none'
        return df