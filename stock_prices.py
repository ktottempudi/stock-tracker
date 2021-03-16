# Stock Market Web Scraping
import urllib.request  # Used to access website
import urllib.parse  # Parse Data
import re  # Regular expression
from bs4 import BeautifulSoup  # Import BeautifulSoup for data parsing


# Overwrites text file for previously saved stocks
def overwrite_stock(list_stock):
    stock_pen = open("stock_list.txt", "w")
    stock_pen.write("\n".join(list_stock))
    stock_pen.close()


# Check to see if stock has already been saved
def check_stock(name, price):
    print(name + price)
    is_repeated = False
    new_list = list()
    stock_check = open("stock_list.txt", "r")
    for stock in stock_check:
        check = stock.split()[0]
        if check == name:
            new_entry = name + " $" + price
            new_list.append(new_entry)
            is_repeated = True
        else:
            new_list.append(stock)
    if is_repeated:
        stock_check.close()
        overwrite_stock(new_list)
    else:
        stock_check.close()
        save_stock(name, price)


# Deciding to stop
def stop_or_not():
    stop = input("Do you wish to quit y/n: ")
    if stop == "n":
        first_decide()
    elif stop == "y":
        print("Done")


# Displays all previous saved stocks
def read_stocks():
    stock_read = open("stock_list.txt", "r+")
    for stock in stock_read:
        print(stock)
    stock_read.close()
    stop_or_not()


# Clear all previously saved stocks
def clear_stocks():
    stock_clear = open("stock_list.txt", "w")
    stock_clear.close()
    stop_or_not()


# Saves company price and name to txt file
def save_stock(name, price):
    saved_entry = name + " $" + price
    stock_list = open("stock_list.txt", "a")  # Open text file to append
    stock_list.write(saved_entry + "\n")  # Append information on new line
    stock_list.close()
    stop_or_not()


def retrieve_price(company):
    link = "https://www.google.com/search?q=" + str(company) + "+stock+price"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 '
                             '(HTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}  # Browser Versions
    request = urllib.request.Request(link, headers=headers)  # Access to website
    response = urllib.request.urlopen(request)
    data = response.read()
    price = data.decode('utf8')
    stock_info = BeautifulSoup(price, "html.parser")
    stock_price_info = stock_info.find("span", {"class": "IsqQVc NprOob XcVN5d"})  # Find line where price is indicated
    value = re.findall(r'\b\d+\.\d+\b', str(stock_price_info))  # Parses data to find stock price and saves it to list
    stock_price = value[0]  # saves stock price to variable
    print("The stock price of " + company + " = $" + stock_price)
    save_choice = input("Do you wish to save this entry y/n: ")
    if save_choice == "y":
        check_stock(company.upper(), stock_price)
        # save_stock(company.upper(), stock_price)
        # first_decide()
    else:
        stop_or_not()


def first_decide():
    stock_lists = open("stock_list.txt")
    if len(list(stock_lists)) == 0:  # Checks to see if anything is in the txt file
        corporation = input("Enter company to check stock price: ")
        retrieve_price(corporation)
    else:
        choice = input("Enter s to search for stock price or w to look at previously saved stocks: ")
        if choice == "s":
            corporate = input("Enter company to check stock price: ")
            retrieve_price(corporate)
        if choice == "w":
            options = input("Enter r to display all saved stocks or c to clear all stocks: ")
            if options == "r":
                read_stocks()
            elif options == "c":
                clear_stocks()
            else:
                print("Not a valid option.")
                stop_or_not()
        else:
            print("Not a valid option")
            stop_or_not()
    stock_lists.close()


first_decide()
