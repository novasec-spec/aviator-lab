import os, sqlite3, random
import numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

db = sqlite3.connect("rounds.db", check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY, mult REAL)")

def history(n=500):
    rows = db.execute("SELECT mult FROM rounds ORDER BY id DESC LIMIT ?", (n,)).fetchall()
    return np.array([r[0] for r in rows][::-1])

def sma(x, n): return x[-n:].mean() if len(x) >= n else None

def rsi(x, n=14):
    if len(x) < n + 1: return None
    d = np.diff(x)[-n:]
    gain, loss = d[d > 0].sum() / n, -d[d < 0].sum() / n
    return 100.0 if loss == 0 else 100 - 100 / (1 + gain / loss)

def crash_point(edge=0.03):
    # fair crash model: P(mult >= x) = (1-edge)/x
    return max(1.0, (1 - edge) / (1 - random.random()))

def backtest(target, rounds=100_000, martingale=False):
    bank, stake, base, lows = 0.0, 1.0, 1.0, 0
    for _ in range(rounds):
        win = crash_point() >= target
        bank += stake * (target - 1) if win else -stake
        stake = base if (win or not martingale) else stake * 2
    return bank / rounds  # avg profit per round

async def add(u: Update, c: ContextTypes.DEFAULT_TYPE):
    for a in c.args:
        db.execute("INSERT INTO rounds(mult) VALUES(?)", (float(a.rstrip("x")),))
    db.commit()
    await u.message.reply_text(f"Saved {len(c.args)} rounds.")

async def stats(u, c):
    h = history()
    if len(h) == 0: return await u.message.reply_text("No data. Use /add 1.23 4.5 ...")
    await u.message.reply_text(
        f"Rounds: {len(h)}\nMedian: {np.median(h):.2f}x\n"
        f"Under 2x: {(h<2).mean()*100:.0f}%\nSMA10: {sma(h,10)}\nRSI14: {rsi(h)}")

async def sim(u, c):
    t = float(c.args[0]) if c.args else 2.0
    flat, mart = backtest(t), backtest(t, martingale=True)
    await u.message.reply_text(
        f"Target {t}x over 100k simulated rounds (1 unit stake):\n"
        f"Flat: {flat:+.4f}/round\nMartingale: {mart:+.4f}/round\n"
        f"Expected: about -0.03 either way. Martingale just hides losses until a big one.")

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
for name, fn in [("add", add), ("stats", stats), ("sim", sim)]:
    app.add_handler(CommandHandler(name, fn))
app.run_polling()
