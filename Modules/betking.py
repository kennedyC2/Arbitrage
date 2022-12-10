# Dependencies
# =============================================================================================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

# Browser Configurations
# =============================================================================================================
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.page_load_strategy = "eager"
service = Service(
    executable_path="C:\Software Development\Arbitrage\chromedriver.exe")
Browser = webdriver.Chrome(service=service, options=options)
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

    # Wait
    WebDriverWait(Browser, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a')))

    # Activate Menu
    Browser.find_element(
        By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a').click()

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
        l = data[each]['location'] + 2

        if l > 0:
            # Click
            Browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l) + ') > a').click()

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            d = soup.find_all('li', 'level-3')
            e = []
            for t in d:
                e.append(t.find('span').get_text().strip())
            data[each]['submenu'] = e

            # UnClick
            Browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l) + ') > a').click()
        else:
            pass

    # Save as JSON
    with open('./Betking/betking_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# ==================================================================
#      Single Chance, Handicap
# ==================================================================

def SH_Chance(fetchAll=False, category=None):
    # Odds
    odds = {}

    # fetch links
    with open('./Betking/betking_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(betking)

    # Wait
    WebDriverWait(Browser, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a')))

    # Activate Menu
    Browser.find_element(
        By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a').click()

    if fetchAll:
        for e in data:
            # Index
            l = data[e]['location']

            if l > 2:
                # Initiate Collection
                odds[e] = {}

                # Activate Submenu
                Browser.find_element(
                    By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()

                # Wait 10 seconds
                time.sleep(10)

                # Parse HtmlDoc
                soup = BeautifulSoup(Browser.page_source, "html5lib")
                ln = soup.find_all('div', 'eventContainer')

                # Loop & Fetch Single Odds
                for ch in range(len(ln)):
                    # Container
                    file = {}

                    elem = soup.find_all('tr', 'trOddsSection')

                    for each in elem:
                        # Define Data
                        _data = {}

                        # Compile
                        match = each.find(
                            'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')
                        file[match] = {}

                        file[match]["time"] = each.find(
                            'td', 'eventDate').get_text().strip()

                        # Home Win, Draw and Away Win Odds
                        g_odds = each.find_all('div', 'oddBorder')

                        _data['home'] = g_odds[0].get_text().strip() or 0

                        _data['draw'] = g_odds[1].get_text().strip() or 0

                        _data['away'] = g_odds[2].get_text().strip() or 0

                        # Upload
                        file[match]["single"] = _data
                        odds[e][data[e]["submenu"][ch]] = file

                # Loop & Fetch Handicap Odds
                for ch in range(len(ln)):
                    # Container
                    file = {}

                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    obj = soup.select(
                        '.eventContainer')[ch].select('.regionAreaContainer > .area')
                    for div in obj:
                        if div.find('div').get_text() == 'Handicap':
                            Handicap = Browser.find_element(
                                By.CSS_SELECTOR, '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                            Browser.execute_script(
                                "arguments[0].click();", Handicap)

                            # Wait 5 seconds
                            time.sleep(5)

                            # Refresh
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")
                            elem = soup.find_all("table", "oddsTable")[
                                ch].find_all('tr', 'trOddsSection')

                            for each in elem:
                                _data = {}

                                match = each.find(
                                    'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')

                                g_odds = each.find_all('div', 'multilineType')

                                # loop
                                for multi in g_odds:
                                    if multi.find("span").get_text().strip() == "1 (0 : 1)":
                                        _data['1 [Away + 1]'] = multi.find(
                                            "div", "oddBorder").get_text().strip()
                                        break

                                    # Default to zero
                                    _data['1 [Away + 1]'] = "0.00"

                                for multi in g_odds:
                                    if multi.find("span").get_text().strip() == "2 (1 : 0)":
                                        _data['2 [Home + 1]'] = multi.find(
                                            "div", "oddBorder").get_text().strip()
                                        break

                                    # Default to zero
                                    _data['2 [Home + 1]'] = "0.00"

                                # Upload
                                odds[e][data[e]["submenu"][ch]
                                        ][match]["handicap"] = _data
                            break
                        continue

                # Deactivate Submenu
                Browser.find_element(
                    By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()
                Browser.find_element(
                    By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a').click()

                # Wait 5 seconds
                time.sleep(5)
            continue
    else:
        # Index
        l = data[category]['location']

        if l > 2:
            # Initiate Collection
            odds[category] = {}

            # Activate Submenu
            Browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()

            # Wait 10 seconds
            time.sleep(10)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            ln = soup.find_all('div', 'eventContainer')

            # Loop & Fetch Single Odds
            for ch in range(len(ln)):
                # Container
                file = {}

                elem = soup.find_all("table", "oddsTable")[
                    ch].find_all('tr', 'trOddsSection')

                for each in elem:
                    # Define Data
                    _data = {}

                    # Compile
                    match = each.find(
                        'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')
                    file[match] = {}

                    file[match]["time"] = each.find(
                        'td', 'eventDate').get_text().strip()

                    # Home Win, Draw and Away Win Odds
                    g_odds = each.find_all('div', 'oddBorder')

                    _data['home'] = g_odds[0].get_text().strip() or 0

                    _data['draw'] = g_odds[1].get_text().strip() or 0

                    _data['away'] = g_odds[2].get_text().strip() or 0

                    # Upload
                    file[match]["single"] = _data

                odds[category][data[category]["submenu"][ch]] = file

            # Loop & Fetch Handicap Odds
            for ch in range(len(ln)):
                # Container
                file = {}

                soup = BeautifulSoup(Browser.page_source, "html5lib")
                obj = soup.select(
                    '.eventContainer')[ch].select('.regionAreaContainer > .area')
                for div in obj:
                    if div.find('div').get_text() == 'Handicap':
                        Handicap = Browser.find_element(
                            By.CSS_SELECTOR, '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                        Browser.execute_script(
                            "arguments[0].click();", Handicap)

                        # Wait 5 seconds
                        time.sleep(5)

                        # Refresh
                        soup = BeautifulSoup(Browser.page_source, "html5lib")
                        elem = soup.find_all("table", "oddsTable")[
                            ch].find_all('tr', 'trOddsSection')

                        for each in elem:
                            _data = {}

                            match = each.find(
                                'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')

                            g_odds = each.find_all('div', 'multilineType')

                            # loop
                            for multi in g_odds:
                                if multi.find("span").get_text().strip() == "1 (0 : 1)":
                                    _data['1 [Away + 1]'] = multi.find(
                                        "div", "oddBorder").get_text().strip()
                                    break

                                # Default to zero
                                _data['1 [Away + 1]'] = "0.00"

                            for multi in g_odds:
                                if multi.find("span").get_text().strip() == "2 (1 : 0)":
                                    _data['2 [Home + 1]'] = multi.find(
                                        "div", "oddBorder").get_text().strip()
                                    break

                                # Default to zero
                                _data['2 [Home + 1]'] = "0.00"

                            # Upload
                            odds[category][data[category]["submenu"]
                                           [ch]][match]["handicap"] = _data
                        break
                    continue

            # Wait 5 seconds
            time.sleep(5)

    with open('./Betking/data.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# getMenu()
SH_Chance(category="Spain")
