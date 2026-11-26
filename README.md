# Aviator Lab

A **Telegram bot** for studying crash-game ("Aviator"-style) multipliers with statistics and simulation. You log real round results, the bot summarises them, and a Monte Carlo backtester shows how betting strategies perform against a fair crash model with a house edge.

The main lesson the bot teaches: **no strategy beats the house edge.** Every target multiplier and every staking system, Martingale included, loses about 3% per round on average.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)

## Commands

| Command | What it does |
| --- | --- |
| `/add 1.23 4.5 2.01x …` | Save one or more round multipliers to the local SQLite database |
| `/stats` | Rounds recorded, median multiplier, share of rounds under 2x, SMA(10) and RSI(14) |
| `/sim [target]` | Backtest a cash-out target (default `2.0`) over 100,000 simulated rounds, flat stake vs Martingale |

## How the simulation works

Crash points follow the standard fair model with a house edge `e` (3% by default):

```
P(multiplier ≥ x) = (1 − e) / x
```

The backtester bets one unit per round at your target, and either keeps the stake flat or doubles it after each loss (Martingale). It then reports the average profit per round. Both strategies come out close to −0.03 per round: Martingale only delays the losses until one very large loss.

## Getting started

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy its token.
2. Install and run:

```bash
git clone https://github.com/novasec-spec/aviator-lab.git
cd aviator-lab
pip install -r requirements.txt
export BOT_TOKEN="your-telegram-bot-token"
python server.py
```

Round data is stored in `rounds.db` (SQLite) next to the script.

## Files

| File | Purpose |
| --- | --- |
| `server.py` | The Telegram bot: storage, statistics and the backtester |
| `key.py` | Small Tkinter utility that logs key presses made inside its own window, with timestamps |
| `rounds.db` | SQLite database the bot creates to store rounds (starts empty) |

## Disclaimer

This project is for education and statistics practice only. It does not predict game outcomes, and past rounds say nothing about future ones. Gambling carries real financial risk.

## Author

Built by [John Munga (novasec-spec)](https://github.com/novasec-spec).
