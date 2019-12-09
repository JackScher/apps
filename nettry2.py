import requests
from bs4 import BeautifulSoup as bs
import sys
import mysql.connector
from datetime import datetime


#url = 'https://sinoptik.ua/погода-запорожье'
url = 'https://sinoptik.ua/погода-'
city = input("Input city:...")
#date = input("Input date in format: 2019-07-03...")
url += city.lower()# + '/' + date
#print(url)
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.72'}


#=======================================================================================================================================================================================================================================


def db(mas):
    mdb = mysql.connector.connect(host='localhost',
                          user='root',
                          password='1234',
                          database='new_database')
    mcursor = mdb.cursor()
    sql = "INSERT INTO sinoptic (city, day, date, temperature) VALUES (%s, %s, %s, %s)"
    mcursor.execute(sql, mas)
    mdb.commit()
    print("Dates added!")


def sinoptic(url, headers):
    data = []
    session = requests.Session()
    request = session.get(url, headers=headers)
    try:
        soup = bs(request.content, 'html.parser')
        rez = soup.find_all('div', attrs={'id': 'bd1'})
        #print(rez)
        for line in rez:
            day = line.find('p', attrs={'class': 'day-link'}).text
            date = line.find('p', attrs={'class': 'date dateFree'}).text
            month = line.find('p', attrs={'class': 'month'}).text
            min_t = line.find('div', attrs={'class': 'min'}).text
            max_t = line.find('div', attrs={'class': 'max'}).text
            data.append({'День: ': day,
                        'Дата: ': str(date) + ' ' + str(month),
                         'Температура: ': min_t + ' ' + max_t})
        return data
    except Exception:
        print("ERROR")
        print(sys.exc_info())


def vard(mas):
    day = mas[0]['День: ']
    return day


def vardt(mas):
    date = mas[0]['Дата: ']
    return date


def vartm(mas):
    temp = mas[0]['Температура: ']
    return temp


#=======================================================================================================================================================================================================================================


mas1 =[]
mas1.append(city)
mas = sinoptic(url, headers)
day = vard(mas)
mas1.append(day)
dt = vardt(mas)
mas1.append(dt)
tm = vartm(mas)
mas1.append(tm)
print(mas1)

db(mas1)