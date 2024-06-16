from mysql.connector import MySQLConnection
from db.connection import get_connection
from db.InvestorsDAO import InvestorDAO
from domain.Investor import Investor
from domain.Portfolio import Portfolio
from db.PortfolioDAO import PortfolioDAO
from db.StockDAO import StockDAO

def main():
    connection = get_connection()
    while True:
        print_menu()
        user_sel = input()
        if user_sel == '0':
            break
        if user_sel == '1':
            investor_dao = InvestorDAO(connection)
            print('List of unique investors:')
            investors = investor_dao.get_all()
            for investor in investors:
                print(investor)

        if user_sel == '2':
            stock_dao = StockDAO(connection)
            print('List of available stocks:')
            stocks = stock_dao.get_all_stocks()
            for stock in stocks:
                print(stock)

        if user_sel == '3':
            investor = input('Please enter an investor ID:\n')
            try:
                portfolio_dao = PortfolioDAO(connection)
                print('Portfolio Details:\n')
                portfolios = portfolio_dao.get_portfolio(investor)
                for portfolio in portfolios:
                    print(portfolio)

            except ValueError as e:
                print(str(e))

        if user_sel == '4':
            investor_id = input('Please enter an investor ID: \n')
            investor_dao = InvestorDAO(connection)
            investor = investor_dao.get_investor_by_id(investor_id)
            if investor is None:
                print("Invalid Investor ID")
                continue
            
            while True:
                action = input('Please select whether you want to deposit or withdraw funds:\n').upper()
                if action not in ['DEPOSIT', 'WITHDRAWAL']:
                    print('Invalid option. Please enter "DEPOSIT" or "WITHDRAWAL"')
                    continue
                break
            
            while True:
                amount_str = input('Please enter the amount:\n')
                try:
                    amount = float(amount_str)
                    break
                except ValueError:
                    print('Amount should be a number')
                    continue
                
            if action == 'DEPOSIT':
                investor_dao.deposit(investor_id, amount)
            else:
                investor_dao.withdrawal(investor_id, amount)

        if user_sel =='5':
            investor_id = input('Please enter an investor ID:\n')
            investor_dao = InvestorDAO(connection)
            investor = investor_dao.get_investor_by_id(investor_id)
            portfolio_dao = PortfolioDAO(connection)
            if investor is None:
                print("Invalid Investor ID")
                continue

            while True:
                stock_ticker = input('Please enter the ticker you would like to purchase:\n')
                stock_dao = StockDAO(connection)
                stock = stock_dao.get_stock_by_ticker(stock_ticker)
                if stock is None:
                    print('Stock does not exist.')
                    continue
                break
            while True:
                quantity = input('Please enter the quantity of stock you would like to purchase:\n')
                try:
                    quantity_int = int(quantity)
                except ValueError:
                    print('Quantity must be a number')
                portfolio_dao.add_stock(investor_id, stock_ticker, quantity_int)
                break
            print('Transaction Sucessful.')

        if user_sel =='6':
            investor_id = input('Please enter an investor ID:\n')
            investor_dao = InvestorDAO(connection)
            investor = investor_dao.get_investor_by_id(investor_id)
            portfolio_dao = PortfolioDAO(connection)
            if investor is None:
                print("Invalid Investor ID")
                continue

            while True:
                stock_ticker = input('Please enter the ticker you would like to sell:\n')
                stock_dao = StockDAO(connection)
                stock = stock_dao.get_stock_by_ticker(stock_ticker)
                if stock is None:
                    print('Stock does not exist.')
                    continue
                break
            while True:
                quantity = input('Please enter the quantity of stock you would like to sell:\n')
                try:
                    quantity_int = int(quantity)
                except ValueError:
                    print('Quantity must be a number')

                break

            while True:
                sell_price = input('Please enter the selling price you would like.\n')
                try:
                    sell_price_float = float(sell_price)
                except ValueError:
                    print('Sell price must be a number')
                portfolio_dao.sell_stock(investor_id, stock_ticker, quantity_int, sell_price_float)
                break
            
        if user_sel == '7':
            while True:
                investor_id = input('Please enter the investor id: \n')
                try:
                    investor_id_int = int(investor_id)
                except ValueError:
                    print('Investor ID must be a number')
                    continue
                investor_dao = InvestorDAO(connection)
                investor = investor_dao.get_investor_by_id(investor_id_int)
                if investor is None:
                    print('Invalid Investor ID')
                    continue
                confirmation = input('Are you sure you want to delete the investor(Y/N)?\n')
                if confirmation == 'Y':
                    investor_dao.delete(investor.id)
                    print('Investor Deleted successfully')
                    break
                elif confirmation == 'N':
                    break
                else:
                    print('Invalid Confirmation Value.')
                    continue



def print_menu():
    print('Please select from the options below:')
    print('1. Get a list of all investors.')
    print('2. Get a list of all stock offerings.')
    print('3. Show portfolio details for an investor.')
    print('4. Deposit or Withdraw money from an account')
    print('5. Purchase a stock from the offerings.')
    print('6. Sell a stock from investor portfolio.')
    print('7. Delete an investor')
    print('0. Exit App.')
    print('Your Choice -> ')

if __name__ == "__main__":
    main()