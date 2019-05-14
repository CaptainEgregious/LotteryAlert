# -*- coding: utf-8 -*-
import os
import sys
import requests
import yaml
from bs4 import BeautifulSoup
import re


class WebPage(object):
    def __init__(self, name=None, page=None, soup=None):
        self.name = name
        self.page = page
        self.soup = soup
        self.price = None

    def get_page_url(self):
        return

    def read_response_to_soup(self, data):
        self.soup = BeautifulSoup(data, "html.parser")

    def get_price(self):
        price_soup = self.soup.find_all('span', {'class': 'amount'})
        self.price = str(price_soup[0])
        priceMatch = re.compile(r'(\d)+(\.)*(\d)*')
        mo = priceMatch.search(self.price)
        print("[INFO]: Analysing {0}".format(self.price))
        if mo is not None:
            try:
                print("[INFO]: mo.group()")
                print(mo.group())
            except Exception as e:
                print("[ERROR]: {0} \n Price: {1}".format(e, self.price))
            self.price = mo.group()
            print("Price is:\n £{0}".format(self.price))
        else:
            print("No price match found")


def analyse_lotteries(lotteries):
    playable = []
    for lottery in lotteries:
        page = WebPage(name=lottery)
        page.read_response_to_soup(lotteries[lottery]['data'])
        page.get_price()
        print("Comparing {0} > {1}".format(page.price, lotteries[lottery]['jackpot']))
        if float(page.price) > lotteries[lottery]['jackpot']:
            playable.append("The {0} Lottery is above limit £{1}M with a jackpot of £{2}M".format(
                lottery, lotteries[lottery]['jackpot'], page.price
            ))
    return playable


def load_config():
    with open("lottery.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_lotteries(config):
    lotteries = {}
    for lottery in config['lotteries']:
        lotteries[lottery] = {}
        lotteries[lottery]['jackpot'] = config['lotteries'][lottery]['jackpot']
        lotteries[lottery]['data'] = load_lottery(config['lotteries'][lottery])
    return lotteries


def load_lottery(lottery):
    r = requests.get(lottery['url'])
    if r.status_code < 300:
        print(r.encoding)
        r.encoding = 'utf8'
        return r.content
    else:
        print("[ERROR] Failed accessing lottery page:\n {0}".format(r.content))
    return 1


def push_results(playable, config):
    url = 'https://api.pushed.co/1/push'
    for msg in playable:
        payload = {
            "app_key": config['pushed']['app_key'],
            "app_secret": config['pushed']['app_secret'],
            "target_type": "channel",
            "target_alias": config['pushed']['target_alias'],
            "content": msg
        }
        r = requests.post(url=url, data=payload)
        print(r.text)


def run():
    config = load_config()
    lotteries = load_lotteries(config)
    if len(lotteries) > 0:
        playable = analyse_lotteries(lotteries)
        # print(playable)
        # push_results(playable=playable, config=config)
    else:
        print("No lotteries found")
        sys.exit(1)


def lambda_handler():
    run()


if __name__ == "__main__":
    run()
