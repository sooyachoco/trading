import pytest
from collective_alpha.paper import PaperBroker

def test_paper_buy_sell_and_costs(tmp_path):
    broker=PaperBroker(str(tmp_path/"paper.sqlite3"),initial_cash=1_000_000)
    buy=broker.order("011790","BUY",10,70_000)
    assert buy["mode"]=="PAPER_ONLY" and buy["gross"]==700_000 and buy["fee"]==350
    p=broker.portfolio(); assert p["cash"]==299_650 and p["positions"][0]["quantity"]==10
    sell=broker.order("011790","SELL",4,75_000)
    assert sell["gross"]==300_000 and sell["fee"]==150 and sell["tax"]==540
    p=broker.portfolio(); assert p["cash"]==598_960 and p["positions"][0]["quantity"]==6 and len(p["recent_trades"])==2

def test_cannot_sell_unowned_shares(tmp_path):
    broker=PaperBroker(str(tmp_path/"paper.sqlite3"),initial_cash=100_000)
    with pytest.raises(ValueError,match="Insufficient virtual shares"): broker.order("005930","SELL",1,70_000)

def test_rejects_invalid_orders(tmp_path):
    broker=PaperBroker(str(tmp_path/"paper.sqlite3"))
    for args in [("abc","BUY",1,100),("005930","BUY",0,100),("005930","HOLD",1,100),("005930","BUY",1,-1)]:
        with pytest.raises(ValueError): broker.order(*args)

def test_insufficient_cash_rolls_back(tmp_path):
    broker=PaperBroker(str(tmp_path/"paper.sqlite3"),initial_cash=100_000)
    with pytest.raises(ValueError,match="including simulated fee"): broker.order("005930","BUY",2,50_000)
    p=broker.portfolio(); assert p["cash"]==100_000 and p["positions"]==[] and p["recent_trades"]==[]
