from flask import Flask, render_template, redirect, request
import requests
import config


app = Flask(__name__)
forexAPI = 'https://www.freeforexapi.com/api/live'
newsAPIKEY = config.news_api_key
newsAPI = f'https://newsdata.io/api/1/news?apikey={newsAPIKEY}'

@app.route('/', methods=['GET', 'POST'])
def index():
    live = requests.get(forexAPI).json()
    pairs = live['supportedPairs']
    currencies = []
    for pair in pairs:
        firstCurrency = pair[0] + pair[1] + pair[2]
        secondCurrency = pair[3] + pair[4] + pair[5]
        if firstCurrency not in currencies:
            currencies.append(firstCurrency)
        if secondCurrency not in currencies:
            currencies.append(secondCurrency)
    currencies.sort()
    if request.method == 'POST':
        url = request.form.get('currency')
        return redirect(f'/currency/{url}')
    return render_template('index.html', currencies=currencies)

@app.route('/currency/<url>', methods=['GET', 'POST'])
def currency(url):
    live = requests.get(forexAPI).json()
    pairs = live['supportedPairs']

    emptyUrl = ""
    for pair in pairs:
        if url in pair:
            emptyUrl += f"{pair},"
    if emptyUrl[len(emptyUrl) - 1] == ",":
        emptyUrl = emptyUrl[:-1]
    urlPairs = f"{forexAPI}?pairs={emptyUrl}"
    rates = requests.get(urlPairs).json()
    viewRates = {}
    if rates['rates'] != None:
        for x, y in rates['rates'].items():
            viewRates[f"{x[0]}{x[1]}{x[2]}-{x[3]}{x[4]}{x[5]}"] = y['rate']
    
    if url == "EUR":
        country = "fr,de,it,nl,es"
    if url != "EUR":
        country = f"{url[0] + url[1]}"
    country.lower()

    news = requests.get(f'{newsAPI}&country={country}&category=business&language=en').json()
    if news['status'] == 'success':
        news = news['results']
        return render_template("currency.html",rates=rates ,viewRates=viewRates, news=news)

    if  news['status'] == 'error':
        return render_template("currency.html",rates=rates ,viewRates=viewRates)

@app.route('/news', methods=['GET', 'POST'])
def news():
    news = requests.get(f'{newsAPI}&country=US&category=business&language=en').json()
    if news['status'] == 'success':
        news = news['results']
    return render_template('news.html', news=news)