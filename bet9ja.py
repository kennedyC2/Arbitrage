# Dependencies
# =============================================================================================================
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import re
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
bet9ja = "https://sports.bet9ja.com/"


# Functions
# =============================================================================================================


# Bet9ja Menu
def getMenu():

    # Object
    data = {}

    # Initialise Browser
    Browser.get(bet9ja)

    # Wait
    WebDriverWait(Browser, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'accordion-item')))

    # Activate Menu
    Browser.find_elements(By.CLASS_NAME, "accordion-item")[0].click()
    Browser.find_element(By.ID,
                         "left_prematch_sport-1_soccer_labelmore-toggle").click()

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, "html5lib")

    # Fetch Menu
    for div in soup.select(".accordion > .accordion-item")[0]:
        upper = div.select(".accordion-inner > .accordion-item")
        for div in upper:
            title = div.find("div", "accordion-text").get_text().strip()
            id = div.find("div", "accordion-toggle")['id']
            data[title] = {}
            data[title]['location'] = id

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']
        Browser.find_element(By.ID, l).click()

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        d = soup.find_all('a', 'side-nav-league__link')
        e = []
        for t in d:
            f = {}
            f['title'] = t['title']
            f['id'] = re.sub('[a-zA-Z_,]', '', t['id'])
            e.append(f)
        data[each]['submenu'] = e

    # Save as JSON
    with open('./Bet9ja/bet9ja_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# Bet9ja links
def getLinks_Bet9ja():
    # web prefix
    p = bet9ja + 'competition/soccer/'

    # link Object
    links = {}

    # fetch menu
    with open('./Bet9ja/bet9ja_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        for a in data[e]['submenu']:
            u = e.lower().replace(',', '').replace(' ', '') + '/'
            v = a['title'].lower().replace(',', '').replace(' ', '') + '/'
            w = a['id'].lower()[1:]

            # full link
            fl = p + u + v + w

            # Gather links
            links[a['title']] = fl

    # Save links
    with open('./Bet9ja/bet9ja_links.txt', 'w') as outfile:
        json.dump(links, outfile, indent=4)

    Browser.quit()


# Bet9ja Odds
# ======================================================================================

# DNB
def DNB():
    # Odds
    odds = {}

    # fetch links
    with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
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
        box = len(soup.find_all('td', 'grid-table__td'))
        for i in range(box):
            if soup.find_all('td', 'grid-table__td')[i].get_text().strip() == 'DNB':
                index = i
                break

        # Activate DNB
        if index > -1:
            Browser.find_elements(By.CLASS_NAME,
                                  'grid-table__td')[index].click()

            # Wait 5 seconds
            time.sleep(5)

            # Scroll the page
            height = int(Browser.execute_script(
                'return document.body.scrollHeight'))
            for i in range(1, height, 10):
                Browser.execute_script("window.scrollTo(0, {});".format(i))

            # Wait 5 seconds
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.select('.sports-table > .table-f')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                home_team = each.find(
                    'div', 'sports-table__home').get_text().strip()
                away_team = each.find(
                    'div', 'sports-table__away').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = each.find('span').get_text().strip()
                info['home'] = each.find_all(
                    'li', 'sports-table__odds-item')[0].get_text().strip() or 0
                info['away'] = each.find_all(
                    'li', 'sports-table__odds-item')[1].get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics
        else:
            pass
        continue

    with open('./Bet9ja/bet9ja_DNB.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# GGNG
def GGNG():
    # Odds
    odds = {}

    # fetch links
    with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
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
        box = len(soup.find_all('td', 'grid-table__td'))
        for i in range(box):
            if soup.find_all('td', 'grid-table__td')[i].get_text().strip() == 'GG/NG':
                index = i
                break

        # Activate GGNG
        if index > -1:
            Browser.find_elements(By.CLASS_NAME,
                                  'grid-table__td')[index].click()

            # Wait 5 seconds
            time.sleep(5)

            # Scroll the page
            height = int(Browser.execute_script(
                'return document.body.scrollHeight'))
            for i in range(1, height, 10):
                Browser.execute_script("window.scrollTo(0, {});".format(i))

            # Wait 5 seconds
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.select('.sports-table > .table-f')

            # Line
            olympics = []

            for each in elem:
                # Compile
                info = {}
                home_team = each.find(
                    'div', 'sports-table__home').get_text().strip()
                away_team = each.find(
                    'div', 'sports-table__away').get_text().strip()
                info['match'] = home_team + ' vs ' + away_team
                info['time'] = each.find('span').get_text().strip()
                info['GG'] = each.find_all(
                    'li', 'sports-table__odds-item')[0].get_text().strip() or 0
                info['NG'] = each.find_all(
                    'li', 'sports-table__odds-item')[1].get_text().strip() or 0

                # Upload
                olympics.append(info)
            odds[e] = olympics
        else:
            pass
        continue

    with open('./Bet9ja/bet9ja_GGNG.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# Double Chance and Single Chance
def DS_chance():
    # Odds
    s_odds = []
    d_odds = []

    # fetch links
    with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        # Initiate Browser
        Browser.get(data[e])

        # Wait 5 seconds
        time.sleep(5)

        # Scroll the page
        height = int(Browser.execute_script(
            'return document.body.scrollHeight'))
        for i in range(1, height, 10):
            Browser.execute_script("window.scrollTo(0, {});".format(i))

        # # Wait 5 seconds
        time.sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.select('.sports-table > .table-f')

        for each in elem:
            # Compile
            info_1 = {}
            info_2 = {}
            home_team = each.find(
                'div', 'sports-table__home').get_text().strip()
            away_team = each.find(
                'div', 'sports-table__away').get_text().strip()

            info_1['category'] = e
            info_2['category'] = e
            info_1['match'] = home_team + ' vs ' + away_team
            info_2['match'] = home_team + ' vs ' + away_team
            info_1['time'] = each.find('span').get_text().strip()
            info_2['time'] = each.find('span').get_text().strip()
            info_1['home'] = each.find_all(
                'li', 'sports-table__odds-item')[0].get_text().strip() or 0
            info_1['away'] = each.find_all(
                'li', 'sports-table__odds-item')[2].get_text().strip() or 0
            info_2['1X'] = each.find_all(
                'li', 'sports-table__odds-item')[3].get_text().strip() or 0
            info_2['2X'] = each.find_all(
                'li', 'sports-table__odds-item')[5].get_text().strip() or 0

            # Upload
            s_odds.append(info_1)
            d_odds.append(info_2)

    with open('./Bet9ja/bet9ja_Single.txt', 'w') as outfile:
        json.dump(s_odds, outfile, indent=4)

    with open('./Bet9ja/bet9ja_Double.txt', 'w') as outfile:
        json.dump(d_odds, outfile, indent=4)
    Browser.quit()


# getMenu()
# getLinks_Bet9ja()
DS_chance()
