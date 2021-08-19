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
bet365 = "https://www.bet365.com"


# Functions
# =============================================================================================================

# Get Menu
def getMenu():

    # Object
    data = {}

    # Initiate Browser
    Browser.get(bet365)

    # Wait
    time.sleep(20)

    # Locate Soccer
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    all = soup.select('.wn-PreMatchGroup > div')
    for div in all:
        if div.get_text().replace('"', '').strip() == 'Soccer':
            # Activate Menu
            Browser.find_element(By.CSS_SELECTOR,
                                 '.wn-PreMatchGroup div:nth-child(' + str(all.index(div) + 1) + ')').click()
            break

    # Wait
    time.sleep(10)

    # Close
    Browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[4]/div[1]').click()

    # Wait
    time.sleep(5)

    # Wait
    time.sleep(5)

    # Parse HtmlDoc
    soup = BeautifulSoup(Browser.page_source, "html5lib")

    # Fetch Menu
    collection = soup.find(
        'div', 'gl-MarketGrid').find_all('div', 'sm-SplashMarketGroup')[0].select('.sm-SplashMarket')
    for d in collection:
        span = d.find('div', 'sm-SplashMarket_Title')
        title = span.get_text().strip()
        id = collection.index(d)
        data[title] = {}
        data[title]['location'] = id

    for e in range(len(collection)):
        if collection[e].find('div', 'sm-SplashMarket_HeaderOpen'):
            # Close
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

    # fetch Submenu and Menu link
    for each in data:
        l = data[each]['location']

        if l > 0:
            # Click
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(5)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            d = soup.find_all('div', 'sm-CouponLink')
            e = []
            for t in d:
                e.append(t.find('span').get_text().strip())
            data[each]['submenu'] = e

            # UnClick
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(5)
        else:
            pass

    # Save as JSON
    with open('./../Bet365/bet365_menu.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    Browser.quit()


# Bet365 Odds
# ======================================================================================

# Single
def Single():
    # Odds
    odds = {}

    # fetch links
    with open('./../Bet365/bet365_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(bet365)

    # Wait
    time.sleep(10)
    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'wn-PreMatchGroup')))

    # Locate Soccer
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    all = soup.select('.wn-PreMatchGroup > div')
    for div in all:
        if div.get_text().replace('"', '').strip() == 'Soccer':
            # Activate Menu
            Browser.find_element(By.CSS_SELECTOR,
                                 '.wn-PreMatchGroup div:nth-child(' + str(all.index(div) + 1) + ')').click()

    # Wait
    time.sleep(5)

    collection = len(data.keys())
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    extra = soup.find(
        'div', 'gl-MarketGrid').find_all('div', 'sm-SplashMarketGroup')[0].select('.sm-SplashMarket')

    for e in range(collection):
        if extra[e].find('div', 'sm-SplashMarket_HeaderOpen'):
            # Wait
            WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]')))

            # Close
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

    for each in data:
        l = data[each]['location']

        if l == 1:
            # Click
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

            # Click Submenu
            Browser.find_elements(By.CLASS_NAME, 'sm-CouponLink')[0].click()

            # Wait
            time.sleep(10)

            # 1st dropdown
            el1 = Browser.find_element(By.CLASS_NAME,
                                       'sph-EventHeader_Dropdown')
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            item = len(soup.find_all('div', 'sdd-MultiLevelDropDownItem'))

            # Wait
            time.sleep(3)

            title = soup.select('.sdd-MultiLevelDropDownItem > span')

            # Close Dropdown
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Deeper
            for i in range(item):
                if i > 0:
                    # Open Dropdown
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el1 = Browser.find_element(By.CLASS_NAME,
                                               'sph-EventHeader_Dropdown')
                    actions.move_to_element(el1).click().perform()

                    # Wait
                    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']')))

                    # Select match type
                    Browser.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']').click()

                    # Wait
                    time.sleep(5)

                    # Select Odd type
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el2 = Browser.find_element(By.CLASS_NAME,
                                               'src-MarketGroupButton_TextWrapper')
                    actions.move_to_element(el2).click().perform()

                    # Wait
                    time.sleep(5)

                    soup = BeautifulSoup(Browser.page_source, 'html5lib')
                    lvl = soup.find_all(
                        'div', 'smd-DropDownItem')

                    # loop
                    for j in lvl:
                        if j.find('span').get_text() == 'Full Time Result':
                            Browser.find_elements(By.CLASS_NAME,
                                                  'smd-DropDownItem')[lvl.index(j)].click()

                            # Wait
                            time.sleep(5)

                            # Line
                            olympics = []

                            # Parse HtmlDoc
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")
                            elem = soup.find(
                                'div', 'src-MarketGroup_Container')

                            # Highlight
                            all_team = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails')

                            all_time = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails_BookCloses')

                            all_home = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[0].find_all('div', 'sgl-ParticipantOddsOnly80')

                            all_away = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[2].find_all('div', 'sgl-ParticipantOddsOnly80')

                            num = len(all_time)

                            for k in range(num):
                                # Compile
                                info = {}
                                team = all_team[k].find_all(
                                    'div', 'rcl-ParticipantFixtureDetailsTeam_TeamName')
                                info['match'] = team[0].get_text().strip(
                                ) + ' vs ' + team[1].get_text().strip()
                                info['time'] = all_time[k].get_text()
                                info['home'] = all_home[k].find(
                                    'span').get_text().strip() or 0
                                info['away'] = all_away[k].find(
                                    'span').get_text().strip() or 0

                                # Upload
                                olympics.append(info)
                            break

                    odds[title[i].get_text()] = olympics

                    if soup.find('div', 'smd-DropDownContainer-visible'):
                        el3 = Browser.find_element(By.CLASS_NAME,
                                                   'src-MarketGroupButton_TextWrapper')
                        actions.move_to_element(el3).click().perform()

            # Return to HO
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div').click()

            # Wait
            time.sleep(10)

    with open('./../Bet365/bet365_Single.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# Double
def Double():
    # Odds
    odds = {}

    # fetch links
    with open('./../Bet365/bet365_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(bet365)

    # Wait
    time.sleep(10)
    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'wn-PreMatchGroup')))

    # Locate Soccer
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    all = soup.select('.wn-PreMatchGroup > div')
    for div in all:
        if div.get_text().replace('"', '').strip() == 'Soccer':
            # Activate Menu
            Browser.find_element(By.CSS_SELECTOR,
                                 '.wn-PreMatchGroup div:nth-child(' + str(all.index(div) + 1) + ')').click()

    # Wait
    time.sleep(5)

    collection = len(data.keys())
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    extra = soup.find(
        'div', 'gl-MarketGrid').find_all('div', 'sm-SplashMarketGroup')[0].select('.sm-SplashMarket')

    for e in range(collection):
        if extra[e].find('div', 'sm-SplashMarket_HeaderOpen'):
            # Wait
            WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]')))

            # Close
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

    for each in data:
        l = data[each]['location']

        if l == 1:
            # Click
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

            # Click Submenu
            Browser.find_elements(By.CLASS_NAME, 'sm-CouponLink')[0].click()

            # Wait
            time.sleep(10)

            # 1st dropdown
            el1 = Browser.find_element(By.CLASS_NAME,
                                       'sph-EventHeader_Dropdown')
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            item = len(soup.find_all('div', 'sdd-MultiLevelDropDownItem'))

            # Wait
            time.sleep(3)

            title = soup.select('.sdd-MultiLevelDropDownItem > span')

            # Close Dropdown
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Deeper
            for i in range(item):
                if i > 0:
                    # Open Dropdown
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el1 = Browser.find_element(By.CLASS_NAME,
                                               'sph-EventHeader_Dropdown')
                    actions.move_to_element(el1).click().perform()

                    # Wait
                    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']')))

                    # Select match type
                    Browser.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']').click()

                    # Wait
                    time.sleep(5)

                    # Select Odd type
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el2 = Browser.find_element(By.CLASS_NAME,
                                               'src-MarketGroupButton_TextWrapper')
                    actions.move_to_element(el2).click().perform()

                    # Wait
                    time.sleep(5)

                    soup = BeautifulSoup(Browser.page_source, 'html5lib')
                    lvl = soup.find_all(
                        'div', 'smd-DropDownItem')

                    # loop
                    for j in lvl:
                        if j.find('span').get_text() == 'Double Chance':
                            Browser.find_elements(By.CLASS_NAME,
                                                  'smd-DropDownItem')[lvl.index(j)].click()

                            # Wait
                            time.sleep(5)

                            olympics = []

                            # Parse HtmlDoc
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")
                            elem = soup.find(
                                'div', 'src-MarketGroup_Container')

                            # Highlight
                            all_team = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails')

                            all_time = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails_BookCloses')

                            all_home = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[0].find_all('div', 'sgl-ParticipantOddsOnly80')

                            all_away = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[1].find_all('div', 'sgl-ParticipantOddsOnly80')

                            num = len(all_time)

                            for k in range(num):
                                # Compile
                                info = {}
                                team = all_team[k].find_all(
                                    'div', 'rcl-ParticipantFixtureDetailsTeam_TeamName')
                                info['match'] = team[0].get_text().strip(
                                ) + ' vs ' + team[1].get_text().strip()
                                info['time'] = all_time[k].get_text()
                                info['home'] = all_home[k].find(
                                    'span').get_text().strip() or 0
                                info['away'] = all_away[k].find(
                                    'span').get_text().strip() or 0

                                # Upload
                                olympics.append(info)
                                # print(info)
                            break

                    odds[title[i].get_text()] = olympics

                    if soup.find('div', 'smd-DropDownContainer-visible'):
                        el3 = Browser.find_element(By.CLASS_NAME,
                                                   'src-MarketGroupButton_TextWrapper')
                        actions.move_to_element(el3).click().perform()

            # Return to HO
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div').click()

            # Wait
            time.sleep(10)

    with open('./../Bet365/bet365_Double.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# DNB
def DNB():
    # Odds
    odds = {}

    # fetch links
    with open('./../Bet365/bet365_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(bet365)

    # Wait
    time.sleep(10)
    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'wn-PreMatchGroup')))

    # Locate Soccer
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    all = soup.select('.wn-PreMatchGroup > div')
    for div in all:
        if div.get_text().replace('"', '').strip() == 'Soccer':
            # Activate Menu
            Browser.find_element(By.CSS_SELECTOR,
                                 '.wn-PreMatchGroup div:nth-child(' + str(all.index(div) + 1) + ')').click()

    # Wait
    time.sleep(5)

    collection = len(data.keys())
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    extra = soup.find(
        'div', 'gl-MarketGrid').find_all('div', 'sm-SplashMarketGroup')[0].select('.sm-SplashMarket')

    for e in range(collection):
        if extra[e].find('div', 'sm-SplashMarket_HeaderOpen'):
            # Wait
            WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]')))

            # Close
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

    for each in data:
        l = data[each]['location']

        if l == 1:
            # Click
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

            # Click Submenu
            Browser.find_elements(By.CLASS_NAME, 'sm-CouponLink')[0].click()

            # Wait
            time.sleep(10)

            # 1st dropdown
            el1 = Browser.find_element(By.CLASS_NAME,
                                       'sph-EventHeader_Dropdown')
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            item = len(soup.find_all('div', 'sdd-MultiLevelDropDownItem'))

            # Wait
            time.sleep(3)

            title = soup.select('.sdd-MultiLevelDropDownItem > span')

            # Close Dropdown
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Deeper
            for i in range(item):
                if i > 0:
                    # Open Dropdown
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el1 = Browser.find_element(By.CLASS_NAME,
                                               'sph-EventHeader_Dropdown')
                    actions.move_to_element(el1).click().perform()

                    # Wait
                    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']')))

                    # Select match type
                    Browser.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']').click()

                    # Wait
                    time.sleep(5)

                    # Select Odd type
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el2 = Browser.find_element(By.CLASS_NAME,
                                               'src-MarketGroupButton_TextWrapper')
                    actions.move_to_element(el2).click().perform()

                    # Wait
                    time.sleep(5)

                    soup = BeautifulSoup(Browser.page_source, 'html5lib')
                    lvl = soup.find_all(
                        'div', 'smd-DropDownItem')

                    # loop
                    for j in lvl:
                        if j.find('span').get_text() == 'Draw No Bet':
                            Browser.find_elements(By.CLASS_NAME,
                                                  'smd-DropDownItem')[lvl.index(j)].click()

                            # Wait
                            time.sleep(5)

                            # Line
                            olympics = []

                            # Parse HtmlDoc
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")
                            elem = soup.find(
                                'div', 'src-MarketGroup_Container')

                            # Highlight
                            all_team = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails')

                            all_time = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails_BookCloses')

                            all_home = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[0].find_all('div', 'sgl-ParticipantOddsOnly80')

                            all_away = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[1].find_all('div', 'sgl-ParticipantOddsOnly80')

                            num = len(all_time)

                            for k in range(num):
                                # Compile
                                info = {}
                                team = all_team[k].find_all(
                                    'div', 'rcl-ParticipantFixtureDetailsTeam_TeamName')
                                info['match'] = team[0].get_text().strip(
                                ) + ' vs ' + team[1].get_text().strip()
                                info['time'] = all_time[k].get_text()
                                info['home'] = all_home[k].find(
                                    'span').get_text().strip() or 0
                                info['away'] = all_away[k].find(
                                    'span').get_text().strip() or 0

                                # Upload
                                olympics.append(info)
                                # print(info)
                            break

                    odds[title[i].get_text()] = olympics

                    if soup.find('div', 'smd-DropDownContainer-visible'):
                        el3 = Browser.find_element(By.CLASS_NAME,
                                                   'src-MarketGroupButton_TextWrapper')
                        actions.move_to_element(el3).click().perform()

            # Return to HO
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div').click()

            # Wait
            time.sleep(10)

    with open('./../Bet365/bet365_DNB.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# GGNG
def GGNG():
    # Odds
    odds = {}

    # fetch links
    with open('./../Bet365/bet365_menu.txt', 'r') as json_file:
        global data
        data = json.load(json_file)

    # Initiate Browser
    Browser.get(bet365)

    # Wait
    time.sleep(10)
    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'wn-PreMatchGroup')))

    # Locate Soccer
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    all = soup.select('.wn-PreMatchGroup > div')
    for div in all:
        if div.get_text().replace('"', '').strip() == 'Soccer':
            # Activate Menu
            Browser.find_element(By.CSS_SELECTOR,
                                 '.wn-PreMatchGroup div:nth-child(' + str(all.index(div) + 1) + ')').click()

    # Wait
    time.sleep(5)

    collection = len(data.keys())
    soup = BeautifulSoup(Browser.page_source, "html5lib")
    extra = soup.find(
        'div', 'gl-MarketGrid').find_all('div', 'sm-SplashMarketGroup')[0].select('.sm-SplashMarket')

    for e in range(collection):
        if extra[e].find('div', 'sm-SplashMarket_HeaderOpen'):
            # Wait
            WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]')))

            # Close
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(e + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

    for each in data:
        l = data[each]['location']

        if l == 1:
            # Click
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[3]/div[2]/div/div[' + str(l + 1) + ']/div[1]').click()

            # Wait
            time.sleep(3)

            # Click Submenu
            Browser.find_elements(By.CLASS_NAME, 'sm-CouponLink')[0].click()

            # Wait
            time.sleep(10)

            # 1st dropdown
            el1 = Browser.find_element(By.CLASS_NAME,
                                       'sph-EventHeader_Dropdown')
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Parse HtmlDoc
            soup = BeautifulSoup(Browser.page_source, "html5lib")
            item = len(soup.find_all('div', 'sdd-MultiLevelDropDownItem'))

            # Wait
            time.sleep(3)

            title = soup.select('.sdd-MultiLevelDropDownItem > span')

            # Close Dropdown
            actions.move_to_element(el1).click().perform()

            # Wait
            time.sleep(3)

            # Deeper
            for i in range(item):
                if i > 0:
                    # Open Dropdown
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el1 = Browser.find_element(By.CLASS_NAME,
                                               'sph-EventHeader_Dropdown')
                    actions.move_to_element(el1).click().perform()

                    # Wait
                    WebDriverWait(Browser, 60).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']')))

                    # Select match type
                    Browser.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[' + str(i + 1) + ']').click()

                    # Wait
                    time.sleep(5)

                    # Select Odd type
                    soup = BeautifulSoup(Browser.page_source, "html5lib")
                    el2 = Browser.find_element(By.CLASS_NAME,
                                               'src-MarketGroupButton_TextWrapper')
                    actions.move_to_element(el2).click().perform()

                    # Wait
                    time.sleep(5)

                    soup = BeautifulSoup(Browser.page_source, 'html5lib')
                    lvl = soup.find_all(
                        'div', 'smd-DropDownItem')

                    # loop
                    for j in lvl:
                        if j.find('span').get_text() == 'Both Teams to Score':
                            Browser.find_elements(By.CLASS_NAME,
                                                  'smd-DropDownItem')[lvl.index(j)].click()

                            # Wait
                            time.sleep(5)

                            # Line
                            olympics = []

                            # Parse HtmlDoc
                            soup = BeautifulSoup(
                                Browser.page_source, "html5lib")
                            elem = soup.find(
                                'div', 'src-MarketGroup_Container')

                            # Highlight
                            all_team = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails')

                            all_time = elem.find_all(
                                'div', 'rcl-ParticipantFixtureDetails_BookCloses')

                            all_home = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[0].find_all('div', 'sgl-ParticipantOddsOnly80')

                            all_away = elem.find_all(
                                'div', 'sgl-MarketOddsExpand')[1].find_all('div', 'sgl-ParticipantOddsOnly80')

                            num = len(all_time)

                            for k in range(num):
                                # Compile
                                info = {}
                                team = all_team[k].find_all(
                                    'div', 'rcl-ParticipantFixtureDetailsTeam_TeamName')
                                info['match'] = team[0].get_text().strip(
                                ) + ' vs ' + team[1].get_text().strip()
                                info['time'] = all_time[k].get_text()
                                info['home'] = all_home[k].find(
                                    'span').get_text().strip() or 0
                                info['away'] = all_away[k].find(
                                    'span').get_text().strip() or 0

                                # Upload
                                olympics.append(info)
                                print(info)
                            break
                        else:
                            pass

                    odds[title[i].get_text()] = olympics

                    if soup.find('div', 'smd-DropDownContainer-visible'):
                        el3 = Browser.find_element(By.CLASS_NAME,
                                                   'src-MarketGroupButton_TextWrapper')
                        actions.move_to_element(el3).click().perform()

            # Return to HO
            Browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div').click()

            # Wait
            time.sleep(10)

    with open('./../Bet365/bet365_GGNG.txt', 'w') as outfile:
        json.dump(odds, outfile, indent=4)
    Browser.quit()


# getMenu()
# Single()
# Double()
# DNB()
# GGNG()
