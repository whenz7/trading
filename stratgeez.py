from indicators import Indicator
from position import Position

class StratGeez():
    def __init__(
        self,
        pair,
        exchange,
        timeframe,
    ):
        self.indicator = Indicator()
        self.position = Position()
        self.pair = pair
        self.exchange = exchange
        self.timeframe = timeframe
        
        self.st_short_atr_window = 7
        self.st_short_atr_multiplier = 3
        self.short_ema_window = 20
        self.long_ema_window = 50
    
    def add_technical_indicators(self):
        print("- add_technical_indicators -")
        df = self.df
        df.drop(columns=df.columns.difference(['open','high','low','close','volume']), inplace=True)
        df = self.indicator.calculate_obv(df)
        df = self.indicator.calculate_rsi(df)
        df = self.indicator.calculate_super_trend(df, df['high'], df['low'], df['close'], self.st_short_atr_window, self.st_short_atr_multiplier)
        df = self.indicator.calculate_ema(df, self.short_ema_window, self.long_ema_window)
        #df = self.indicator.calculate_knn(df, self.knn_n_neighbors) 
        df = self.indicator.calculate_macd_crossover(df)
        #df = get_n_columns(df, ["super_trend_direction", "ema_short", "ema_long", "rsi", "obv", "macd" ], 1)
        self.df = df # mise à jour du DataFrame ici
        return self.df

    def populate_buy_sell(self): 
        print("- populate_buy_sell -")
        df = self.df
        df["open_long_limit"] = False
        df["close_long_limit"] = False

        df.loc[
            (df['super_trend_direction'] == True) & (df['macd_cross'] == 'bullish'),
            "open_long_limit"
        ] = True

        df.loc[
            (df['super_trend_direction'] == False) & (df['macd_cross'] == 'bearish'),
            "close_long_limit"
        ] = True
        

        self.df = df
        return df
