import random, datetime, time
from .models import trader_collection, trades

def total_earning(record):
    sum = 0
    if record:
        for x in record:            
            val = x['stake_return']
            sum += val        
        return sum
    

def total_loss(record):
    sum = 0
    if record:
        for x in record:            
            val = x['stake_return']
            sum += abs(val)
        return sum


def simulate_profit_loss():
    return round(random.uniform(-5, 5), 2)  # Simulating profit/loss between -5 and 5 dollars

def simulate_trading():
    while True:
        traders = trader_collection.find()

        if traders:
            for x in traders:
                tid = x['_id']
                stv = x['stock_value'] # trader current stock amount balance
                nowDate = datetime.datetime.now() # time trade was taken
                trade_turnout = simulate_profit_loss() # trade turnout

                if stv != 0: # check trader's stock balance
                    if trade_turnout > 0:
                        stv += trade_turnout 
                        status = 'profit'
                    
                    if trade_turnout < 0:
                        stv -= abs(trade_turnout) 
                        status = 'loss'
                    
                    balance = stv

                    record = {
                        "trader_id": tid,
                        "timestamp": nowDate,
                        "entry_balance": x['stock_value'],
                        "status": status,
                        "stake_return": trade_turnout,
                        "balance": balance
                    }
                    
                    trades.insert_one(record)
                    
                    trader_collection.update_one(
                        {'_id': tid},
                        {'$set': {'stock_value': balance}}
                    )

        time.sleep(60)

