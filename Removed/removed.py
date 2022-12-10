# ======================================================================================
#                                    Bet9ja Odds
# ======================================================================================

# # DNB
# def DNB():
#     # Odds
#     odds = []

#     # fetch links
#     with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
#         global data
#         data = json.load(json_file)

#     for e in data:
#         # Initiate Browser
#         Browser.get(data[e])

#         # Wait 5 seconds
#         sleep(5)

#         # Index of target
#         index = -1

#         # Get index
#         soup = BeautifulSoup(Browser.page_source, 'html5lib')
#         box = len(soup.find_all('td', 'grid-table__td'))
#         for i in range(box):
#             if soup.find_all('td', 'grid-table__td')[i].get_text().strip() == 'DNB':
#                 index = i
#                 break

#         # Activate DNB
#         if index > -1:
#             Browser.find_elements(
#                 By.CLASS_NAME, 'grid-table__td')[index].click()

#             # Wait 5 seconds
#             sleep(5)

#             # Scroll the page
#             height = int(Browser.execute_script(
#                 'return document.body.scrollHeight'))
#             for i in range(1, height, 10):
#                 Browser.execute_script("window.scrollTo(0, {});".format(i))

#             # Wait 5 seconds
#             sleep(5)

#             # Parse HtmlDoc
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             elem = soup.select('.sports-table > .table-f')

#             for each in elem:
#                 # Compile
#                 info = {}
#                 home_team = each.find(
#                     'div', 'sports-table__home').get_text().strip()
#                 away_team = each.find(
#                     'div', 'sports-table__away').get_text().strip()

#                 info['category'] = e
#                 info['match'] = home_team + ' vs ' + away_team
#                 info['time'] = each.find('span').get_text().strip()
#                 info['home'] = each.find_all(
#                     'li', 'sports-table__odds-item')[0].get_text().strip() or 0
#                 info['away'] = each.find_all(
#                     'li', 'sports-table__odds-item')[1].get_text().strip() or 0

#                 # Upload
#                 odds.append(info)
#         else:
#             pass
#         continue

#     with open('./Bet9ja/bet9ja_DNB.txt', 'w') as outfile:
#         json.dump(odds, outfile, indent=4)
#     Browser.quit()


# # GGNG
# def GGNG():
#     # Odds
#     odds = []

#     # fetch links
#     with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
#         global data
#         data = json.load(json_file)

#     for e in data:
#         # Initiate Browser
#         Browser.get(data[e])

#         # Wait 5 seconds
#         sleep(5)

#         # Index of target
#         index = -1

#         # Get index
#         soup = BeautifulSoup(Browser.page_source, 'html5lib')
#         box = len(soup.find_all('td', 'grid-table__td'))
#         for i in range(box):
#             if soup.find_all('td', 'grid-table__td')[i].get_text().strip() == 'GG/NG':
#                 index = i
#                 break

#         # Activate GGNG
#         if index > -1:
#             Browser.find_elements(
#                 By.CLASS_NAME, 'grid-table__td')[index].click()

#             # Wait 5 seconds
#             sleep(5)

#             # Scroll the page
#             height = int(Browser.execute_script(
#                 'return document.body.scrollHeight'))
#             for i in range(1, height, 10):
#                 Browser.execute_script("window.scrollTo(0, {});".format(i))

#             # Wait 5 seconds
#             sleep(5)

#             # Parse HtmlDoc
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             elem = soup.select('.sports-table > .table-f')

#             for each in elem:
#                 # Compile
#                 info = {}
#                 home_team = each.find(
#                     'div', 'sports-table__home').get_text().strip()
#                 away_team = each.find(
#                     'div', 'sports-table__away').get_text().strip()

#                 info['category'] = e
#                 info['match'] = home_team + ' vs ' + away_team
#                 info['time'] = each.find('span').get_text().strip()
#                 info['GG'] = each.find_all(
#                     'li', 'sports-table__odds-item')[0].get_text().strip() or 0
#                 info['NG'] = each.find_all(
#                     'li', 'sports-table__odds-item')[1].get_text().strip() or 0

#                 # Upload
#                 odds.append(info)
#         else:
#             pass
#         continue

#     with open('./Bet9ja/bet9ja_GGNG.txt', 'w') as outfile:
#         json.dump(odds, outfile, indent=4)
#     Browser.quit()


# # Double Chance and Single Chance
# def DS_chance():
#     # Odds
#     s_odds = []
#     d_odds = []

#     # fetch links
#     with open('./Bet9ja/bet9ja_links.txt', 'r') as json_file:
#         global data
#         data = json.load(json_file)

#     for e in data:
#         # Initiate Browser
#         Browser.get(data[e])

#         # Wait 5 seconds
#         sleep(5)

#         # Scroll the page
#         height = int(Browser.execute_script(
#             'return document.body.scrollHeight'))
#         for i in range(1, height, 10):
#             Browser.execute_script("window.scrollTo(0, {});".format(i))

#         # # Wait 5 seconds
#         sleep(5)

#         # Parse HtmlDoc
#         soup = BeautifulSoup(Browser.page_source, "html5lib")
#         elem = soup.select('.sports-table > .table-f')

#         for each in elem:
#             # Compile
#             info_1 = {}
#             info_2 = {}
#             home_team = each.find(
#                 'div', 'sports-table__home').get_text().strip()
#             away_team = each.find(
#                 'div', 'sports-table__away').get_text().strip()

#             info_1['category'] = e
#             info_2['category'] = e
#             info_1['match'] = home_team + ' vs ' + away_team
#             info_2['match'] = home_team + ' vs ' + away_team
#             info_1['time'] = each.find('span').get_text().strip()
#             info_2['time'] = each.find('span').get_text().strip()
#             info_1['home'] = each.find_all(
#                 'li', 'sports-table__odds-item')[0].get_text().strip() or 0
#             info_1['away'] = each.find_all(
#                 'li', 'sports-table__odds-item')[2].get_text().strip() or 0
#             info_2['1X'] = each.find_all(
#                 'li', 'sports-table__odds-item')[3].get_text().strip() or 0
#             info_2['2X'] = each.find_all(
#                 'li', 'sports-table__odds-item')[5].get_text().strip() or 0

#             # Upload
#             s_odds.append(info_1)
#             d_odds.append(info_2)

#     with open('./Bet9ja/bet9ja_Single.txt', 'w') as outfile:
#         json.dump(s_odds, outfile, indent=4)

#     with open('./Bet9ja/bet9ja_Double.txt', 'w') as outfile:
#         json.dump(d_odds, outfile, indent=4)
#     Browser.quit()

# ======================================================================================
#                                  BetKing Odds
# ======================================================================================

# # GGNG
# def GGNG():
#     # Odds
#     odds = {}

#     # fetch links
#     with open('./../Betking/betking_menu.txt', 'r') as json_file:
#         global data
#         data = json.load(json_file)

#     # Initiate Browser
#     Browser.get(betking)

#     # Activate Menu
#     Browser.find_element(By.XPATH,
#                          '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

#     # Wait 5 seconds
#     time.sleep(5)

#     for e in data:

#         # Index
#         l = data[e]['location']

#         if l > 0:
#             # Activate Submenu
#             Browser.find_element(By.XPATH,
#                                  '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()

#             # Wait 10 seconds
#             time.sleep(10)

#             # Parse HtmlDoc
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             ln = len(soup.find_all('div', 'eventContainer'))

#             # Loop & Click
#             for ch in range(ln):
#                 soup = BeautifulSoup(Browser.page_source, "html5lib")
#                 obj = soup.select('.eventContainer')[
#                     ch].select('.regionAreaContainer > .area')
#                 for div in obj:
#                     if div.find('div').get_text() == 'GG/NG':
#                         GG_NG = Browser.find_element(By.CSS_SELECTOR,
#                                                      '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
#                         Browser.execute_script("arguments[0].click();", GG_NG)
#                         break

#             # Wait 5 seconds
#             time.sleep(5)

#             # Re--
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             elem = soup.find_all('tr', 'trOddsSection')

#             # Line
#             olympics = []

#             for each in elem:
#                 # Compile
#                 info = {}
#                 match = each.find(
#                     'td', 'matchName')['data-matchname'].strip()
#                 matchTm = each.find(
#                     'td', 'eventDate').get_text().strip()
#                 g_odds = each.find_all('div', 'oddBorder')
#                 info['match'] = match
#                 info['time'] = matchTm
#                 info['GG'] = g_odds[0].get_text().strip() or 0
#                 info['NG'] = g_odds[1].get_text().strip() or 0

#                 # Upload
#                 olympics.append(info)
#             odds[e] = olympics

#             # Deactivate Submenu
#             Browser.find_element(By.XPATH,
#                                  '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()
#             Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

#             # Wait 5 seconds
#             time.sleep(5)
#         else:
#             pass

#     with open('./../Betking/betking_GGNG.txt', 'w') as outfile:
#         json.dump(odds, outfile, indent=4)
#     Browser.quit()


# # DNB
# def DNB():
#     # Odds
#     odds = {}

#     # fetch links
#     with open('./../Betking/betking_menu.txt', 'r') as json_file:
#         global data
#         data = json.load(json_file)

#     # Initiate Browser
#     Browser.get(betking)

#     # Activate Menu
#     Browser.find_element(By.XPATH,
#                          '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[1]').click()

#     # Wait 5 seconds
#     time.sleep(5)

#     for e in data:

#         # Index
#         l = data[e]['location']

#         if l > 0:
#             # Activate Submenu
#             Browser.find_element(By.XPATH,
#                                  '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()

#             # Wait 10 seconds
#             time.sleep(10)

#             # Parse HtmlDoc
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             ln = len(soup.find_all('div', 'eventContainer'))

#             # Loop & Click
#             for ch in range(ln):
#                 soup = BeautifulSoup(Browser.page_source, "html5lib")
#                 obj = soup.select('.eventContainer')[
#                     ch].select('.regionAreaContainer > .area')
#                 for div in obj:
#                     if div.find('div').get_text() == 'DNB':
#                         DNB = Browser.find_element(By.CSS_SELECTOR,
#                                                    '.eventContainer-' + str(ch) + ' .regionAreaContainer .area:nth-child(' + str(obj.index(div) + 1) + ')')
#                         Browser.execute_script("arguments[0].click();", DNB)
#                         break

#             # Wait 5 seconds
#             time.sleep(5)

#             # Re--
#             soup = BeautifulSoup(Browser.page_source, "html5lib")
#             elem = soup.find_all('tr', 'trOddsSection')

#             # Line
#             olympics = []

#             for each in elem:
#                 # Compile
#                 info = {}
#                 match = each.find(
#                     'td', 'matchName')['data-matchname'].strip()
#                 matchTm = each.find(
#                     'td', 'eventDate').get_text().strip()
#                 g_odds = each.find_all('div', 'oddBorder')
#                 info['match'] = match
#                 info['time'] = matchTm
#                 info['home'] = g_odds[0].get_text().strip() or 0
#                 info['away'] = g_odds[1].get_text().strip() or 0

#                 # Upload
#                 olympics.append(info)
#             odds[e] = olympics

#             # Deactivate Submenu
#             Browser.find_element(By.XPATH,
#                                  '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[2]/ul/abn-tree[2]/ul/li[' + str(l + 2) + ']/a/i[2]').click()
#             Browser.find_element(By.CLASS_NAME, 'level-2')[l].click()

#             # Wait 5 seconds
#             time.sleep(5)
#         else:
#             pass

#     with open('./../Betking/betking_DNB.txt', 'w') as outfile:
#         json.dump(odds, outfile, indent=4)
#     Browser.quit()
