from flask import Flask
from flask import render_template
from flask import request
import json
import yfinance as yf
import datetime

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def yfinancetut(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    stock = tickerinfo['shortName']
    return stock

def yfinanceOpen(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    todaysDate = datetime.datetime.today().isoformat()
    tickerHistory = tickerdata.history(period='id',start='2000-1-1',end=todaysDate[:10])
    lastOpen = tickerHistory['Open'].iloc[-10]
    OpenInt = int(lastOpen)
    Open = OpenInt
    return Open

def yfinanceClose(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    todaysDate = datetime.datetime.today().isoformat()
    tickerHistory = tickerdata.history(period='id',start='2000-1-1',end=todaysDate[:10])
    lastClose = tickerHistory['Close'].iloc[-10]
    closeInt = int(lastClose)
    close = closeInt
    return close

def yfinanceAVG(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    avg = tickerinfo['fiftyDayAverage']
    return avg

def yfPtoE(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    PricetoEarnings = tickerinfo['forwardPE']
    return PricetoEarnings

def yfBeta(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    beta = tickerinfo['beta']
    return beta

def yfMtkCap(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    cap = tickerinfo['marketCap']
    return cap

def yfFiveYearDividend(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    hold = tickerinfo['fiveYearAvgDividendYield']
    return hold

def yfYearlyHigh(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    hold = tickerinfo['fiftyTwoWeekHigh']
    return hold

def yfSector(tickersymbol):
    tickerdata = yf.Ticker(tickersymbol)
    tickerinfo = tickerdata.info
    hold = tickerinfo['sector']
    return hold



app = Flask(__name__)
@app.route('/')
def stockInfo(ticker='msft'):
    """ Return a greeting """
    title = "Stock Data"
    stock = yfinancetut(ticker)
    open = yfinanceOpen(ticker)
    close = yfinanceClose(ticker)
    fifty_day = yfinanceAVG(ticker)
    PE = yfPtoE(ticker)
    beta = yfBeta(ticker)
    marketCap = yfMtkCap(ticker)
    avergedDividend = yfFiveYearDividend(ticker)
    sector = yfSector(ticker)
    yearlyHigh = yfYearlyHigh(ticker)
    return render_template('about.html', title=title, stock=stock,
                           open=open, close=close, fifty_day=fifty_day, PE=PE,
                           beta=beta, marketCap=marketCap, dividend=avergedDividend,
                           sector=sector, yearlyHigh=yearlyHigh)


@app.route('/ticker')
def getTicker():
    title = "Stock Info"
    tickerVar = request.args.get('ticker')
    stock = yfinancetut(tickerVar)
    open = yfinanceOpen(tickerVar)
    close = yfinanceClose(tickerVar)
    fifty_day = yfinanceAVG(tickerVar)
    PE = yfPtoE(tickerVar)
    beta = yfBeta(tickerVar)
    marketCap = yfMtkCap(tickerVar)
    avergedDividend = yfFiveYearDividend(tickerVar)
    sector = yfSector(tickerVar)
    yearlyHigh = yfYearlyHigh(tickerVar)
    error = "You have not entered a comparison ticker: You are now comparing to Benchmarks."

    tickerVar2 = request.args.get('ticker2')

    if tickerVar:
        if tickerVar2:
            stock2 = yfinancetut(tickerVar2)
            open2 = yfinanceOpen(tickerVar2)
            close2 = yfinanceClose(tickerVar2)
            fifty_day2 = yfinanceAVG(tickerVar2)
            PE2 = yfPtoE(tickerVar2)
            beta2 = yfBeta(tickerVar2)
            marketCap2 = yfMtkCap(tickerVar2)
            avergedDividend2 = yfFiveYearDividend(tickerVar2)
            sector2 = yfSector(tickerVar2)
            yearlyHigh2 = yfYearlyHigh(tickerVar2)

            peComparison = round(PE/PE2, 5)
            capComparison = round(int(marketCap)/int(marketCap2), 5)
            betaComparison = round(beta/beta2, 5)
            divComparison = round(avergedDividend/avergedDividend2, 5)

            return render_template('testingInputs.html', title=title, tickerVar=tickerVar,
                                   stock=stock, open=open, close=close, fifty_day=fifty_day, PE=PE,
                                   tickerVar2=tickerVar2, beta=beta, marketCap=marketCap, dividend=avergedDividend,
                                   sector=sector, yearlyHigh=yearlyHigh,
                                   stock2=stock2, open2=open2, close2=close2, fifty_day2=fifty_day2, PE2=PE2,
                                   beta2=beta2, marketCap2=marketCap2, dividend2=avergedDividend2, sector2=sector2,
                                   yearlyHigh2=yearlyHigh2, peComparison=peComparison,capComparison=capComparison,
                                   betaComparison=betaComparison, divComparison=divComparison)
        else:
            count = 0
            if PE > 50:
                peText = "is higher than our benchmark"
            else:
                peText = "is within our benchmark"
                count += 1
            if beta > 1.5:
                betaText = "is higher than our benchmark"
            else:
                betaText = "is within our benchmark"
                count += 1
            if marketCap < 100000000000:
                marketText = "is lower than our benchmark"
            else:
                marketText = "is within our benchmark"
                count += 1
            if avergedDividend < 1:
                divText = "is lower than our benchmark"
            else:
                divText = "is within our benchmark"
                count += 1

            return render_template('home.html', title=title, tickerVar=tickerVar,
                                   stock=stock, open=open, close=close, fifty_day=fifty_day, PE=PE,
                                   beta=beta, marketCap=marketCap, dividend=avergedDividend,
                                   sector=sector, yearlyHigh=yearlyHigh, error=error, count=count,
                                   peText=peText, betaText=betaText, marketText=marketText, divText=divText)



if __name__ == '__main__':
    app.run(debug=True)
else:
    None
