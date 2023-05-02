class Backtest:
    def __init__(self, strategy, historical_data, pair=None):
        self.strategy = strategy
        self.historical_data = historical_data
        self.pair = pair
        self.display_results = True

    def run(self):
        self.strategy.trades = []
        self.strategy.df = self.historical_data
        self.strategy.add_technical_indicators()
        self.strategy.populate_buy_sell()

        for index, row in self.strategy.df.iterrows():
            try:
                if row["open_long_limit"]:
                    self.strategy.position.check_opening_position(row.name, row)
                if row["close_long_limit"]:
                    self.strategy.position.check_closing_position(row.name, row)
            except Exception as e:
                print(f"Error: {e}")

        if self.display_results:
            for self.trade in self.strategy.position.trades:
                print(self.trade)

        return self.strategy.position.trades, self.strategy.df
