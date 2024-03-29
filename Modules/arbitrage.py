# Dependencies
# ===============================================================================================
import json
import re
from difflib import SequenceMatcher

# Globals
# ===============================================================================================
# Get file
with open('C:/Software Development/Arbitrage/Bet9ja/data.txt', 'r') as json_file_1:
    global bet9ja
    bet9ja = json.load(json_file_1)

with open('C:/Software Development/Arbitrage/Betking/data.txt', 'r') as json_file_2:
    global betking
    betking = json.load(json_file_2)

global keys
global data_1
global data_2
global data_3
global result

# Variables
# ===============================================================================================
keys = []
data_1 = {}
data_2 = {}
data_3 = {}
result = {}

# Function
# ===============================================================================================
# Checker


def Compile(all=False, category=None):
    if all:
        for a in bet9ja.keys():
            for e in bet9ja[a]:
                for g in bet9ja[a][e]:
                    bet9ja[a][e][g]["category"] = a
                    bet9ja[a][e][g]["sub-category"] = e
                    data_1[g] = bet9ja[a][e][g]

        for c in bet9ja.keys():
            for e in betking[c]:
                for g in betking[c][e]:
                    betking[c][e][g]["category"] = c
                    betking[c][e][g]["sub-category"] = e.replace(
                        c[0:3].upper() + " - ", "")
                    data_2[g] = betking[c][e][g]
    else:
        for e in bet9ja[category]:
            for g in bet9ja[category][e]:
                bet9ja[category][e][g]["category"] = category
                bet9ja[category][e][g]["sub-category"] = e
                data_1[g] = bet9ja[category][e][g]

        for e in betking[category]:
            for g in betking[category][e]:
                betking[category][e][g]["category"] = category
                betking[category][e][g]["sub-category"] = e.replace(
                    category[0:3].upper() + " - ", "")
                data_2[g] = betking[category][e][g]


# Pair Up
def pair_up():
    # Loop and Check
    for e in data_1.keys():
        for f in data_2.keys():
            if SequenceMatcher(a=e, b=f).ratio() > 0.7:
                if data_1[e]["time"] == data_2[f]["time"] and SequenceMatcher(a=data_1[e]["sub-category"], b=data_2[f]["sub-category"]).ratio() > 0.7:
                    data_3[e] = {
                        "bet9ja": data_1[e],
                        "betking": data_2[f]
                    }

                break
            else:
                continue


# Calculate Possibilities
# ===========================================================================================================================

# 3-Way Arbitrage Calculator
def Arbitrage_3(total_stake):
    for e in data_3:
        # Bet9ja
        bet9ja_SH = float(data_3[e]["bet9ja"]["single"]["home"])
        bet9ja_SA = float(data_3[e]["bet9ja"]["single"]["away"])
        bet9ja_SD = float(data_3[e]["bet9ja"]["single"]["draw"])
        bet9ja_2H1 = float(data_3[e]["bet9ja"]["handicap"]["2 [Home + 1]"])
        bet9ja_1A1 = float(data_3[e]["bet9ja"]["handicap"]["1 [Away + 1]"])

        # Betking
        betking_SH = float(data_3[e]["betking"]["single"]["home"])
        betking_SA = float(data_3[e]["betking"]["single"]["away"])
        betking_SD = float(data_3[e]["betking"]["single"]["draw"])
        betking_2H1 = float(data_3[e]["betking"]["handicap"]["2 [Home + 1]"])
        betking_1A1 = float(data_3[e]["betking"]["handicap"]["1 [Away + 1]"])

        # Check bet9ja single home is greater than bet9ja single away
        if bet9ja_SH > bet9ja_SA:
            # if true, check is its greater than 3.00
            if bet9ja_SH >= 3.00:
                # if true, check if its greater than betking's offer
                if bet9ja_SH > betking_SH:
                    # If true, Use bet9ja home value
                    # Compare bet9ja home advantage, away win odd and betking home advantage, away win
                    if bet9ja_2H1 > betking_2H1:
                        # if true, use bet9ja "2 [Home + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / bet9ja_SH) + (1 / bet9ja_2H1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Home": {
                                        "odd": bet9ja_SH,
                                        "stake": total_stake / (1 + (bet9ja_SH / bet9ja_2H1) + (bet9ja_SH / bet9ja_SD))
                                    },
                                    "bet9ja 2 [Home + 1]": {
                                        "odd":  bet9ja_2H1,
                                        "stake": total_stake / (1 + (bet9ja_2H1 / bet9ja_SH) + (bet9ja_2H1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd":  bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / bet9ja_SH) + (1 / bet9ja_2H1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Home": {
                                        "odd": bet9ja_SH,
                                        "stake": total_stake / (1 + (bet9ja_SH / bet9ja_2H1) + (bet9ja_SH / bet9ja_SD))
                                    },
                                    "bet9ja 2 [Home + 1]": {
                                        "odd":  bet9ja_2H1,
                                        "stake": total_stake / (1 + (bet9ja_2H1 / bet9ja_SH) + (bet9ja_2H1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd":  betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                    else:
                        # Use betking "2 [Home + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / bet9ja_SH) + (1 / betking_2H1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Home": {
                                        "odd": bet9ja_SH,
                                        "stake": total_stake / (1 + (bet9ja_SH / bet9ja_2H1) + (bet9ja_SH / bet9ja_SD))
                                    },
                                    "betking 2 [Home + 1]": {
                                        "odd":  betking_2H1,
                                        "stake": total_stake / (1 + (betking_2H1 / bet9ja_SH) + (betking_2H1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd":  bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / bet9ja_SH) + (1 / betking_2H1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Home": {
                                        "odd": bet9ja_SH,
                                        "stake": total_stake / (1 + (bet9ja_SH / bet9ja_2H1) + (bet9ja_SH / bet9ja_SD))
                                    },
                                    "betking 2 [Home + 1]": {
                                        "odd":  betking_2H1,
                                        "stake": total_stake / (1 + (betking_2H1 / bet9ja_SH) + (betking_2H1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd":  betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                else:
                    # If true, Use betking home value
                    # Compare bet9ja home advantage, away win odd and betking home advantage, away win
                    if bet9ja_2H1 > betking_2H1:
                        # if true, use bet9ja "2 [Home + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / betking_SH) + (1 / bet9ja_2H1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "betking Home": {
                                        "odd": betking_SH,
                                        "stake": total_stake / (1 + (betking_SH / bet9ja_2H1) + (betking_SH / bet9ja_SD))
                                    },
                                    "bet9ja 2 [Home + 1]": {
                                        "odd":  bet9ja_2H1,
                                        "stake": total_stake / (1 + (bet9ja_2H1 / bet9ja_SH) + (bet9ja_2H1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd":  bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / betking_SH) + (1 / bet9ja_2H1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "betking Home": {
                                        "odd": betking_SH,
                                        "stake": total_stake / (1 + (betking_SH / bet9ja_2H1) + (betking_SH / bet9ja_SD))
                                    },
                                    "bet9ja 2 [Home + 1]": {
                                        "odd":  bet9ja_2H1,
                                        "stake": total_stake / (1 + (bet9ja_2H1 / bet9ja_SH) + (bet9ja_2H1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd":  betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                    else:
                        # Use betking "2 [Home + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / betking_SH) + (1 / betking_2H1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "betking Home": {
                                        "odd": betking_SH,
                                        "stake": total_stake / (1 + (betking_SH / bet9ja_2H1) + (betking_SH / bet9ja_SD))
                                    },
                                    "betking 2 [Home + 1]": {
                                        "odd":  betking_2H1,
                                        "stake": total_stake / (1 + (betking_2H1 / bet9ja_SH) + (betking_2H1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd":  bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_2H1) + (bet9ja_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / betking_SH) + (1 / betking_2H1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "betking Home": {
                                        "odd": betking_SH,
                                        "stake": total_stake / (1 + (betking_SH / bet9ja_2H1) + (betking_SH / bet9ja_SD))
                                    },
                                    "betking 2 [Home + 1]": {
                                        "odd":  betking_2H1,
                                        "stake": total_stake / (1 + (betking_2H1 / bet9ja_SH) + (betking_2H1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd":  betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_2H1) + (betking_SD / bet9ja_SH)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
            else:
                continue
        else:
            # Use bet9ja single away
            # check if its greater than 3.00
            if bet9ja_SA >= 3.00:
                # if true, check if its greater than betking's offer
                if bet9ja_SA > betking_SA:
                    # If true, Use bet9ja away value
                    # Compare bet9ja away advantage, home win odd and betking away advantage, home win
                    if bet9ja_1A1 > betking_1A1:
                        # if true, use bet9ja "1 [Away + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / bet9ja_SA) + (1 / bet9ja_1A1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Away": {
                                        "odd":  bet9ja_SA,
                                        "stake": total_stake / (1 + (bet9ja_SA / bet9ja_1A1) + (bet9ja_SA / bet9ja_SD))
                                    },
                                    "bet9ja 1 [Away + 1]": {
                                        "odd":  bet9ja_1A1,
                                        "stake": total_stake / (1 + (bet9ja_1A1 / bet9ja_SA) + (bet9ja_1A1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd": bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / bet9ja_SA) + (1 / bet9ja_1A1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Away": {
                                        "odd":  bet9ja_SA,
                                        "stake": total_stake / (1 + (bet9ja_SA / bet9ja_1A1) + (bet9ja_SA / bet9ja_SD))
                                    },
                                    "bet9ja 1 [Away + 1]": {
                                        "odd":  bet9ja_1A1,
                                        "stake": total_stake / (1 + (bet9ja_1A1 / bet9ja_SA) + (bet9ja_1A1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd": betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                    else:
                        # Use betking "1 [Away + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / bet9ja_SA) + (1 / betking_1A1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Away": {
                                        "odd":  bet9ja_SA,
                                        "stake": total_stake / (1 + (bet9ja_SA / bet9ja_1A1) + (bet9ja_SA / bet9ja_SD))
                                    },
                                    "betking 1 [Away + 1]": {
                                        "odd":  betking_1A1,
                                        "stake": total_stake / (1 + (betking_1A1 / bet9ja_SA) + (betking_1A1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd": bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / bet9ja_SA) + (1 / betking_1A1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "bet9ja Away": {
                                        "odd":  bet9ja_SA,
                                        "stake": total_stake / (1 + (bet9ja_SA / bet9ja_1A1) + (bet9ja_SA / bet9ja_SD))
                                    },
                                    "betking 1 [Away + 1]": {
                                        "odd":  betking_1A1,
                                        "stake": total_stake / (1 + (betking_1A1 / bet9ja_SA) + (betking_1A1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd": betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                else:
                    # If true, Use betking away value
                    # Compare bet9ja away advantage, home win odd and betking away advantage, home win
                    if bet9ja_1A1 > betking_1A1:
                        # if true, use bet9ja "1 [Away + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / betking_SA) + (1 / bet9ja_1A1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "betking Away": {
                                        "odd":  betking_SA,
                                        "stake": total_stake / (1 + (betking_SA / bet9ja_1A1) + (betking_SA / bet9ja_SD))
                                    },
                                    "bet9ja 1 [Away + 1]": {
                                        "odd":  bet9ja_1A1,
                                        "stake": total_stake / (1 + (bet9ja_1A1 / bet9ja_SA) + (bet9ja_1A1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd": bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / betking_SA) + (1 / bet9ja_1A1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "betking Away": {
                                        "odd":  betking_SA,
                                        "stake": total_stake / (1 + (betking_SA / bet9ja_1A1) + (betking_SA / bet9ja_SD))
                                    },
                                    "bet9ja 1 [Away + 1]": {
                                        "odd":  bet9ja_1A1,
                                        "stake": total_stake / (1 + (bet9ja_1A1 / bet9ja_SA) + (bet9ja_1A1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd": betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                    else:
                        # Use betking "1 [Away + 1]" offer
                        # Compare Draws
                        if bet9ja_SD > betking_SD:
                            # Use bet9ja draw offer
                            # Calculate
                            if (1 / betking_SA) + (1 / betking_1A1) + (1 / bet9ja_SD) < 1:
                                # Update
                                _data = {
                                    "betking Away": {
                                        "odd":  betking_SA,
                                        "stake": total_stake / (1 + (betking_SA / bet9ja_1A1) + (betking_SA / bet9ja_SD))
                                    },
                                    "betking 1 [Away + 1]": {
                                        "odd":  betking_1A1,
                                        "stake": total_stake / (1 + (betking_1A1 / bet9ja_SA) + (betking_1A1 / bet9ja_SD))
                                    },
                                    "bet9ja Draw": {
                                        "odd": bet9ja_SD,
                                        "stake": total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (bet9ja_SD * (total_stake / (1 + (bet9ja_SD / bet9ja_1A1) + (bet9ja_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
                        else:
                            # Use betking draw offer
                            # Calculate
                            if (1 / betking_SA) + (1 / betking_1A1) + (1 / betking_SD) < 1:
                                # Update
                                _data = {
                                    "betking Away": {
                                        "odd":  betking_SA,
                                        "stake": total_stake / (1 + (betking_SA / bet9ja_1A1) + (betking_SA / bet9ja_SD))
                                    },
                                    "betking 1 [Away + 1]": {
                                        "odd":  betking_1A1,
                                        "stake": total_stake / (1 + (betking_1A1 / bet9ja_SA) + (betking_1A1 / bet9ja_SD))
                                    },
                                    "betking Draw": {
                                        "odd": betking_SD,
                                        "stake": total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA))
                                    },
                                    # "amount": total_stake,
                                    # "profit": (betking_SD * (total_stake / (1 + (betking_SD / bet9ja_1A1) + (betking_SD / bet9ja_SA)))) - total_stake
                                }

                                result[e] = {
                                    "category": data_3[e]["bet9ja"]["category"],
                                    "sub-category": data_3[e]["bet9ja"]["sub-category"],
                                    "date": data_3[e]["bet9ja"]["date"],
                                    "time": data_3[e]["bet9ja"]["time"],
                                    "3-way": _data
                                }
                            else:
                                continue
            else:
                continue

    # Save as JSON
    with open('./arb3.txt', 'w') as outfile:
        json.dump(result, outfile, indent=4)


# 2-Way Arbitrage Calculator
def Arbitrage_2(total_stake):
    for e in data_3:
        # Bet9ja
        bet9ja_SH = float(data_3[e]["bet9ja"]["single"]["home"])
        bet9ja_SA = float(data_3[e]["bet9ja"]["single"]["away"])
        bet9ja_SD = float(data_3[e]["bet9ja"]["single"]["draw"])
        bet9ja_1X = float(data_3[e]["bet9ja"]["double"]["1X"])
        bet9ja_12 = float(data_3[e]["bet9ja"]["double"]["12"])
        bet9ja_2X = float(data_3[e]["bet9ja"]["double"]["2X"])

        # Betking
        betking_SH = float(data_3[e]["betking"]["single"]["home"])
        betking_SA = float(data_3[e]["betking"]["single"]["away"])
        betking_SD = float(data_3[e]["betking"]["single"]["draw"])
        betking_1X = float(data_3[e]["betking"]["double"]["1X"])
        betking_12 = float(data_3[e]["betking"]["double"]["12"])
        betking_2X = float(data_3[e]["betking"]["double"]["2X"])

        if (1 / bet9ja_1X) + (1 / betking_2X) < 1:
            # Update
            data_3[e]["2-way"] = {
                "bet9ja 1X": {
                    "odd":  bet9ja_1X,
                    "stake": total_stake / (1 + (bet9ja_1X / betking_2X))
                },
                "betking 2X": {
                    "odd": betking_2X,
                    "stake": total_stake / (1 + (betking_2X / bet9ja_1X))
                },
                # "amount": total_stake,
                # "profit": (bet9ja_1X * (total_stake / (1 + (bet9ja_1X / betking_2X)))) - total_stake
            }
            result[e] = data_3[e]
        else:
            continue

        if (1 / bet9ja_2X) + (1 / betking_1X) < 1:
            # Update
            data_3[e]["2-way"] = {
                "bet9ja 2X": {
                    "odd":  bet9ja_2X,
                    "stake": total_stake / (1 + (bet9ja_2X / betking_1X))
                },
                "betking 1X": {
                    "odd": betking_1X,
                    "stake": total_stake / (1 + (betking_1X / bet9ja_2X))
                },
                # "amount": total_stake,
                # "profit": (bet9ja_2X * (total_stake / (1 + (bet9ja_2X / betking_1X)))) - total_stake
            }
            result[e] = data_3[e]
        else:
            continue

    # Save as JSON
    with open('./arb2.txt', 'w') as outfile:
        json.dump(result, outfile, indent=4)
