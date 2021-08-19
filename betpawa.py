# Dependencies
# =============================================================================================================
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import os
from pathlib import Path

# Browser Configurations
# =============================================================================================================

# Create empty profile
os.mkdir('./chrome_profile')
Path('./chrome_profile/First Run').touch()

# Continue
BrowserMode = uc.ChromeOptions()
BrowserMode.headless = False
BrowserMode.add_argument("--start-maximized")
Browser = uc.Chrome(options=BrowserMode)
actions = ActionChains(Browser)

# Websites
# =============================================================================================================
betPawa = "https://www.betpawa.ng"


# Functions
# =============================================================================================================

# Get Menu
def getMenu():

    # Object
    data = {}

    # Initiate Browser
    Browser.get(betPawa)

    # Wait
    time.sleep(5)

    # Activate Menu
    Browser.find_element(By.CLASS_NAME, 'last').click()

    # Wait
    time.sleep(5)

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, 'html5lib')

    # Fetch Menu
    menu = soup.select('.tournaments > .menu-item')

    # loop
    for li in menu:
        a = li.find('a', 'menu-link')
        data[a.get_text()] = {}
        data[a.get_text()]['link'] = a['href']

    # Save as JSON
    with open('./../Betpawa/betpawa_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# BetPawa links
def getLinks():

    # link Object
    links = {}

    # fetch menu
    with open('./../Betpawa/betpawa_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        a = data[e]['link']

        # full link
        fl = betPawa + a

        # Gather links
        links[e] = fl

    # Save links
    with open('./../Betpawa/betpawa_links.txt', 'w') as outfile:
        json.dump(links, outfile, indent=4)

    Browser.quit()


# BetPawa Odds
# ======================================================================================

# Single
def Single():
    # Odds
    odds = {}

    # fetch links
    with open('./../Betpawa/betpawa_links.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        # Initiate Browser
        Browser.get(data[e])

        # Wait 5 seconds
        time.sleep(5)

        # Index of target
        index = -1

        # Get index
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        box = len(soup.find_all('li', 'tabs-selector'))
        for i in range(box):
            if soup.find_all('li', 'tabs-selector')[i].get_text().strip() == '1X2':
                index = i
                break

        # Activate DNB
        if index > -1:
            Browser.find_element(By.CLASS_NAME,
                                 'tabs-selector')[index].click()

            # Wait 5 seconds
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('div', 'events-container')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                home_team = each.find_all(
                    'p', 'team')[0].get_text().strip()
                away_team = each.find_all(
                    'p', 'team')[1].get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = each.find('div', 'times').get_text().strip()
                info['home'] = each.find_all(
                    'span', 'event-bet')[0].find('span', 'event-odds').get_text().strip() or 0
                info['away'] = each.find_all(
                    'span', 'event-bet')[2].find('span', 'event-odds').get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics
        else:
            pass
        continue

    with open('./../Betpawa/betpawa_Single.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# Double
def Double():
    # Odds
    odds = {}

    # fetch links
    with open('./../Betpawa/betpawa_links.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        # Initiate Browser
        Browser.get(data[e])

        # Wait 5 seconds
        time.sleep(5)

        # Index of target
        index = -1

        # Get index
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        box = len(soup.find_all('li', 'tabs-selector'))
        for i in range(box):
            if soup.find_all('li', 'tabs-selector')[i].get_text().strip() == 'DC':
                index = i
                break

        # Activate DNB
        if index > -1:
            Browser.find_element(By.CLASS_NAME,
                                 'tabs-selector')[index].click()

            # Wait 5 seconds
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('div', 'events-container')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                home_team = each.find_all(
                    'p', 'team')[0].get_text().strip()
                away_team = each.find_all(
                    'p', 'team')[1].get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = each.find('div', 'times').get_text().strip()
                info['1X'] = each.find_all(
                    'span', 'event-bet')[0].find('span', 'event-odds').get_text().strip() or 0
                info['2X'] = each.find_all(
                    'span', 'event-bet')[1].find('span', 'event-odds').get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics
        else:
            pass
        continue

    with open('./../Betpawa/betpawa_Double.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# GG/NG
def GGNG():
    # Odds
    odds = {}

    # fetch links
    with open('./../Betpawa/betpawa_links.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        # Initiate Browser
        Browser.get(data[e])

        # Wait 5 seconds
        time.sleep(5)

        # Index of target
        index = -1

        # Get index
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        box = len(soup.find_all('li', 'tabs-selector'))
        for i in range(box):
            if soup.find_all('li', 'tabs-selector')[i].get_text().strip() == 'BTTS':
                index = i
                break

        # Activate DNB
        if index > -1:
            Browser.find_element(By.CLASS_NAME,
                                 'tabs-selector')[index].click()

            # Wait 5 seconds
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('div', 'events-container')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                home_team = each.find_all(
                    'p', 'team')[0].get_text().strip()
                away_team = each.find_all(
                    'p', 'team')[1].get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = each.find('div', 'times').get_text().strip()
                info['GG'] = each.find_all(
                    'span', 'event-bet')[0].find('span', 'event-odds').get_text().strip() or 0
                info['NG'] = each.find_all(
                    'span', 'event-bet')[1].find('span', 'event-odds').get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics
        else:
            pass
        continue

    with open('./../Betpawa/betpawa_GGNG.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()
