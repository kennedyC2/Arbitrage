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
betking = "https://www.betking.com/sports/s/prematch/soccer"


# Functions
# =============================================================================================================

# Get Menu
def getMenu():

    # Object
    data = {}

    # Initiate Browser
    Browser.get(betking)

    # Activate Menu
    Browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

    # Wait
    time.sleep(5)

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, "html5lib")

    # Fetch Menu
    collection = soup.find_all('li', 'level-2')
    for div in collection:
        span = div.find('span', 'tree-label')
        title = span.get_text().strip()
        id = collection.index(div)
        data[title] = {}
        data[title]['location'] = id

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']

        if l > 0:
            # Click
            Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            d = soup.find_all('li', 'level-3')
            e = []
            for t in d:
                e.append(t.find('span').get_text().strip())
            data[each]['submenu'] = e

            # UnClick
            Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()
        else:
            pass

    # Save as JSON
    with open('./../Betking/betking_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# Sportybet Odds
# ======================================================================================

# Double and Single
def DS_Chance():
    # Odds
    s_odds = {}
    d_odds = {}

    # fetch links
    with open('./../Betking/betking_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(betking)

    # Activate Menu
    Browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

    for e in data:

        # Index
        l = data[e]['location']

        if l > 0:
            # Activate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()

            # Wait 10 seconds
            time.sleep(10)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('tr', 'trOddsSection')

            # Line
            olympics_1 = []
            olympics_2 = []

            for each in elem:
                # Compile
                info_1 = {}
                info_2 = {}
                match = each.find(
                    'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')
                matchTm = each.find(
                    'td', 'eventDate').get_text().strip()
                g_odds = each.find_all('div', 'oddBorder')
                info_1['match'] = match
                info_2['match'] = match
                info_1['time'] = matchTm
                info_2['time'] = matchTm
                info_1['home'] = g_odds[0].get_text().strip() or 0
                info_1['away'] = g_odds[2].get_text().strip() or 0
                info_2['1X'] = g_odds[3].get_text().strip() or 0
                info_2['2X'] = g_odds[5].get_text().strip() or 0

                # Upload
                olympics_1.append(info_1)
                olympics_2.append(info_2)
            s_odds[e] = olympics_1
            d_odds[e] = olympics_2

            # Deactivate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()
            Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

            # Wait 5 seconds
            time.sleep(5)
        else:
            pass

    with open('./../Betking/betking_Single.txt', 'w') as outfile:
        json.dump(s_odds, outfile, indent=4)

    with open('./../Betking/betking_Double.txt', 'w') as outfile:
        json.dump(d_odds, outfile, indent=4)
    Browser.quit()


# GGNG
def GGNG():
    # Odds
    odds = {}

    # fetch links
    with open('./../Betking/betking_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(betking)

    # Activate Menu
    Browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

    # Wait 5 seconds
    time.sleep(5)

    for e in data:

        # Index
        l = data[e]['location']

        if l > 0:
            # Activate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()

            # Wait 10 seconds
            time.sleep(10)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            ln = len(soup.find_all('div', 'eventContainer'))

            # Loop & Click
            for ch in range(ln):
                soup = BeautifulSoup(Browser.page_source, "html5lib")
                obj = soup.select('.eventContainer')[
                    ch].select('.regionAreaContainer > .area')
                for div in obj:
                    if div.find('div').get_text() == 'GG/NG':
                        GG_NG = Browser.find_element(By.CSS_SELECTOR,
                                                     '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                        Browser.execute_script("arguments[0].click();", GG_NG)
                        break

            # Wait 5 seconds
            time.sleep(5)

            # Re--
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('tr', 'trOddsSection')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                match = each.find(
                    'td', 'matchName')['data-matchname'].strip()
                matchTm = each.find(
                    'td', 'eventDate').get_text().strip()
                g_odds = each.find_all('div', 'oddBorder')
                info['match'] = match
                info['time'] = matchTm
                info['GG'] = g_odds[0].get_text().strip() or 0
                info['NG'] = g_odds[1].get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics

            # Deactivate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()
            Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

            # Wait 5 seconds
            time.sleep(5)
        else:
            pass

    with open('./../Betking/betking_GGNG.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# DNB
def DNB():
    # Odds
    odds = {}

    # fetch links
    with open('./../Betking/betking_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(betking)

    # Activate Menu
    Browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

    # Wait 5 seconds
    time.sleep(5)

    for e in data:

        # Index
        l = data[e]['location']

        if l > 0:
            # Activate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()

            # Wait 10 seconds
            time.sleep(10)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            ln = len(soup.find_all('div', 'eventContainer'))

            # Loop & Click
            for ch in range(ln):
                soup = BeautifulSoup(Browser.page_source, "html5lib")
                obj = soup.select('.eventContainer')[
                    ch].select('.regionAreaContainer > .area')
                for div in obj:
                    if div.find('div').get_text() == 'DNB':
                        DNB = Browser.find_element(By.CSS_SELECTOR,
                                                   '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                        Browser.execute_script("arguments[0].click();", DNB)
                        break

            # Wait 5 seconds
            time.sleep(5)

            # Re--
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('tr', 'trOddsSection')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                match = each.find(
                    'td', 'matchName')['data-matchname'].strip()
                matchTm = each.find(
                    'td', 'eventDate').get_text().strip()
                g_odds = each.find_all('div', 'oddBorder')
                info['match'] = match
                info['time'] = matchTm
                info['home'] = g_odds[0].get_text().strip() or 0
                info['away'] = g_odds[1].get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics

            # Deactivate Submenu
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()
            Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

            # Wait 5 seconds
            time.sleep(5)
        else:
            pass

    with open('./../Betking/betking_DNB.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# getMenu()
# DS_Chance()
# GGNG()
# DNB()
