class Position():
    def __init__(self):
        self.current_position = None
        self.open_positions = []
        self.trades = []
        self.leverage = 1
        self.maker_fee = 0.0001  # 0,01% en décimal
        self.taker_fee = 0.0006  # 0,06% en décimal
        self.initial_wallet = 100
        self.wallet = self.initial_wallet

    def open_position(self, index, row, reason):
        trade_size = (self.wallet * self.leverage / row["open"])   
        if trade_size > 0:
            self.wallet -= trade_size * row["open"]
            fee = trade_size * row["open"] * self.taker_fee
            self.wallet -= fee
            self.current_position = {
                "date": index,
                "reason": reason,
                "side": "LONG",
                "size": trade_size,
                "price": row["open"],
                "fee": fee,
            }
            return True
        return False

    def close_position(self, index, row, reason):
        close_price = row["open"]
        trade_result = (close_price - self.current_position["price"]) 
        self.wallet += self.current_position["size"] * trade_result

        fee = self.current_position["size"] * close_price * self.taker_fee
        self.wallet -= fee
        self.trades.append(
            {
                "open_date": self.current_position["date"],
                "close_date": index,
                "open_reason": self.current_position["reason"],
                "close_reason": reason,
                "open_price": self.current_position["price"],
                "close_price": close_price,
                "open_fee": self.current_position["fee"],
                "close_fee": fee,
                "wallet": self.wallet,
            }
        )
        self.current_position = None

    def check_opening_position(self, index, row):
        if not self.current_position:
                opened = self.open_position(index, row, "Buy signal")
                if opened:
                    self.trades.append(
                        {
                            "open_date": index,
                            "position": "LONG",
                            "open_reason": "Buy signal",
                            "open_price": row["open"],
                            "open_fee": self.current_position["fee"],
                            "open_trade_size": self.current_position["size"],
                            "wallet": self.wallet,
                        }
                    )
                    self.open_positions.append(self.current_position)
                    with open('positions.txt', 'a') as file:
                        file.write(f"{index}, {row['open']}, {self.current_position['size']}, {self.current_position['side']}\n")

    def check_closing_position(self, index, row):
        if self.current_position:
            if self.current_position["side"] == "LONG":
                    self.close_position(index, row, "Limit")
