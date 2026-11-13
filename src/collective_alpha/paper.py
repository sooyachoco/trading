import sqlite3
from pathlib import Path
from datetime import datetime, timezone

class PaperBroker:
    """Local SQLite simulated broker. It never connects to a brokerage account."""
    def __init__(self, db_path: str, initial_cash: int = 10_000_000, fee_bps: int = 5, sell_tax_bps: int = 18):
        if initial_cash < 0: raise ValueError("initial_cash cannot be negative")
        if fee_bps < 0 or sell_tax_bps < 0: raise ValueError("fee and tax rates cannot be negative")
        self.db_path, self.fee_bps, self.sell_tax_bps = db_path, fee_bps, sell_tax_bps
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS paper_account(id INTEGER PRIMARY KEY CHECK(id=1), cash INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS paper_positions(symbol TEXT PRIMARY KEY, quantity INTEGER NOT NULL, avg_price REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS paper_trades(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, symbol TEXT NOT NULL,
            side TEXT NOT NULL, quantity INTEGER NOT NULL, price REAL NOT NULL, gross INTEGER NOT NULL, fee INTEGER NOT NULL,
            tax INTEGER NOT NULL, net_cash_change INTEGER NOT NULL);''')
            db.execute("INSERT OR IGNORE INTO paper_account(id,cash) VALUES(1,?)", (initial_cash,))
    def _db(self):
        db = sqlite3.connect(self.db_path, timeout=15)
        db.execute("PRAGMA busy_timeout=15000")
        return db
    def portfolio(self):
        with self._db() as db:
            cash = db.execute("SELECT cash FROM paper_account WHERE id=1").fetchone()[0]
            positions = db.execute("SELECT symbol,quantity,avg_price FROM paper_positions ORDER BY symbol").fetchall()
            trades = db.execute("SELECT ts,symbol,side,quantity,price,gross,fee,tax,net_cash_change FROM paper_trades ORDER BY id DESC LIMIT 20").fetchall()
        return {"mode":"PAPER_ONLY","cash":cash,"positions":[{"symbol":s,"quantity":q,"avg_price":p} for s,q,p in positions],
            "recent_trades":[{"timestamp":t,"symbol":s,"side":side,"quantity":q,"price":p,"gross":g,"fee":f,"tax":tax,"net_cash_change":net} for t,s,side,q,p,g,f,tax,net in trades]}
    def order(self, symbol: str, side: str, quantity: int, price: float):
        symbol, side = symbol.strip().zfill(6), side.upper().strip()
        if not (symbol.isdigit() and len(symbol) == 6): raise ValueError("symbol must be a six-digit numeric stock code")
        if side not in {"BUY","SELL"}: raise ValueError("side must be BUY or SELL")
        if isinstance(quantity,bool) or not isinstance(quantity,int) or quantity <= 0: raise ValueError("quantity must be a positive integer")
        if price <= 0: raise ValueError("price must be positive")
        gross = round(quantity * price); fee = round(gross * self.fee_bps / 10000)
        tax = round(gross * self.sell_tax_bps / 10000) if side == "SELL" else 0
        net = -(gross + fee) if side == "BUY" else gross - fee - tax
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            cash = db.execute("SELECT cash FROM paper_account WHERE id=1").fetchone()[0]
            row = db.execute("SELECT quantity,avg_price FROM paper_positions WHERE symbol=?",(symbol,)).fetchone()
            held, avg = row if row else (0,0.0)
            if side == "BUY":
                if gross + fee > cash: raise ValueError("Insufficient virtual cash, including simulated fee.")
                new_qty = held + quantity; new_avg = ((held * avg) + gross + fee) / new_qty
                db.execute("UPDATE paper_account SET cash=cash+? WHERE id=1",(net,))
                db.execute("INSERT INTO paper_positions VALUES(?,?,?) ON CONFLICT(symbol) DO UPDATE SET quantity=excluded.quantity,avg_price=excluded.avg_price",(symbol,new_qty,new_avg))
            else:
                if quantity > held: raise ValueError("Insufficient virtual shares.")
                db.execute("UPDATE paper_account SET cash=cash+? WHERE id=1",(net,))
                if quantity == held: db.execute("DELETE FROM paper_positions WHERE symbol=?",(symbol,))
                else: db.execute("UPDATE paper_positions SET quantity=? WHERE symbol=?",(held-quantity,symbol))
            db.execute("INSERT INTO paper_trades(ts,symbol,side,quantity,price,gross,fee,tax,net_cash_change) VALUES(?,?,?,?,?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(),symbol,side,quantity,price,gross,fee,tax,net))
        return {"status":"SIMULATED_FILLED","mode":"PAPER_ONLY","symbol":symbol,"side":side,"quantity":quantity,
                "price":price,"gross":gross,"fee":fee,"tax":tax,"net_cash_change":net}
