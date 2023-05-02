README - StratGeez
Description
Ce projet contient un modèle de stratégie de trading basé sur des indicateurs techniques, dont le but est d'analyser les signaux de marché et de prendre des positions d'achat et de vente en conséquence.

Fichiers
Le projet est composé de trois fichiers principaux :

stratgeez.py : Contient la classe StratGeez qui implémente la stratégie de trading.
position.py : Contient la classe Position qui gère les positions, les trades et le portefeuille.
indicator.py : Contient la classe Indicator qui calcule les indicateurs techniques utilisés dans la stratégie.

1. stratgeez.py
La classe StratGeez implémente la stratégie de trading. Ses principales méthodes sont :

__init__(self, pair, exchange, timeframe): Initialise la stratégie avec les paramètres donnés.
add_technical_indicators(self, show_log=True): Ajoute les indicateurs techniques au DataFrame.
populate_buy_sell(self, show_log=False): Détermine les signaux d'achat et de vente en fonction des indicateurs techniques.

2. position.py
La classe Position gère les positions, les trades et le portefeuille. Ses principales méthodes sont :

__init__(self): Initialise les attributs de la classe.
open_position(self, index, row, reason): Ouvre une position et met à jour le portefeuille.
close_position(self, index, row, reason): Ferme une position et met à jour le portefeuille.
check_opening_position(self, index, row): Vérifie si les conditions pour ouvrir une position sont remplies.
check_closing_position(self, index, row): Vérifie si les conditions pour fermer une position sont remplies.

3. indicator.py
La classe Indicator calcule les indicateurs techniques utilisés dans la stratégie. Ses principales méthodes sont :

calculate_knn(self, df, n_neighbors=5, features=['close', 'volume']): Calcule le signal KNN.
calculate_obv(self, df): Calcule l'indicateur de volume On Balance Volume (OBV).
calculate_rsi(self, df): Calcule l'indicateur de force relative (RSI).
calculate_super_trend(self, df, high, low, close, atr_window, atr_multiplier): Calcule l'indicateur Super Trend.
calculate_ema(self, df, short_ema_window, long_ema_window): Calcule les moyennes mobiles exponentielles (EMA) à court et long termes.
calculate_macd_crossover(self, df): Calcule les croisements de la ligne MACD et de la ligne de signal.