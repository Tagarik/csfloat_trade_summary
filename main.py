from api import CSFloat
import asyncio, math, json, os, dotenv, time
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
    print('Data has been refreshed successfully')
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

def displaySummary(summary):
    now = datetime.now().astimezone()
    
    # Ask user for sorting preference
    print("Sort by:")
    print("1. Total price")
    print("2. Average price")
    print("3. Latest trade date")
    print("4. Seller ID")
    sort_choice = input("Enter your choice >>> ")
    clr()
    if sort_choice == '1':
        print('Sorting method:')
        print('1. Highest first')
        print('2. Lowest first')
        sort_choice = input("Enter your choice >>> ")
        if sort_choice == '1':
            summary.sort(key=lambda x: x['total'], reverse=True)
        elif sort_choice == '2':
            summary.sort(key=lambda x: x['total'])
        else:
            clr()
            print("Invalid choice, please try again.")
            input("Press any key to continue...")
            menu()
    elif sort_choice == '2':
        print('Sorting method:')
        print('1. Highest first')
        print('2. Lowest first')
        sort_choice = input("Enter your choice >>> ")
        if sort_choice == '1':
            summary.sort(key=lambda x: x['average'])
        elif sort_choice == '2':
            summary.sort(key=lambda x: x['average'], reverse=True)
        else:
            clr()
            print("Invalid choice, please try again.")
            input("Press any key to continue...")
            menu()
    elif sort_choice == '3':
        print('Sorting method:')
        print('1. Oldest first')
        print('2. Newest first')
        sort_choice = input("Enter your choice >>> ")
        if sort_choice == '1':
            summary.sort(key=lambda x: x['latest_trade_date'])
        elif sort_choice == '2':
            summary.sort(key=lambda x: x['latest_trade_date'], reverse=True)
        else:
            clr()
            print("Invalid choice, please try again.")
            input("Press any key to continue...")
            menu()
    elif sort_choice == '4':
        summary.sort(key=lambda x: x['seller'], reverse=True)

    for i in summary:
        time_diff = now - i['latest_trade_date']
        days_ago = time_diff.days
        print(f"Seller >>> {i['seller']} | Total >>> {round(float(i['total'])/100,2)} $ | Average item price >>> {round(float(i['average'])/100,2)} $ | Last Trade >>> {days_ago} days ago")
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