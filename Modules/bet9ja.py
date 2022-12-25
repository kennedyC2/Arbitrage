# Dependencies
# =============================================================================================================
from bs4 import BeautifulSoup
from time import sleep
import json
import re

# Websites
# =============================================================================================================
bet9ja = "https://sports.bet9ja.com/"


# Functions
# =============================================================================================================
# Bet9ja Menu
def getBet9ja_Menu(WebDriverWait, EC, By, browser=None, actionChains=None):
    # Object
    data = {}

    # Initialise browser
    actions = actionChains(browser)
    browser.get(bet9ja)

    # Wait
    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.ID, 'left_prematch_sport-1_soccer_label-toggle')))

    try:
        # Remove Ad Banner
        browser.execute_script(
            """
            setInterval(() => {
                const ad = document.getElementById("novasdk-inbox-widget");
                if (ad) {
                    ad.remove()
                }
            }, 10000)
            """
        )
    except:
        pass

    # Activate Menu
    browser.find_element(
        By.ID, "left_prematch_sport-1_soccer_label-toggle").click()

    sleep(5)

    browser.find_element(
        By.ID, "left_prematch_sport-1_soccer_labelmore-toggle").click()

    # Parse HtmlDoc
    soup = BeautifulSoup(browser.page_source, "html5lib")

    # Fetch Menu
    target = soup.select_one(
        ".accordion > .accordion-item--open")

    upper = target.select(
        ".accordion-content > .accordion-inner > .accordion-item")

    for div in upper:
        title = div.find("div", "accordion-text").get_text().strip()
        id = div.find("div", "accordion-toggle")['id']
        data[title] = {}
        data[title]['location'] = id

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']
        browser.find_element(By.ID, l).click()

        # Parse HtmlDoc
        soup = BeautifulSoup(browser.page_source, "html5lib")
        d = soup.find_all('a', 'menu-list__link txt-cut')
        e = []
        for t in d:
            f = {}
            f['title'] = ("_").join(t['title'].split(" ")).lower()
            f['id'] = re.sub('[a-zA-Z_,]', '',
                             t['id'].replace("_" + f['title'], ""))
            e.append(f)
        data[each]['submenu'] = e

        # Wait
        sleep(2)

    # Save as JSON
    with open('C:/Software Development/Arbitrage/Bet9ja/bet9ja_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)


# Bet9ja links
def getBet9ja_links():
    # web prefix
    p = bet9ja + 'competition/soccer/'

    # link Object
    files = {}

    # fetch menu
    with open('C:/Software Development/Arbitrage/Bet9ja/bet9ja_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    for e in data:
        # Define DAta Object
        files[e] = []

        # Loop
        for a in data[e]['submenu']:
            u = e.lower().replace(',', '').replace(' ', '') + '/'
            v = a['title'].lower().replace(',', '').replace(
                ' ', '').replace("_", "") + '/'
            w = a['id'].lower()[
                1:-1] if a['title'][0].isnumeric() else a['id'].lower()[1:]

            # full link
            fl = p + u + v + w

            # Object
            obj = {
                "sub-category": a["title"],
                "link": fl
            }

            # Update
            files[e].append(obj)

    # Save links
    with open('C:/Software Development/Arbitrage/Bet9ja/bet9ja_links.txt', 'w') as outfile:
        json.dump(files, outfile, indent=4)


# ==================================================================
#      Single Chance, Handicap
# ==================================================================

def bet9ja_SH_Chance(WebDriverWait, EC, By, browser=None, actionChains=None, fetchAll=False, category=None):
    # Variables
    global index
    global odds

    # ActionChains
    actions = actionChains(browser)

    # fetch links
    with open('C:/Software Development/Arbitrage/Bet9ja/bet9ja_links.txt', 'r') as json_file:
        data = json.load(json_file)

    if fetchAll:
        # Odds
        odds = {}

        for c in data:
            # Initiate Collection
            odds[c] = {}

            for e in range(len(data[c])):
                # Initiate browser
                browser.get(data[c][e]["link"])

                try:
                    # Wait
                    WebDriverWait(browser, 10).until(
                        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sports-table')))
                except:
                    pass

                file = {}

                try:
                    # Remove Ad Banner
                    browser.execute_script(
                        """
                        setInterval(() => {
                            const ad = document.getElementById("novasdk-inbox-widget");
                            if (ad) {
                                ad.remove()
                            }
                        }, 10000)
                        """
                    )
                except:
                    pass

                # Scroll the page
                height = int(browser.execute_script(
                    'return document.body.scrollHeight'))

                for b in range(1, height, 5):
                    browser.execute_script("window.scrollTo(0, {});".format(b))

                # Wait 2 seconds
                sleep(2)

                # Parse HtmlDoc
                soup = BeautifulSoup(browser.page_source, "html5lib")
                elem = soup.select('.sports-table > .table-f')

                for i in range(len(elem)):
                    # Define Data
                    _data1 = {}
                    _data2 = {}

                    # Compile Names
                    home_team = elem[i].find(
                        'div', 'sports-table__home').get_text().strip()
                    away_team = elem[i].find(
                        'div', 'sports-table__away').get_text().strip()

                    file[home_team + ' vs ' + away_team] = {}
                    file[home_team + ' vs ' + away_team]["date"] = elem[i].parent.find_previous_sibling(
                        "div").select_one(".sports-head__date > span").get_text().strip()
                    file[home_team + ' vs ' + away_team]["time"] = elem[i].find(
                        'span').get_text().strip()

                    # Home Win, Draw and Away Win Odds
                    info = elem[i].find_all(
                        'li', 'sports-table__odds-item')

                    _data1['home'] = info[0].get_text().strip() or 0

                    _data1['draw'] = info[1].get_text().strip() or 0

                    _data1['away'] = info[2].get_text().strip() or 0

                    _data2['1X'] = info[3].get_text().strip() or 0

                    _data2['12'] = info[4].get_text().strip() or 0

                    _data2['2X'] = info[5].get_text().strip() or 0

                    file[home_team + ' vs ' + away_team]["single"] = _data1

                    file[home_team + ' vs ' + away_team]["double"] = _data2

                # Get Length Of Possibilities
                box = len(soup.find_all('td', 'grid-table__td'))

                # Get index of Handicap
                for z in range(box):
                    index = -1
                    if soup.find_all('td', 'grid-table__td')[z].get_text().strip() == 'Handicap':
                        index = z
                        break

                # Activate handicap
                if index > -1:
                    # print(c, index)
                    # Click Handicap Tab
                    browser.find_elements(
                        By.CLASS_NAME, 'grid-table__td')[index].click()

                    try:
                        # Wait
                        WebDriverWait(browser, 10).until(
                            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sports-table')))
                    except:
                        pass

                    # Scroll the page
                    height = int(browser.execute_script(
                        'return document.body.scrollHeight'))

                    for i in range(1, height, 5):
                        browser.execute_script(
                            "window.scrollTo(0, {});".format(i))

                    # Parse HtmlDoc
                    soup = BeautifulSoup(browser.page_source, "html5lib")
                    elem = soup.select('.sports-table > .table-f')

                    for i in range(len(elem)):
                        _data = {}

                        # Compile
                        home_team = elem[i].find(
                            'div', 'sports-table__home').get_text().strip()
                        away_team = elem[i].find(
                            'div', 'sports-table__away').get_text().strip()

                        # Switch to home-1
                        browser.find_elements(
                            By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                        # Refresh
                        soup = BeautifulSoup(browser.page_source, "html5lib")
                        target = soup.select(
                            ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")

                        # Loop and select
                        for j in range(len(target)):
                            if target[j].find("a", "dropdown__link").get_text().strip() == "-1":
                                browser.find_elements(
                                    By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")[j].find_element(By.CLASS_NAME, "dropdown__link").click()

                                # Wait 2 seconds
                                sleep(2)

                                # Refresh
                                soup = BeautifulSoup(
                                    browser.page_source, "html5lib")

                                # Home Wins with Away 1 gaol Advantage
                                _data['1 [Away + 1]'] = soup.select('.sports-table > .table-f')[i].find_all('li', 'sports-table__odds-item')[
                                    1].get_text().strip() or 0

                                break

                            # Default to zero
                            _data['1 [Away + 1]'] = "0.00"

                        # Refresh
                        soup = BeautifulSoup(browser.page_source, "html5lib")

                        # Check
                        if soup.select_one(".sports-table__odds-item > .dropdown--open"):
                            # Close
                            browser.find_elements(
                                By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                        # Switch to home+1 and Away+1
                        browser.find_elements(
                            By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                        # Wait 2 seconds
                        sleep(2)

                        # Loop and select
                        for k in range(len(target)):
                            if target[k].find("a", "dropdown__link").get_text().strip() == "+1":
                                browser.find_elements(
                                    By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")[k].find_element(By.CLASS_NAME, "dropdown__link").click()

                                # Wait 2 seconds
                                sleep(2)

                                # Refresh
                                soup = BeautifulSoup(
                                    browser.page_source, "html5lib")

                                _data['2 [Home + 1]'] = soup.select('.sports-table > .table-f')[i].find_all('li', 'sports-table__odds-item')[
                                    3].get_text().strip() or 0

                                break

                            # Default to zero
                            _data['2 [Home + 1]'] = "0.00"

                        # Refresh
                        soup = BeautifulSoup(browser.page_source, "html5lib")

                        # Check
                        if soup.select_one(".sports-table__odds-item > .dropdown--open"):
                            # Close
                            browser.find_elements(
                                By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                        file[home_team + ' vs ' + away_team]["handicap"] = _data
                else:
                    continue

                odds[c][data[c][e]["sub-category"]] = file
    else:
        # Odds
        odds = {}

        # Initiate Collection
        odds[category] = {}

        for e in range(len(data[category])):
            # Initiate browser
            browser.get(data[category][e]["link"])

            try:
                # Wait
                WebDriverWait(browser, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sports-table')))
            except:
                pass

            file = {}

            try:
                # Remove Ad Banner
                browser.execute_script(
                    """
                    document.getElementById("novasdk-inbox-widget").remove()
                    """
                )
            except:
                pass

            # Scroll the page
            height = int(browser.execute_script(
                'return document.body.scrollHeight'))

            for b in range(1, height, 5):
                browser.execute_script("window.scrollTo(0, {});".format(b))

            # Wait 2 seconds
            sleep(2)

            # Parse HtmlDoc
            soup = BeautifulSoup(browser.page_source, "html5lib")
            elem = soup.select('.sports-table > .table-f')

            for i in range(len(elem)):
                # Define Data
                _data1 = {}
                _data2 = {}

                # Compile Names
                home_team = elem[i].find(
                    'div', 'sports-table__home').get_text().strip()
                away_team = elem[i].find(
                    'div', 'sports-table__away').get_text().strip()

                file[home_team + ' vs ' + away_team] = {}
                file[home_team + ' vs ' + away_team]["date"] = elem[i].parent.find_previous_sibling(
                    "div").select_one(".sports-head__date > span").get_text().strip()
                file[home_team + ' vs ' + away_team]["time"] = elem[i].find(
                    'span').get_text().strip()

                # Home Win, Draw and Away Win Odds
                info = elem[i].find_all(
                    'li', 'sports-table__odds-item')

                _data1['home'] = info[0].get_text().strip() or 0

                _data1['draw'] = info[1].get_text().strip() or 0

                _data1['away'] = info[2].get_text().strip() or 0

                _data2['1X'] = info[3].get_text().strip() or 0

                _data2['12'] = info[4].get_text().strip() or 0

                _data2['2X'] = info[5].get_text().strip() or 0

                file[home_team + ' vs ' + away_team]["single"] = _data1

                file[home_team + ' vs ' + away_team]["double"] = _data2

            # Get Length Of Possibilities
            box = len(soup.find_all('td', 'grid-table__td'))

            # Get index of Handicap
            for z in range(box):
                index = -1
                if soup.find_all('td', 'grid-table__td')[z].get_text().strip() == 'Handicap':
                    index = z
                    break

            # Activate handicap
            if index > -1:
                # Click Handicap Tab
                browser.find_elements(
                    By.CLASS_NAME, 'grid-table__td')[index].click()

                try:
                    # Wait
                    WebDriverWait(browser, 10).until(
                        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sports-table')))
                except:
                    pass

                # Scroll the page
                height = int(browser.execute_script(
                    'return document.body.scrollHeight'))

                for i in range(1, height, 5):
                    browser.execute_script("window.scrollTo(0, {});".format(i))

                # Parse HtmlDoc
                soup = BeautifulSoup(browser.page_source, "html5lib")
                elem = soup.select('.sports-table > .table-f')

                for i in range(len(elem)):
                    _data = {}

                    # Compile
                    home_team = elem[i].find(
                        'div', 'sports-table__home').get_text().strip()
                    away_team = elem[i].find(
                        'div', 'sports-table__away').get_text().strip()

                    # Switch to home-1
                    browser.find_elements(
                        By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                    # Refresh
                    soup = BeautifulSoup(browser.page_source, "html5lib")
                    target = soup.select(
                        ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")

                    # Loop and select
                    for j in range(len(target)):
                        if target[j].find("a", "dropdown__link").get_text().strip() == "-1":
                            browser.find_elements(
                                By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")[j].find_element(By.CLASS_NAME, "dropdown__link").click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                browser.page_source, "html5lib")

                            # Home Wins with Away 1 gaol Advantage
                            _data['1 [Away + 1]'] = soup.select('.sports-table > .table-f')[i].find_all('li', 'sports-table__odds-item')[
                                1].get_text().strip() or 0

                            break

                        # Default to zero
                        _data['1 [Away + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(browser.page_source, "html5lib")

                    # Check
                    if soup.select_one(".sports-table__odds-item > .dropdown--open"):
                        # Close
                        browser.find_elements(
                            By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                    # Switch to home+1 and Away+1
                    browser.find_elements(
                        By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                    # Wait 2 seconds
                    sleep(2)

                    # Loop and select
                    for k in range(len(target)):
                        if target[k].find("a", "dropdown__link").get_text().strip() == "+1":
                            browser.find_elements(
                                By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown--open > .dropdown__menu > .dropdown__item")[k].find_element(By.CLASS_NAME, "dropdown__link").click()

                            # Wait 2 seconds
                            sleep(2)

                            # Refresh
                            soup = BeautifulSoup(
                                browser.page_source, "html5lib")

                            _data['2 [Home + 1]'] = soup.select('.sports-table > .table-f')[i].find_all('li', 'sports-table__odds-item')[
                                3].get_text().strip() or 0

                            break

                        # Default to zero
                        _data['2 [Home + 1]'] = "0.00"

                    # Refresh
                    soup = BeautifulSoup(browser.page_source, "html5lib")

                    # Check
                    if soup.select_one(".sports-table__odds-item > .dropdown--open"):
                        # Close
                        browser.find_elements(
                            By.CSS_SELECTOR, ".sports-table__odds-item > .dropdown > .dropdown__toggle")[i].click()

                    file[home_team + ' vs ' + away_team]["handicap"] = _data
            else:
                continue

            odds[category][data[category][e]["sub-category"]] = file

    with open('./Bet9ja/data.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
