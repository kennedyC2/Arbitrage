# Imports
# ================================================================================
from bet9ja import getBet9ja_Menu, getBet9ja_links, bet9ja_SH_Chance
from betking import getBetking_Menu, betking_SH_Chance
from arbitrage import Compile, pair_up, Arbitrage_3
from time import sleep

# Dependencies
# ================================================================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Browser Configurations
# ================================================================================
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.page_load_strategy = "eager"
service = Service(
    executable_path="C:\Software Development\Arbitrage\chromedriver.exe")

# Globals


# Initialize APP
def app(Browser, data):
    # Get Bet9ja menu
    getBet9ja_Menu(
        WebDriverWait, EC, By, browser=Browser, actionChains=ActionChains)

    # Wait
    sleep(5)

    # Compile links
    getBet9ja_links()

    # Wait
    sleep(2)

    # Get Betking menu
    getBetking_Menu(
        WebDriverWait, EC, By, browser=Browser, actionChains=ActionChains)

    # Wait
    sleep(5)

    # fetch bet9ja ODDs
    bet9ja_SH_Chance(
        WebDriverWait, EC, By, category=data, browser=Browser, actionChains=ActionChains)

    # Wait
    sleep(5)

    # fetch betking ODDs
    betking_SH_Chance(
        WebDriverWait, EC, By,  category=data, browser=Browser, actionChains=ActionChains)

    # Close
    Browser.quit()

    # Wait
    sleep(5)

    # COmpile
    Compile(category=data)

    # Wait
    sleep(2)

    # Pair_Up
    pair_up()

    # Wait
    sleep(2)

    # Calculate
    Arbitrage_3(total_stake=1000)


def app_start(data):
    while True:
        app(Browser=webdriver.Chrome(service=service, options=options), data=data)

        # wait
        sleep(60 * 60 * 12)


app_start("Brazil")
