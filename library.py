from twilio.rest import Client
import requests
from bs4 import BeautifulSoup as soup
from random import choice
from time import sleep
import pandas as pd
from selenium import webdriver


def send_telegram(token, chat_id, msg):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=html'
    requests.get(url)


def send_whatsapp(msg, to_number):
    account_sid = 'AC7cdfca43c5f8cb4a21201224954179c7'
    auth_token = '3d9d17512d436bcff97baa8eab20a5b0'
    client = Client(account_sid, auth_token)

    client.messages.create(
        from_='whatsapp:+14155238886',
        body=msg,
        to='whatsapp:+{}'.format(to_number)
    )


def get_proxy():
    url = 'https://sslproxies.org/'
    response = requests.get(url)
    page_soup = soup(response.content, "html.parser")
    td = page_soup.find('table', {'id': 'proxylisttable'}).findAll('td')
    return {'https': choice(list(
        map(lambda x: x[0] + ':' + x[1], list(zip(map(lambda x: x.text, td[::8]), map(lambda x: x.text, td[1::8]))))))}


def get_historical_data(driver, ticker, download_path, freq):
    url = f"https://in.finance.yahoo.com/quote/{ticker}.NS/history?p={ticker}.NS"
    driver.driver.get(url)
    sleep(4)
    driver.driver.find_elements_by_xpath("//div[@data-test='dropdown']")[1].click()
    driver.driver.find_element_by_xpath("//span[text()='Max']").click()
    if freq == 'w':  # weekly data
        driver.driver.find_element_by_xpath("//span[text()='Daily']").click()
        driver.driver.find_element_by_xpath("//span[text()='Weekly']").click()
    if freq == 'm':  # monthly data
        driver.driver.find_element_by_xpath("//span[text()='Daily']").click()
        driver.driver.find_element_by_xpath("//span[text()='Monthly']").click()
    driver.driver.find_element_by_xpath("//span[text()='Apply']").click()
    driver.driver.find_element_by_xpath("//span[text()='Download']").click()
    sleep(2)
    return pd.read_csv(f'{download_path}/{ticker}.NS.csv', index_col=0)


class Driver:
    """
    path: Web driver path, eg: Chrome, Firefox
    options: list of web driver options
    This creates a webdriver object with options.
    """

    def __init__(self, path, options=()):
        self.path = path
        self.options = options
        self.driver_options = webdriver.ChromeOptions()
        for option in self.options:
            self.driver_options.add_argument(option)
        self.driver = webdriver.Chrome(executable_path=path, options=self.driver_options)
