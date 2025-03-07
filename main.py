from api import CSFloat
import asyncio, pprint, math, json, os, dotenv, time
from datetime import datetime

def changeToken():
    newToken = input("Enter your CSFloat session token >>> ")
    os.environ['SESSION_TOKEN'] = newToken
    dotenv.set_key(dotenv.find_dotenv(), 'SESSION_TOKEN', newToken)
    clr()
    print("Token has been changed successfully!")
    input("Press any key to continue...")

async def refresh():
    AnalysisData = []
    if os.environ['SESSION_TOKEN'] == '':
        print("Please set your session token first.")
        input("Press any key to continue...")
        return
    csfloat = CSFloat(os.environ['SESSION_TOKEN'])
    print('Fetching data...')
    count = await csfloat.requestTradeData('buyer', 0)
    pages = math.ceil(int(count['count']) / 50)
    if pages > 29:
        pages = 30
    for i in range(pages):

        printProgressBar(i + 1, pages, prefix = 'Progress:', suffix = 'Complete', length = 50)
        tradeData = await csfloat.requestTradeData('buyer', i)
        for x in tradeData['trades']:
            AnalysisData.append({
                'item': x['contract']['item']['market_hash_name'],
                'price': x['contract']['price'],
                'seller': x['seller']['steam_id'],
                'date': x['accepted_at']
            })
    clr()
    json.dump(AnalysisData, open('AnalysisData.json', 'w'), indent=4)
    pprint.pprint('Data has been refreshed successfully')
    input("Press any key to continue...")

def AnalyseData():
    summary = []
    
    with open('AnalysisData.json') as raw_data:
        if raw_data is None:
            print("No data found, please refresh data first.")
            input("Press any key to continue...")
            return
        data = json.load(raw_data)
        sellers = sellerList(data)
        summary = createSummary(sellers, data)  
    displaySummary(summary)

        
def sellerList(data):
    sellers = []
    for i in data:
        if i['seller'] not in sellers:
            sellers.append(i['seller'])
    return sellers

def createSummary(sellers, data):
    summary = []
    for i in sellers:
        total : int = 0
        count : int = 0
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

def displaySummary(summary):
    now = datetime.now().astimezone()
    for i in summary:
        time_diff = now - i['latest_trade_date']
        days_ago = time_diff.days
        print(f"Seller >>> {i['seller']} | Total >>> {i['total']} | Average >>> {i['average']} | Last Trade >>> {days_ago} days ago")
    input("Press any key to continue...")
    menu()

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def menu():
    while True:
        clr()
        print("Select an option:")
        print("1. Show summary")
        print("2. Refresh data")
        print("3. Change session token")
        print("4. Exit")
        choice = input("Enter your choice >>> ")

        if choice == '1':
            clr()
            AnalyseData()
        if choice == '2':
            clr()
            asyncio.run(refresh())
        elif choice == '3':
            clr()
            changeToken()
        elif choice == '4':
            clr()
            print("Exiting...")
            time.sleep(1)
            break
        else:
            clr()
            print("Invalid choice, please try again.")
            time.sleep(5)
            clr()

if __name__ == '__main__':
    dotenv.load_dotenv(dotenv.find_dotenv())
    menu()