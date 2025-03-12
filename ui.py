import os
from datetime import datetime

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    if iteration == total: 
        print()

def getSortPreference():
    print("Sort by:")
    print("1. Total price")
    print("2. Average price")
    print("3. Latest trade date")
    print("4. Seller ID")
    sort_choice = input("Enter your choice >>> ")
    
    if sort_choice in ['1', '2', '3']:
        clr()
        print('Sorting method:')
        if sort_choice in ['1', '2']:
            print('1. Highest first')
            print('2. Lowest first')
        else:  # sort_choice == '3'
            print('1. Oldest first')
            print('2. Newest first')
            
        order_choice = input("Enter your choice >>> ")
        return sort_choice, order_choice
    
    return sort_choice, None

def displaySummary(summary, currency, convert_currency_func):
    now = datetime.now().astimezone()
    
    for i in summary:
        time_diff = now - i['latest_trade_date']
        days_ago = time_diff.days
        total_converted = round(convert_currency_func(float(i['total']), currency), 2)
        avg_converted = round(convert_currency_func(float(i['average']), currency), 2)
        print(f"Seller >>> {i['seller']} | Total >>> {total_converted} {currency} | Average item price >>> {avg_converted} {currency} | Last Trade >>> {days_ago} days ago")
    return input("Press any key to continue...")

def getCurrencyChoice():
    print("Select a currency:")
    print("1. USD")
    print("2. EUR")
    print("3. GBP")
    print("4. CNY")
    print("5. PLN")
    return input("Enter your choice >>> ")

def displayMenu(current_currency):
    clr()
    print("Select an option:")
    print("1. Show summary")
    print("2. Refresh data")
    print("3. Change session token")
    print(f"4. Change currency | Currently set to {current_currency}")
    print("5. Exit")
    return input("Enter your choice >>> ")

def getNewToken():
    return input("Enter your CSFloat session token >>> ")

def showMessage(message, wait_for_key=True):
    print(message)
    if wait_for_key:
        input("Press any key to continue...")
