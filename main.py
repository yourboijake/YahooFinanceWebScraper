from bs4 import BeautifulSoup
import requests
import pandas as pd
from matplotlib import pyplot as plt

#get all stock data
page_a = requests.get('https://finance.yahoo.com/quote/AAPL/history?period1=1569740400&period2=1577606400&interval=1d&filter=history&frequency=1d')
page_b = requests.get('https://finance.yahoo.com/quote/AAPL/history?period1=1561791600&period2=1569740400&interval=1d&filter=history&frequency=1d')
page_c = requests.get('https://finance.yahoo.com/quote/AAPL/history?period1=1553842800&period2=1561791600&interval=1d&filter=history&frequency=1d')
page_d = requests.get('https://finance.yahoo.com/quote/AAPL/history?period1=1546070400&period2=1553842800&interval=1d&filter=history&frequency=1d')

#convert raw request data to beautiful soup objects
soup_a = BeautifulSoup(page_a.content, 'html.parser')
soup_b = BeautifulSoup(page_b.content, 'html.parser')
soup_c = BeautifulSoup(page_c.content, 'html.parser')
soup_d = BeautifulSoup(page_d.content, 'html.parser')

#creates 'raw_price_data' string to store all the raw html data
data = soup_a.find_all(class_="smartphone_Px(20px)")
raw_price_data = data[0].get_text()
data = soup_b.find_all(class_="smartphone_Px(20px)")
raw_price_data += data[0].get_text()
data = soup_c.find_all(class_="smartphone_Px(20px)")
raw_price_data += data[0].get_text()
data = soup_d.find_all(class_="smartphone_Px(20px)")
raw_price_data += data[0].get_text()

#provides columns for data frame
price_dictionary = {"Date:": [],
                    "Close Price:": []}

#used to index the process of grabbing data from raw_price_data
months = ["Dec", "Nov", "Oct", "Sep", "Aug", "Jul", "Jun", "May",
          "Apr", "Mar", "Feb", "Jan"]

#gets the price data, properly indexed
for x in range(30, len(raw_price_data)-36):
    if raw_price_data[x:x+3] in months and 'Dividend' not in raw_price_data[x:x+30]:
        price_dictionary["Date:"].append(raw_price_data[x:x+12])
        price_dictionary["Close Price:"].append(float(raw_price_data[x+30:x+36]))

#converts price_dictionary into a dataframe
stock_df = pd.DataFrame(price_dictionary)

#creates excel sheet with the stock data
stock_df.to_excel("stock data.xlsx")

#prints the properly ordered stock data
stock_df = stock_df.sort_index(ascending=False, axis=0)
stock_df.plot(kind='line', x="Date:", y="Close Price:")
plt.show()

