
README - StratGeez
Description
StratGeez est un projet de stratégie de trading algorithmique basé sur des indicateurs techniques. Le but est d'analyser les signaux de marché et de prendre des positions d'achat et de vente en conséquence. Le projet est composé de trois fichiers principaux qui définissent la logique de la stratégie de trading, les positions et le calcul des indicateurs techniques.

Fichiers et classes

1. stratgeez.py

La classe StratGeez implémente la stratégie de trading. Ses principales méthodes et attributs sont :

__init__(self, pair, exchange, timeframe): Initialise la stratégie avec les paramètres donnés (paire de devises, échange et période).
pair: Paire de devises à trader (par exemple, "BTC/USD").
exchange: Plateforme d'échange (par exemple, "bitstamp").
timeframe: Intervalle de temps pour les bougies (par exemple, "1h").


Attributs liés aux indicateurs :
st_short_atr_window: Fenêtre de l'ATR pour le calcul de Super Trend (par défaut : 7).
st_short_atr_multiplier: Multiplicateur de l'ATR pour le calcul de Super Trend (par défaut : 3).
short_ema_window: Fenêtre de la moyenne mobile exponentielle courte (par défaut : 20).
long_ema_window: Fenêtre de la moyenne mobile exponentielle longue (par défaut : 50).

add_technical_indicators(self, show_log=True): Ajoute les indicateurs techniques au DataFrame et renvoie le DataFrame modifié.
populate_buy_sell(self, show_log=False): Détermine les signaux d'achat et de vente en fonction des indicateurs techniques et renvoie le DataFrame modifié.

2. position.py : 
Ce fichier contient la classe Position, qui gère les positions de trading ouvertes et fermées, ainsi que les informations sur les frais et la valeur du portefeuille. La classe Position est utilisée par la classe StratGeez pour interagir avec les positions de trading en fonction des signaux générés par les indicateurs techniques.

Les principales méthodes de la classe Position sont :

__init__: Initialise la position avec des valeurs par défaut pour le portefeuille, les frais et les positions ouvertes.
open_position: Ouvre une nouvelle position de trading en fonction des signaux d'achat et met à jour le portefeuille.
close_position: Ferme une position de trading ouverte en fonction des signaux de vente et met à jour le portefeuille.
check_opening_position: Vérifie s'il est possible d'ouvrir une nouvelle position en fonction des signaux d'achat.
check_closing_position: Vérifie s'il est possible de fermer une position ouverte en fonction des signaux de vente.

indicator.py : 
Ce fichier contient la classe Indicator, qui est responsable du calcul des indicateurs techniques utilisés dans la stratégie de trading. Les indicateurs sont calculés en utilisant la bibliothèque ta (Technical Analysis) et d'autres fonctions personnalisées.

Les principales méthodes de la classe Indicator sont :

calculate_knn: Calcule les signaux de trading en utilisant l'algorithme K-nearest neighbors (KNN) pour les caractéristiques spécifiées.
calculate_obv: Calcule l'indicateur On Balance Volume (OBV) et l'ajoute au DataFrame.
calculate_rsi: Calcule l'indicateur Relative Strength Index (RSI) et l'ajoute au DataFrame.
calculate_super_trend: Calcule l'indicateur SuperTrend et l'ajoute au DataFrame.
calculate_ema: Calcule les moyennes mobiles exponentielles (EMA) à court et à long terme et les ajoute au DataFrame.
calculate_macd_crossover: Calcule les croisements de l'indicateur Moving Average Convergence Divergence (MACD) et les ajoute au DataFrame.

/  RUN  \
Lancer les tests historiques 

Pour lancer les tests historiques sur des données de marché, vous devez utiliser la classe Backtest avec les données historiques du marché que vous souhaitez tester. 
le fichier de référance est main.py


Mise à jour des données historiques
Pour charger de nouvelles données historiques, vous devez mettre à jour le fichier dll.js avec les informations de la paire de devises, de l'intervalle de temps et de la date de début. Voici un exemple de configuration :

pair_list = ["BTCUSDT"]
timeframe_list = ["1m"]
start_date = "01-01-2023"

Une fois le fichier dll.js mis à jour, vous pouvez exécuter le script pour générer de nouvelles données historiques au format CSV. Ces données seront stockées dans le dossier spécifié dans la configuration (par exemple, database/Bybit/1m/BTCUSDT.csv).
ex: node dll.js

Ensuite, mettez à jour le chemin du fichier CSV dans le script de test historique pour utiliser les nouvelles données :

csv_file_path = "nouveau_chemin_vers_le_fichier_csv"
historical_data = load_historical_data(csv_file_path)

Maintenant, vous pouvez exécuter à nouveau le script de test historique pour tester la stratégie de trading sur les nouvelles données historiques.


