# Dependencies
# =============================================================================================================
from bs4 import BeautifulSoup
import time
import json

# Websites
# =============================================================================================================
betking = "https://www.betking.com/sports/s/prematch/soccer"


# Functions
# =============================================================================================================

# Get Menu
def getBetking_Menu(WebDriverWait, EC, By, browser=None, actionChains=None):
    # Object
    data = {}

    # Initiate browser
    actions = actionChains(browser)
    browser.get(betking)

    # Wait
    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a')))

    # Activate Menu
    browser.find_element(
        By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a').click()

    # Wait
    time.sleep(5)

    # Parse HtmlDoc
    soup = BeautifulSoup(browser.page_source, "html5lib")

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
            browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l) + ') > a').click()

            # Parse HtmlDoc
            soup = BeautifulSoup(browser.page_source, "html5lib")
            d = soup.find_all('li', 'level-3')
            e = []
            for t in d:
                e.append(t.find('span').get_text().strip())
            data[each]['submenu'] = e

            # UnClick
            browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l) + ') > a').click()
        else:
            pass

    # Save as JSON
    with open('./Betking/betking_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)


# ==================================================================
#      Single Chance, Handicap
# ==================================================================

def betking_SH_Chance(WebDriverWait, EC, By, browser=None, actionChains=None, fetchAll=False, category=None):
    # Odds
    odds = {}

    # fetch links
    with open('./Betking/betking_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate browser
    actions = actionChains(browser)
    browser.get(betking)

    # Wait
    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a')))

    # Activate Menu
    browser.find_element(
        By.CSS_SELECTOR, '#prematchMenu > ul > li.level-1.child-active > a').click()

    if fetchAll:
        for e in data:
            # Index
            l = data[e]['location']

            if l > 2:
                # Initiate Collection
                odds[e] = {}

                # Activate Submenu
                browser.find_element(
                    By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()

                # Wait 10 seconds
                time.sleep(10)

                # Parse HtmlDoc
                soup = BeautifulSoup(browser.page_source, "html5lib")
                ln = soup.find_all('div', 'eventContainer')

                # Loop & Fetch Single Odds
                for ch in range(len(ln)):
                    # Container
                    file = {}

                    elem = soup.find_all('tr', 'trOddsSection')

                    for each in elem:
                        # Define Data
                        _data1 = {}
                        _data2 = {}
                        print(e)

                        # Compile
                        match = each.find(
                            'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')
                        file[match] = {}

                        file[match]["time"] = each.find(
                            'td', 'eventDate').get_text().strip()

                        # Home Win, Draw and Away Win Odds
                        g_odds = each.find_all('div', 'oddBorder')

                        if len(g_odds) >= 8:
                            _data1['home'] = g_odds[0].get_text().strip() or 0

                            _data1['draw'] = g_odds[1].get_text().strip() or 0

                            _data1['away'] = g_odds[2].get_text().strip() or 0

                            _data2['1X'] = g_odds[3].get_text().strip() or 0

                            _data2['12'] = g_odds[4].get_text().strip() or 0

                            _data2['2X'] = g_odds[5].get_text().strip() or 0

                            # Upload
                            file[match]["single"] = _data1
                            file[match]["double"] = _data2
                            odds[e][data[e]["submenu"][ch]] = file

                # Loop & Fetch Handicap Odds
                for ch in range(len(ln)):
                    # Container
                    file = {}

                    soup = BeautifulSoup(browser.page_source, "html5lib")
                    obj = soup.select(
                        '.eventContainer')[ch].select('.regionAreaContainer > .area')
                    for div in obj:
                        if div.find('div').get_text() == 'Handicap':
                            Handicap = browser.find_element(
                                By.CSS_SELECTOR, '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                            browser.execute_script(
                                "arguments[0].click();", Handicap)

                            # Wait 5 seconds
                            time.sleep(5)

                            # Refresh
                            soup = BeautifulSoup(
                                browser.page_source, "html5lib")
                            elem = soup.find_all("table", "oddsTable")[
                                ch].find_all('tr', 'trOddsSection')

                            for each in elem:
                                _data = {}

                                match = each.find(
                                    'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')

                                g_odds = each.find_all('div', 'multilineType')

                                if len(g_odds) >= 8:
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
                browser.find_element(
                    By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()
                browser.find_element(
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
            browser.find_element(
                By.CSS_SELECTOR, '#prematchMenu > ul > li:nth-child(' + str(l + 2) + ') > a > i.box-icon.icon-box.fa.fa-square-o').click()

            # Wait 10 seconds
            time.sleep(10)

            # Parse HtmlDoc
            soup = BeautifulSoup(browser.page_source, "html5lib")
            ln = soup.find_all('div', 'eventContainer')

            # Loop & Fetch Single Odds
            for ch in range(len(ln)):
                # Container
                file = {}

                elem = soup.find_all("table", "oddsTable")[
                    ch].find_all('tr', 'trOddsSection')

                for each in elem:
                    # Define Data
                    _data1 = {}
                    _data2 = {}

                    # Compile
                    match = each.find(
                        'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')
                    file[match] = {}

                    file[match]["time"] = each.find(
                        'td', 'eventDate').get_text().strip()

                    # Home Win, Draw and Away Win Odds
                    g_odds = each.find_all('div', 'oddBorder')

                    if len(g_odds) >= 8:
                        _data1['home'] = g_odds[0].get_text().strip() or 0

                        _data1['draw'] = g_odds[1].get_text().strip() or 0

                        _data1['away'] = g_odds[2].get_text().strip() or 0

                        _data2['1X'] = g_odds[3].get_text().strip() or 0

                        _data2['12'] = g_odds[4].get_text().strip() or 0

                        _data2['2X'] = g_odds[5].get_text().strip() or 0

                        # Upload
                        file[match]["single"] = _data1
                        file[match]["double"] = _data2

                odds[category][data[category]["submenu"][ch]] = file

            # Loop & Fetch Handicap Odds
            for ch in range(len(ln)):
                # Container
                file = {}

                soup = BeautifulSoup(browser.page_source, "html5lib")
                obj = soup.select(
                    '.eventContainer')[ch].select('.regionAreaContainer > .area')
                for div in obj:
                    if div.find('div').get_text() == 'Handicap':
                        Handicap = browser.find_element(
                            By.CSS_SELECTOR, '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
                        browser.execute_script(
                            "arguments[0].click();", Handicap)

                        # Wait 5 seconds
                        time.sleep(5)

                        # Refresh
                        soup = BeautifulSoup(browser.page_source, "html5lib")
                        elem = soup.find_all("table", "oddsTable")[
                            ch].find_all('tr', 'trOddsSection')

                        for each in elem:
                            _data = {}

                            match = each.find(
                                'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')

                            g_odds = each.find_all('div', 'multilineType')

                            if len(g_odds) >= 8:
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
                    else:
                        # Refresh
                        soup = BeautifulSoup(browser.page_source, "html5lib")
                        elem = soup.find_all("table", "oddsTable")[
                            ch].find_all('tr', 'trOddsSection')

                        for each in elem:
                            _data = {}

                            match = each.find(
                                'td', 'matchName')['data-matchname'].strip().replace('-', 'vs')

                            # Default to zero
                            _data['1 [Away + 1]'] = "0.00"

                            # Default to zero
                            _data['2 [Home + 1]'] = "0.00"

                            # Upload
                            odds[category][data[category]["submenu"]
                                           [ch]][match]["handicap"] = _data

            # Wait 5 seconds
            time.sleep(5)

    with open('./Betking/data.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
