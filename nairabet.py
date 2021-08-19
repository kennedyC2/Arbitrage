# Dependencies
# =============================================================================================================
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
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
BrowserMode = Options()
BrowserMode.headless = False
BrowserMode.add_argument("start-maximized")
Browser = Chrome(options=BrowserMode,
                 executable_path=r"/usr/local/bin/chromedriver")

# Websites
# =============================================================================================================
nairabet = "https://www.nairabet.com/"


# Nairabet Menu
def getMenu():

    # Object
    data = {}

    # Initialise Browser
    Browser.get(nairabet)

    # Wait 5 seconds
    time.sleep(5)

    # Activate Menu
    Browser.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/partial[1]/div/ul/li[1]').click()

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, "html5lib")

    # Fetch Menu
    collection = soup.select('.dropdown-submenu > .dropdown-menu-item')
    for li in collection:
        title = li.find('span', 'title').get_text().strip()
        id = collection.index(li)
        data[title] = {}
        data[title]['location'] = id

    # print(data)

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']
        Browser.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/partial[1]/div/ul/li[1]/ul/li[' + str(l + 1) + ']').click()

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        d = soup.select(
            '.left-menu > ul > li.StyledDropdownMenu__DropdownMenuItem-gYSekk.eVnYmE.is-active.has-submenu.dropdown-menu-item > ul > li:nth-child(' + str(l + 1) + ') > ul > li')

        e = []
        for t in d:
            e.append(t.find('span', 'title').get_text())

        data[each]['submenu'] = e

    # Save as JSON
    with open('./../Nairabet/nairabet_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# Nairabet Odds
# ======================================================================================


# Double Chance and Single Chance
def DS_chance():
    # Odds
    s_odds = {}
    d_odds = {}

    # fetch links
    with open('./../Nairabet/nairabet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(nairabet)

    # Wait 5 seconds
    time.sleep(5)

    # Activate Menu
    Browser.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/partial[1]/div/ul/li[1]').click()

    for e in data:
        # location
        l = data[e]['location']

        # Locate Element
        Browser.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/partial[1]/div/ul/li[1]/ul/li[' + str(l + 1) + ']').click()

        # item length
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select(
            '.left-menu > ul > li.StyledDropdownMenu__DropdownMenuItem-gYSekk.eVnYmE.is-active.has-submenu.dropdown-menu-item > ul > li:nth-child(' + str(l + 1) + ') > ul > li'))

        # Loop
        for i in range(1, ln + 1):
            if data[e]['submenu'][i - 1] != 'Outrights':
                # Click Target
                Browser.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/partial[1]/div/ul/li[1]/ul/li[' + str(l + 1) + ']/ul/li[' + str(i) + ']').click()

                # Wait 3 seconds
                time.sleep(5)

                # Parse HtmlDoc
                soup = BeautifulSoup(Browser.page_source, "html5lib")
                elem = soup.find_all('li', 'eventListPeriodItemPartial')

                # Line
                olympics_1 = []
                olympics_2 = []

                for each in elem:
                    # Compile
                    info_1 = {}
                    info_2 = {}
                    team = each.find(
                        'span', 'event-name').get_text().replace('-', 'vs')
                    info_1['match'] = team
                    info_2['match'] = team
                    info_1['time'] = each.find(
                        'span', 'time').get_text().strip()
                    info_2['time'] = each.find(
                        'span', 'time').get_text().strip()

                    if not(each.select('.hide-column-0 > .goto-event')):
                        info_1['home'] = each.select(
                            '.hide-column-0 > .game > button')[0].get_text().strip() or 0
                        info_1['away'] = each.select(
                            '.hide-column-0 > .game > button')[2].get_text().strip() or 0

                    if not(each.select('.hide-column-1 > .goto-event')):
                        info_2['1X'] = each.select(
                            '.hide-column-1 > .game > button')[0].get_text().strip() or 0
                        info_2['2X'] = each.select(
                            '.hide-column-1 > .game > button')[2].get_text().strip() or 0

                    # Upload
                    olympics_1.append(info_1)
                    olympics_2.append(info_2)
                s_odds[e] = olympics_1
                d_odds[e] = olympics_2
            else:
                continue

    with open('./../Nairabet/nairabet_Single.txt', 'w') as outfile:
        json.dump(s_odds, outfile, indent=4)

    with open('./../Nairabet/nairabet_Double.txt', 'w') as outfile:
        json.dump(d_odds, outfile, indent=4)
    Browser.quit()
