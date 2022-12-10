# Dependencies
# =============================================================================================================
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
# import os
# from pathlib import Path

# Browser Configurations
# =============================================================================================================
BrowserMode = uc.ChromeOptions()
BrowserMode.headless = False
BrowserMode.add_argument('--user-data-dir=./chrome_profile/')
BrowserMode.add_argument("--start-maximized")
Browser = uc.Chrome(options=BrowserMode)
actions = ActionChains(Browser)

# Websites
# =============================================================================================================
sportybet = "https://www.sportybet.com/ng/sport/football"


# Functions
# =============================================================================================================

# Get Menu
def getMenu():

    # Object
    data = {}

    # Initiate Browser
    Browser.get(sportybet)

    # Wait
    time.sleep(5)

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, "html5lib")

    # Fetch Menu
    collection = soup.select(
        ".sport-list > .category-list-item > .category-item")
    for div in collection:
        span = div.find_all('span')[0]
        title = span.get_text().strip()
        id = collection.index(div)
        data[title] = {}
        data[title]['location'] = id

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        d = soup.select(
            ".sport-list > .category-list-item > .tournament-list > ul")[l]
        e = []
        for t in d.find_all('span', 'tournament-name'):
            e.append(t.get_text().strip())
        data[each]['submenu'] = e

    # Save as JSON
    with open('./Sportybet/sportybet_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# Sportybet Odds
# ======================================================================================

# Single
def Single():
    # Odds
    odds = []

    # fetch links
    with open('./Sportybet/sportybet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(sportybet)

    for e in data:

        # Index
        l = data[e]['location']

        # Menu
        item = Browser.find_element(By.XPATH,
                                    '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']')

        # Extend submenu
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select('#sportList > div.game-list > ul.sport-list > li:nth-child(' +
                             str(l + 1) + ') > div.tournament-list > ul > li'))

        # loop and click
        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # Click
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(10)

        # Activate Single
        for j in range(ln):
            Browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[' + str(2 + j) + ']/div/div[3]/div[1]').click()
        # Wait 5 seconds
        time.sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for each in elem:
            # Compile
            category = each.find('span', 'text').get_text().strip()
            div = each.find_all('div', 'm-content-row')

            for cc in div:
                info = {}
                info['category'] = category
                home_team = cc.find(
                    'div', 'home-team').get_text().strip()
                away_team = cc.find(
                    'div', 'away-team').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = cc.find(
                    'div', 'clock-time').get_text().replace('&nbsp;', '').strip()
                info['home'] = cc.find_all(
                    'span', 'm-outcome-odds')[0].get_text().strip() or 0
                info['away'] = cc.find_all(
                    'span', 'm-outcome-odds')[2].get_text().strip() or 0

                # Upload
                odds.append(info)

        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # UnClick
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(10)

    with open('./Sportybet/sportybet_Single.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# Double
def Double():
    # Odds
    odds = []

    # fetch links
    with open('./Sportybet/sportybet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(sportybet)

    for e in data:

        # Index
        l = data[e]['location']

        # Menu
        item = Browser.find_element(By.XPATH,
                                    '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']')

        # Extend submenu
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select('#sportList > div.game-list > ul.sport-list > li:nth-child(' +
                             str(l + 1) + ') > div.tournament-list > ul > li'))

        # loop and click
        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # Click
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(15)

        # Activate Double
        for j in range(ln):
            Browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[' + str(2 + j) + ']/div/div[3]/div[2]').click()

        # Wait 5 seconds
        time.sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for each in elem:
            # Compile
            category = each.find('span', 'text').get_text().strip()
            div = each.find_all('div', 'm-content-row')

            for cc in div:
                info = {}
                info['category'] = category
                home_team = cc.find(
                    'div', 'home-team').get_text().strip()
                away_team = cc.find(
                    'div', 'away-team').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = cc.find(
                    'div', 'clock-time').get_text().replace('&nbsp;', '').strip()

                if not(cc.find_all('div', 'm-outcome--disabled')):
                    info['1X'] = cc.find_all(
                        'span', 'm-outcome-odds')[0].get_text().strip() or 0
                    info['2X'] = cc.find_all(
                        'span', 'm-outcome-odds')[2].get_text().strip() or 0
                else:
                    if cc.select('.m-market > div')[0]['class'].index('m-outcome--disabled') > -1:
                        info['1X'] = 0
                    else:
                        info['1X'] = cc.find_all(
                            'span', 'm-outcome-odds')[0].get_text().strip() or 0

                    if cc.select('.m-market > div')[2]['class'].index('m-outcome--disabled') > -1:
                        info['2X'] = 0
                    else:
                        info['2X'] = cc.find_all(
                            'span', 'm-outcome-odds')[2].get_text().strip() or 0

                # Upload
                odds.append(info)

        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # UnClick
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(10)

    with open('./Sportybet/sportybet_Double.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# GGNG
def GGNG():
    # Odds
    odds = []

    # fetch links
    with open('./Sportybet/sportybet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(sportybet)

    for e in data:

        # Index
        l = data[e]['location']

        # Menu
        item = Browser.find_element(By.XPATH,
                                    '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']')

        # Extend submenu
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select('#sportList > div.game-list > ul.sport-list > li:nth-child(' +
                             str(l + 1) + ') > div.tournament-list > ul > li'))

        # loop and click
        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # Click
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(15)

        # Activate GGNG
        for j in range(ln):
            Browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[' + str(2 + j) + ']/div/div[3]/div[3]').click()

        # Wait 5 seconds
        time.sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for each in elem:
            # Compile
            category = each.find('span', 'text').get_text().strip()
            div = each.find_all('div', 'm-content-row')

            for cc in div:
                info = {}
                info['category'] = category
                home_team = cc.find(
                    'div', 'home-team').get_text().strip()
                away_team = cc.find(
                    'div', 'away-team').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = cc.find(
                    'div', 'clock-time').get_text().replace('&nbsp;', '').strip()

                if not(cc.find_all('div', 'm-outcome--disabled')):
                    info['GG'] = cc.find_all(
                        'span', 'm-outcome-odds')[0].get_text().strip() or 0
                    info['NG'] = cc.find_all(
                        'span', 'm-outcome-odds')[1].get_text().strip() or 0
                else:
                    if cc.select('.m-market > div')[0]['class'].index('m-outcome--disabled') > -1:
                        info['GG'] = 0
                    else:
                        info['GG'] = cc.find_all(
                            'span', 'm-outcome-odds')[0].get_text().strip() or 0

                    if cc.select('.m-market > div')[1]['class'].index('m-outcome--disabled') > -1:
                        info['NG'] = 0
                    else:
                        info['NG'] = cc.find_all(
                            'span', 'm-outcome-odds')[1].get_text().strip() or 0

                # Upload
                odds.append(info)

        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # UnClick
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(10)

    with open('./Sportybet/sportybet_GGNG.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# DNB
def DNB():
    # Odds
    odds = []

    # fetch links
    with open('./Sportybet/sportybet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(sportybet)

    for e in data:

        # Index
        l = data[e]['location']

        # Menu
        item = Browser.find_element(By.XPATH,
                                    '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']')

        # Extend submenu
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select('#sportList > div.game-list > ul.sport-list > li:nth-child(' +
                             str(l + 1) + ') > div.tournament-list > ul > li'))

        # loop and click
        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # Click
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(15)

        # Activate Draw No Bet
        for j in range(ln):
            Browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[' + str(2 + j) + ']/div/div[3]/div[4]').click()

        # Wait 5 seconds
        time.sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for each in elem:
            # Compile
            category = each.find('span', 'text').get_text().strip()
            div = each.find_all('div', 'm-content-row')

            for cc in div:
                info = {}
                info['category'] = category
                home_team = cc.find(
                    'div', 'home-team').get_text().strip()
                away_team = cc.find(
                    'div', 'away-team').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = cc.find(
                    'div', 'clock-time').get_text().replace('&nbsp;', '').strip()

                if not(cc.find_all('div', 'm-outcome--disabled')):
                    info['home'] = cc.find_all(
                        'span', 'm-outcome-odds')[0].get_text().strip() or 0
                    info['away'] = cc.find_all(
                        'span', 'm-outcome-odds')[1].get_text().strip() or 0
                else:
                    if cc.select('.m-market > div')[0]['class'].index('m-outcome--disabled') > -1:
                        info['home'] = 0
                    else:
                        info['home'] = cc.find_all(
                            'span', 'm-outcome-odds')[0].get_text().strip() or 0

                    if cc.select('.m-market > div')[1]['class'].index('m-outcome--disabled') > -1:
                        info['away'] = 0
                    else:
                        info['away'] = cc.find_all(
                            'span', 'm-outcome-odds')[1].get_text().strip() or 0

                # Upload
                odds.append(info)

        actions.move_to_element(item).perform()
        for z in range(1, ln + 1):
            # UnClick
            d1 = Browser.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div[2]/div/div[1]/div/div/div[4]/ul[2]/li[' + str(l + 1) + ']/div[2]/ul/li[' + str(z) + ']')
            Browser.execute_script("arguments[0].click();", d1)

        # Wait 10 seconds
        time.sleep(10)

    with open('./Sportybet/sportybet_DNB.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


Single()
# getMenu()
# Double()
# GGNG()
# DNB()
