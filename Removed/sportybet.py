# Dependencies
# =============================================================================================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import json
import re

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
    WebDriverWait(Browser, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'match-league-wrap')))

    # Wait
    sleep(5)

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
def SH_Chance(fetchAll=False, category=False):
    global odds
    global catgy

    # fetch links
    with open('./Sportybet/sportybet_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    if (fetchAll):
        # Variables
        odds = {}

        # Initiate Browser
        Browser.get(sportybet)

        # Wait
        WebDriverWait(Browser, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'import-match')))

        for e in data:
            # Index
            l = data[e]['location']

            # Initiate Collection
            odds[e] = {}

            # Menu
            item = Browser.find_element(
                By.CSS_SELECTOR, '.sport-list .category-list-item')[l + 1]

            # Extend submenu
            soup = BeautifulSoup(Browser.page_source, 'html5lib')
            ln = len(soup.select(
                '#sportList > div.game-list > ul.sport-list > li:nth-child(' + str(l + 1) + ') > div.tournament-list > ul > li'))

            # loop and click
            actions.move_to_element(item).perform()
            for z in range(ln):
                # Click
                d1 = Browser.find_element(By.CSS_SELECTOR, '#sportList > div.game-list > ul.sport-list > li:nth-child(' + str(
                    l + 1) + ') > div.tournament-list > ul > li')[str(z)]
                Browser.execute_script("arguments[0].click();", d1)

                sleep(2)

            # Activate Single
            for j in range(ln):
                Browser.find_element(By.CSS_SELECTOR, '#importMatch > div:nth-child(' + str(
                    2 + j) + ') > div > div.market-group.clearfix > div.market-item').click()

            # Wait 5 seconds
            sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('div', 'match-league')

            for each in elem:
                # Container
                file = {}

                # Compile
                catgy = each.find(
                    'span', 'text').get_text().replace(e, "").strip()
                div = each.find_all('div', 'm-content-row')

                for cc in div:
                    # Define Data
                    _data = {}

                    # Compile Names
                    home_team = cc.find(
                        'div', 'home-team').get_text().strip()
                    away_team = cc.find(
                        'div', 'away-team').get_text().strip()

                    file[home_team + ' vs ' + away_team] = {}

                    file[home_team + ' vs ' + away_team]['time'] = cc.find(
                        'div', 'clock-time').get_text().replace('&nbsp;', '').strip()

                    # Home Win, Draw and Away Win Odds
                    _data['home'] = cc.find_all(
                        'span', 'm-outcome-odds')[0].get_text().strip() or 0
                    _data['draw'] = cc.find_all(
                        'span', 'm-outcome-odds')[1].get_text().strip() or 0
                    _data['away'] = cc.find_all(
                        'span', 'm-outcome-odds')[2].get_text().strip() or 0

                    # Upload
                    file[home_team + ' vs ' + away_team]["single"] = _data

            # Wait 3 seconds
            sleep(3)

            # Activate Handicap
            for j in range(ln):
                # Click
                Browser.execute_script(
                    """
                        document.querySelectorAll("div#importMatch div.market-group.clearfix > div.market-item.m-select-market")[ """ + str(j) + """].classList.add("show-item")
                    """
                )

                # Wait 2 secs
                sleep(2)

                # Refresh
                soup = BeautifulSoup(Browser.page_source, "html5lib")
                obj = soup.select(
                    "div#importMatch div.market-group.clearfix > div.market-item.m-select-market")[j].find_all("li")

                # Loop
                for li in range(len(obj)):
                    # Check for handicap
                    if obj[li].get_text().strip() == 'Handicap':
                        Handicap = Browser.find_elements(
                            By.CSS_SELECTOR, 'div#importMatch div.market-group.clearfix > div.market-item.m-select-market')[j].find_elements(By.TAG_NAME, "li")[li].click()

                        break

            # Wait 5 seconds
            sleep(5)

            # Refresh
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            elem = soup.find_all('div', 'match-league')

            for m in range(len(elem)):
                # Compile
                cat = elem[m].find(
                    'span', 'text').get_text().replace(e, "").strip()
                div = elem[m].find_all('div', 'm-content-row')

                for i in range(len(div)):
                    _data = {}

                    home_team = div[i].find(
                        'div', 'home-team').get_text().strip()
                    away_team = div[i].find(
                        'div', 'away-team').get_text().strip()

                    # Switch to home-1
                    Browser.find_elements(
                        By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title")[0].click()

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    target = soup.select(
                        "html > div.af-select-list-open > span")

                    # Loop and select
                    for j in range(len(target)):
                        if target[j].get_text().strip() == "0:1":
                            Browser.find_elements(
                                By.CSS_SELECTOR, "html > div.af-select-list-open > span")[j].click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")

                            # Home Wins with Away 1 gaol Advantage
                            _data['1 [Away + 1]'] = soup.select('.match-league')[m].select(
                                '.m-content-row')[i].find_all("span", "m-outcome-odds")[0].get_text().strip()

                            break

                        # Default to zero
                        _data['1 [Away + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")

                    # Check
                    if not soup.select_one("html > div.af-select-list-open"):
                        # Close
                        Browser.find_elements(
                            By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title")[0].click()

                    # Wait 2 seconds
                    sleep(2)

                    # Loop and select
                    for k in range(len(target)):
                        if target[j].get_text().strip() == "1:0":
                            Browser.find_elements(
                                By.CSS_SELECTOR, "html > div.af-select-list-open > span")[j].click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")

                            # Away Wins with Home 1 gaol Advantage
                            _data['1 [Away + 1]'] = soup.select('.match-league')[m].select(
                                '.m-content-row')[i].find_all("span", "m-outcome-odds")[2].get_text().strip()

                            break

                        # Default to zero
                        _data['2 [Home + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")

                    # Check
                    if soup.select_one("html > div.af-select-list-open"):
                        # Close
                        Browser.find_elements(
                            By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title")[0].click()

                    # Switch to home+1 and Away+1
                    Browser.find_elements(
                        By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title")[0].click()

                    file[home_team + ' vs ' + away_team]["handicap"] = _data

            odds[e][catgy] = file

        with open('./Sportybet/sportybet_Single.txt', 'w') as outfile:
            json.dump(odds, outfile, indent=4)
        Browser.quit()
    else:
        # Initiate Collection
        odds = {}

        # Initiate Browser
        Browser.get(sportybet)

        # Wait
        WebDriverWait(Browser, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'match-league-wrap')))

        # Index
        l = data[category]['location']

        # Initiate Collection
        odds[category] = {}

        # Menu
        item = Browser.find_elements(
            By.CSS_SELECTOR, '.sport-list .category-list-item')[l + 1]

        # Extend submenu
        soup = BeautifulSoup(Browser.page_source, 'html5lib')
        ln = len(soup.select(
            '#sportList > div.game-list > ul.sport-list > li:nth-child(' + str(l + 1) + ') > div.tournament-list > ul > li'))

        # loop and click
        actions.move_to_element(item).perform()
        for z in range(ln):
            # Click
            d1 = Browser.find_elements(By.CSS_SELECTOR, '#sportList > div.game-list > ul.sport-list > li:nth-child(' + str(
                l + 1) + ') > div.tournament-list > ul > li')[z]
            Browser.execute_script("arguments[0].click();", d1)

            sleep(2)

        # Activate Single
        for j in range(ln):
            Browser.find_element(By.CSS_SELECTOR, '#importMatch > div:nth-child(' + str(
                2 + j) + ') > div > div.market-group.clearfix > div.market-item').click()

        # Wait 5 seconds
        sleep(5)

        # Parse HtmlDoc
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for each in elem:
            # Container
            file = {}

            # Compile
            category = each.find(
                'span', 'text').get_text().replace(category, "").strip()
            div = each.find_all('div', 'm-content-row')

            for cc in div:
                # Define Data
                _data = {}

                # Compile Names
                home_team = cc.find(
                    'div', 'home-team').get_text().strip()
                away_team = cc.find(
                    'div', 'away-team').get_text().strip()

                file[home_team + ' vs ' + away_team] = {}

                file[home_team + ' vs ' + away_team]['time'] = cc.find(
                    'div', 'clock-time').get_text().replace('&nbsp;', '').strip()

                # Home Win, Draw and Away Win Odds
                _data['home'] = cc.find_all(
                    'span', 'm-outcome-odds')[0].get_text().strip() or 0
                _data['draw'] = cc.find_all(
                    'span', 'm-outcome-odds')[1].get_text().strip() or 0
                _data['away'] = cc.find_all(
                    'span', 'm-outcome-odds')[2].get_text().strip() or 0

                # Upload
                file[home_team + ' vs ' + away_team]["single"] = _data

        # Wait 3 seconds
        sleep(3)

        # Activate Handicap
        for j in range(ln):
            # Click
            Browser.execute_script(
                """
                    document.querySelectorAll("div#importMatch div.market-group.clearfix > div.market-item.m-select-market")[ """ + str(j) + """].classList.add("show-item")
                """
            )

            # Wait 2 secs
            sleep(2)

            # Refresh
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            obj = soup.select(
                "div#importMatch div.market-group.clearfix > div.market-item.m-select-market")[j].find_all("li")

            # Loop
            for li in range(len(obj)):
                # Check for handicap
                if obj[li].get_text().strip() == 'Handicap':
                    Handicap = Browser.find_elements(
                        By.CSS_SELECTOR, 'div#importMatch div.market-group.clearfix > div.market-item.m-select-market')[j].find_elements(By.TAG_NAME, "li")[li].click()

                    break

        # Wait 5 seconds
        sleep(5)

        # Refresh
        soup = BeautifulSoup(Browser.page_source, "html5lib")
        elem = soup.find_all('div', 'match-league')

        for m in range(len(elem)):
            # Compile
            catgy = elem[m].find(
                'span', 'text').get_text().replace(category, "").strip()
            div = elem[m].find_all('div', 'm-content-row')

            for i in range(len(div)):
                info = {}

                home_team = div[i].find(
                    'div', 'home-team').get_text().strip()
                away_team = div[i].find(
                    'div', 'away-team').get_text().strip()

                if soup.select("div.match-league")[m].select("div.m-content-row")[i].find("div", "af-select-title"):
                    # Switch to home-1
                    Browser.find_elements(
                        By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title").click()

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    target = soup.select(
                        "html > div.af-select-list-open > span")

                    # Loop and select
                    for j in range(len(target)):
                        if target[j].get_text().strip() == "0:1":
                            Browser.find_elements(
                                By.CSS_SELECTOR, "html > div.af-select-list-open > span")[j].click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")

                            # Home Wins with Away 1 gaol Advantage
                            _data['1 [Away + 1]'] = soup.select('.match-league')[m].select(
                                '.m-content-row')[i].find_all("span", "m-outcome-odds")[0].get_text().strip()

                            break

                        # Default to zero
                        _data['1 [Away + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")

                    # Check
                    if not soup.select_one("html > div.af-select-list-open"):
                        # Close
                        Browser.find_elements(
                            By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title").click()

                    # Wait 2 seconds
                    sleep(2)

                    # Loop and select
                    for k in range(len(target)):
                        if target[j].get_text().strip() == "1:0":
                            Browser.find_elements(
                                By.CSS_SELECTOR, "html > div.af-select-list-open > span")[j].click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")

                            # Away Wins with Home 1 gaol Advantage
                            _data['1 [Away + 1]'] = soup.select('.match-league')[m].select(
                                '.m-content-row')[i].find_all("span", "m-outcome-odds")[2].get_text().strip()

                            break

                        # Default to zero
                        _data['2 [Home + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(Browser.page_source, "html5lib")

                    # Check
                    if not soup.select_one("html > div.af-select-list-open"):
                        # Close
                        Browser.find_elements(
                            By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title").click()

                    # Switch to Away + 1 and Home Win
                    Browser.find_elements(
                        By.CSS_SELECTOR, "div.match-league")[m].find_elements(By.CLASS_NAME, "m-content-row")[i].find_element(By.CLASS_NAME, "af-select-title").click()

                    file[home_team + ' vs ' + away_team]["handicap"] = _data
                else:
                    continue

        odds[category][catgy] = file

    with open('./Sportybet/sportybet_Single.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# getMenu()
SH_Chance(category="Australia")
