# -*- coding: utf-8 -*-
import os
import sys
import requests
import yaml
from bs4 import BeautifulSoup


class WebPage(object):
    def __init__(self, name=None, page=None, soup=None):
        self.name = name
        self.page = page
        self.soup = soup
        self.price = None

    def get_page_url(self):
        return

    def readResponseToSoup(self, data):
        self.soup = BeautifulSoup(data, "html.parser")

    def openSoup(self, filename):
        with open(filename, 'r') as soupFile:
            wbf = soupFile.read()
            self.soup = BeautifulSoup(wbf, "html.parser")

    def writeSoup(self, filename):
        with open(filename, 'w') as outFile:
            outFile.write(str(self.soup))

    def get_price(self):
        price_soup = self.soup.find_all('span', {'class': 'amount'})
        print price_soup
        self.price = str(price_soup[0])
        self.price = self.price[self.price.index('£')+2 : self.price.index('£')+6].split('<')[0]


def analyse_lotteries(lotteries):
    playable = []
    for lottery in lotteries:
        page = WebPage(name=lottery)
        page.readResponseToSoup(lotteries[lottery]['data'])
        page.get_price()
        print "Comparing {0} > {1}".format(page.price, lotteries[lottery]['jackpot'])
        if float(page.price) > lotteries[lottery]['jackpot']:
            string = "The {0} Lottery is above limit £{1}M with a jackpot of £{2}M".format(
                lottery, lotteries[lottery]['jackpot'], page.price
            )
            print "normal"
            print string
            print "utf8"
            print string.encode("utf8")
            playable.append(unicode("The {0} Lottery is above limit £{1}M with a jackpot of £{2}M".format(
                lottery, lotteries[lottery]['jackpot'], page.price
            )))
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
        print r.encoding
        r.encoding = 'utf8'
        return r.content
    else:
        print "[ERROR] Failed accessing lottery page:\n {0}".format(r.content)
    return 1


def run():
    config = load_config()
    lotteries = load_lotteries(config)
    if len(lotteries) > 0:
        playable = analyse_lotteries(lotteries)
        print playable
    else:
        print "No lotteries found"
        sys.exit(1)


if __name__ == "__main__":
    run()