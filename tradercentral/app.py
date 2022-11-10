from flask import Flask, render_template, redirect, request
import requests


app = Flask(__name__)
forexAPI = 'https://www.freeforexapi.com/api/live'
newsAPIKEY = 'pub_11972791983aeced716007f550b28902779f0'
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
    #print(rates)
    if rates['rates'] != None:
        for x, y in rates['rates'].items():
            viewRates[x] = y['rate']
    
    if url == "EUR":
        country = "fr,de,it,nl,es"
    if url != "EUR":
        country = f"{url[0] + url[1]}"
    country.lower()

    if requests.get(f'{newsAPI}&country={country}&category=business&language=en').json()['status'] == 'success':
        news = requests.get(f'{newsAPI}&country={country}&category=business&language=en').json()
        #print(news)
        articleTitles = []
        articleBody = []
        articleLink = []
        for article in news['results']:
            if article['title'] == None:
                articleTitles.append(None)
            articleTitles.append(article['title'])
            if article['content'] == None:
                articleBody.append(None)
            articleBody.append(article['content'])
            if article['link'] == None:
                articleLink.append(None)
            articleLink.append(article['link'])
        return render_template("currency.html",rates=rates ,viewRates=viewRates, articleBody=articleBody, articleTitles=articleTitles, articleLink=articleLink)

    if  requests.get(f'{newsAPI}&country={country}&category=business&language=en').json()['status'] == 'error':
        return render_template("currency.html",rates=rates ,viewRates=viewRates)

@app.route('/news', methods=['GET', 'POST'])
def news():
    return render_template('news.html')