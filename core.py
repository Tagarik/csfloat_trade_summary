from api import CSFloat, Currencies
import math, json, os, dotenv
from datetime import datetime

currencyApi = Currencies()

async def fetchCurrencies():
    await currencyApi.fetchCurrencies()

def updateToken(newToken):
    os.environ['SESSION_TOKEN'] = newToken
    dotenv.set_key(dotenv.find_dotenv(), 'SESSION_TOKEN', newToken)
    return True

async def fetchTradeData():
    if os.environ['SESSION_TOKEN'] == '':
        # Instead of returning a value, yield a status object
        yield {'status': 'error', 'message': 'No session token set'}
        return  # No value with return in generator
        
    AnalysisData = []
    csfloat = CSFloat(os.environ['SESSION_TOKEN'])
    count = await csfloat.requestTradeData('buyer', 0)
    pages = math.ceil(int(count['count']) / 50)
    if pages > 29:
        pages = 30
        
    progress_data = {'status': 'progress', 'total': pages, 'current': 0}
    
    for i in range(pages):
        progress_data['current'] = i + 1
        yield progress_data  # This allows the UI to show progress
        
        tradeData = await csfloat.requestTradeData('buyer', i)
        for x in tradeData['trades']:
            AnalysisData.append({
                'item': x['contract']['item']['market_hash_name'],
                'price': x['contract']['price'],
                'seller': x['seller']['steam_id'],
                'date': x['accepted_at']
            })
            
    json.dump(AnalysisData, open('AnalysisData.json', 'w'), indent=4)
    # Final yield with completion status instead of return
    yield {'status': 'completed'}

def sellerList(data):
    sellers = set()  # Use a set to ensure unique sellers
    for i in data:
        sellers.add(i['seller'])
    return list(sellers)

def createSummary(sellers, data):
    summary = []
    for i in sellers:
        total = 0
        count = 0
        latest_date = None
        for x in data:
            if i == x['seller']:
                total += x['price']
                count += 1
                trade_date = datetime.fromisoformat(x['date'].replace('Z', '+00:00'))
                if latest_date is None or trade_date > latest_date:
                    latest_date = trade_date
        summary.append({
            'seller': i,
            'total': total,
            'average': total / count,
            'latest_trade_date': latest_date
        })
    return summary
    
def loadAnalysisData():
    try:
        with open('AnalysisData.json') as raw_data:
            data = json.load(raw_data)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def convertCurrency(amount, currency):
    return currencyApi.convertCurrency(amount/100, currency)
