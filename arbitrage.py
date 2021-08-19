# Dependencies
# ===============================================================================================
import re
import json

# Keys
# ===============================================================================================

# Odd type
a = 'Single'
b = 'Double'
c = 'DNB'
d = 'GGNG'

# Bookmarker
u = 'Bet9ja'
v = 'Betking'
w = 'Bet365'
x = 'Betpawa'
y = 'Nairabet'
z = 'Sportybet'

# Angle
m = 1
n = 2


# Function
# ===============================================================================================

# Fetch
def fetch(bookmarker_1, bookmaker_1_oddType, bookmarker_2, bookmaker_2_oddType):
    # Define f path
    f_1 = bookmarker_1.lower() + '_' + bookmaker_1_oddType + '.txt'
    fd_1 = bookmarker_1
    f_2 = bookmarker_2.lower() + '_' + bookmaker_2_oddType + '.txt'
    fd_2 = bookmarker_2

    # Get file
    with open('./' + fd_1 + '/' + f_1, 'r') as json_file_1:
        global data_1
        data_1 = json.load(json_file_1)

    with open('./' + fd_2 + '/' + f_2, 'r') as json_file_2:
        global data_2
        data_2 = json.load(json_file_2)

    # loop and search
    for i in range(len(data_1)):
        match_1 = data_1[i]['match'].split(' vs ')
        home_team_1 = match_1[0].split(' ')
        away_team_1 = match_1[1].split(' ')
        for j in range(len(data_2)):
            match_2 = data_2[j]['match'].split(' vs ')
            home_team_2 = match_2[0].split(' ')
            away_team_2 = match_2[1].split(' ')

            # Check
            for h_team in home_team_1:
                # Compare Home teams
                if h_team in home_team_2 and len(h_team) > 2:
                    for a_team in away_team_1:
                        # Compare Away teams
                        if a_team in away_team_2 and len(a_team) > 2:
                            pair = []
                            pair.append(data_1[i])
                            pair.append(data_2[j])
                            print(pair)
                            break
                        else:
                            pass
                        continue
                else:
                    pass
                break


fetch(u, a, z, a)
