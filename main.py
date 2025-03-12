import asyncio, os, dotenv, time
import core
import ui

currency = 'USD'

def changeToken():
    newToken = ui.getNewToken()
    core.updateToken(newToken)
    ui.clr()
    ui.showMessage("Token has been changed successfully!")

async def refresh():
    if os.environ['SESSION_TOKEN'] == '':
        ui.showMessage("Please set your session token first.")
        return
        
    print('Fetching data...')
    
    completed = False
    async for data in core.fetchTradeData():
        if data['status'] == 'error':
            ui.showMessage(data['message'])
            return
        elif data['status'] == 'progress':
            ui.printProgressBar(
                data['current'], 
                data['total'], 
                prefix='Progress:', 
                suffix='Complete', 
                length=50
            )
        elif data['status'] == 'completed':
            completed = True
    
    if completed:
        ui.clr()
        ui.showMessage('Data has been refreshed successfully')
    else:
        ui.showMessage('Error occurred while refreshing data')

def AnalyseData():
    data = core.loadAnalysisData()
    if data is None:
        ui.showMessage("No data found, please refresh data first.")
        return
        
    sellers = core.sellerList(data)
    summary = core.createSummary(sellers, data)
    
    sort_choice, order_choice = ui.getSortPreference()
    ui.clr()
    
    if sort_choice == '1':  # Total price
        summary.sort(key=lambda x: x['total'], reverse=(order_choice == '1'))
    elif sort_choice == '2':  # Average price
        summary.sort(key=lambda x: x['average'], reverse=(order_choice == '1'))
    elif sort_choice == '3':  # Latest trade date
        summary.sort(key=lambda x: x['latest_trade_date'], reverse=(order_choice == '2'))
    elif sort_choice == '4':  # Seller ID
        summary.sort(key=lambda x: x['seller'], reverse=True)
    else:
        ui.clr()
        ui.showMessage("Invalid choice, please try again.")
        return
        
    ui.displaySummary(summary, currency, core.convertCurrency)
    menu()

def changeCurrency():
    global currency
    currency_choice = ui.getCurrencyChoice()
    
    if currency_choice == '1':
        currency = 'USD'
    elif currency_choice == '2':
        currency = 'EUR'
    elif currency_choice == '3':
        currency = 'GBP'
    elif currency_choice == '4':
        currency = 'CNY'
    elif currency_choice == '5':
        currency = 'PLN'
    else:
        ui.clr()
        print("Invalid choice, please try again.")
        time.sleep(5)

def menu():
    global currency
    while True:
        choice = ui.displayMenu(currency)

        if choice == '1':
            ui.clr()
            AnalyseData()
        if choice == '2':
            ui.clr()
            asyncio.run(refresh())
        elif choice == '3':
            ui.clr()
            changeToken()
        elif choice == '4':
            ui.clr()
            changeCurrency()
        elif choice == '5':
            ui.clr()
            print("Exiting...")
            time.sleep(1)
            os._exit(0)
        else:
            ui.clr()
            print("Invalid choice, please try again.")
            time.sleep(5)
            ui.clr()

if __name__ == '__main__':
    dotenv.load_dotenv(dotenv.find_dotenv())
    asyncio.run(core.fetchCurrencies())
    menu()