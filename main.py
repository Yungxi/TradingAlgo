from requests import get

from requests.exceptions import RequestException

from contextlib import closing

from bs4 import BeautifulSoup



def simple_get(url):

    """

    Attempts to get the content at `url` by making an HTTP GET request.

    If the content-type of response is some kind of HTML/XML, return the

    text content, otherwise return None.

    """

    try:

        with closing(get(url, stream=True)) as resp:

            if is_good_response(resp):

                return resp.content

            else:

                return None



    except RequestException as e:

        log_error('Error during requests to {0} : {1}'.format(url, str(e)))

        return None





def is_good_response(resp):

    """

    Returns True if the response seems to be HTML, False otherwise.

    """

    content_type = resp.headers['Content-Type'].lower()

    return (resp.status_code == 200

            and content_type is not None

            and content_type.find('html') > -1)





def log_error(e):

    """

    It is always a good idea to log errors.

    This function just prints them, but you can

    make it do anything.

    """

    print(e)



while True:
    ticker = input('Enter Stock Ticker: ')

    if ticker == 'close':
        break

    # Closing Price
    raw_html = simple_get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch')

    html = BeautifulSoup(raw_html, 'html.parser')

    Price = html.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text.replace(',', '')

    NumPrice = float(Price)

    print('Closing Price:', NumPrice)

    # weekly low
    Lowraw_html = simple_get(
        'https://finance.yahoo.com/quote/' + ticker + '/history?period1=1584704232&period2=1616240232&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true')

    weekLow = BeautifulSoup(Lowraw_html, 'html.parser')

    weeklyLow = weekLow.find_all('td', {'class': 'Py(10px) Pstart(10px)'})

    NumWeeklyLow = float(weeklyLow[2].text.replace(',', ''))

    print("Week Low:", NumWeeklyLow)

    # weekly high
    weekHigh = BeautifulSoup(Lowraw_html, 'html.parser')

    weeklyHigh = weekHigh.find_all('td', {'class': 'Py(10px) Pstart(10px)'})

    NumWeeklyHigh = float(weeklyHigh[1].text.replace(',', ''))

    print('Week High', NumWeeklyHigh)

    # 200 day moving average

    moving_html = simple_get('https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker)

    movingAverage = BeautifulSoup(moving_html, 'html.parser')

    twoMovingAverage = movingAverage.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})

    print("200 Day Moving Average:", twoMovingAverage[15].text.replace(',', ''))

    NumMovingAvearge = float(twoMovingAverage[15].text.replace(',', ''))

    # algo
    if NumPrice <= NumWeeklyLow and NumPrice > NumMovingAvearge:
        print('buy')
    elif NumPrice > NumWeeklyLow and NumPrice > NumMovingAvearge:
        if NumPrice - NumWeeklyLow <= NumPrice / 100:
            print('buy - caution')
        elif NumPrice - NumWeeklyLow > NumPrice / 100:
                print('hold')

    elif NumPrice >= NumWeeklyHigh:
        print('sell')
    else:
        print("Don't Buy")






