import requests
from bs4 import BeautifulSoup
import time

# names of cryptocurrencies of which you want to now the price
crypto_to_find = ["bitcoin", "ethereum", "eos", "xrp", "stellar", "cardano", "elrond"]
# amount of each above listed currency
amount_of_each_coin = [0.00212823, 0.03362318, 7.5372, 30.354818, 81.6360419, 53.128107, 0.1287]
# the price you payed for each currency
purchase_price_of_each_coin = [466.24, 243.40, 150.00, 100.00, 150.00, 254.61, 28.80 * 3.83]

start = '>$'
end = '</div>'

if len(crypto_to_find) != len(amount_of_each_coin) != len(purchase_price_of_each_coin):
    # you may want to check the if you didn't forget anything in the above lists
    print("something is wrong with list lenghts")
    quit()

while True:
    price_of_each_coin = []
    paragraphs = []
    # scraping info from https://coinmarketcap.com/"name of currency"/markets/
    for crypto in crypto_to_find:
        URL = 'https://coinmarketcap.com/currencies/' + crypto + '/markets/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='priceValue___11gHJ')
        paragraphs.append(str(results[0]))

    x = 0
    # formatting our info into some usable strings
    for info in paragraphs:
        price = float(info[info.find(start) + len(start):info.rfind(end)].strip().replace(",", ""))
        price_of_each_coin.append(price)
        print(crypto_to_find[x] + ':' + ' ' * (25 - len(str(price)) - len(crypto_to_find[x])) + str(
            price) + '$' + '     ' + str(amount_of_each_coin[x] * price_of_each_coin[x])[0:8] + '$')
        x += 1
    x = 0
    price, suma = 0.0, 0.0
    print("\n" * 2)
    # open a text file for storing our data
    f = open("crypto_stats.txt", "a")
    f.write("-" * 40 + '\n')
    # finding out how much money we've made
    for crypto in crypto_to_find:
        price = float(amount_of_each_coin[x] * price_of_each_coin[x] * 3.82) #converting $ to any currency (change 3.82)
        price -= float(purchase_price_of_each_coin[x])
        # total sum of our earnings
        suma = suma + price
        print(crypto + ':' + ' ' * (30 - len(str(price)) - len(crypto_to_find[x])) + str(price)[0:6] + 'zł')
        f.write(crypto + ':' + ' ' * (30 - len(str(price)) - len(crypto_to_find[x])) + str(price)[0:6] + 'zł\n')
        x += 1

    print("\nGain: " + str(suma)[0:7])
    # Yay
    if suma > 0:
        f.write("\n\n               Gain: " + str(suma)[0:6] + 'zł' + '\n')
    # :((
    else:
        f.write("\n\n               Loss: " + str(suma)[0:6] + 'zł' + '\n')

    f.close()
    # repeat after 5min
    time.sleep(60 * 5)
