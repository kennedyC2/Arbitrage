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
    f_1 = bookmarker_1 + '_' + bookmaker_1_oddType + '.txt'
    fd_1 = bookmarker_1.capitalize()
    f_2 = bookmarker_2 + '_' + bookmaker_2_oddType + '.txt'
    fd_2 = bookmarker_2.capitalize()

    # Get file
    with open('./' + fd_1 + '/' + f_1, 'r') as json_file_1:
        global data_1
        data_1 = json.load(json_file_1)

    with open('./' + fd_2 + '/' + f_2, 'r') as json_file_2:
        global data_2
        data_2 = json.load(json_file_2)

    # loop and search
    for i in data_1:
        for k in data_1[i]:
            arr_1a = data_1[i][k]['match'].split(' vs ')[0]
            arr_1b = data_1[i][k]['match'].split(' vs ')[1]
            for j in data_2:
                for l in data_2[j]:
                    arr_2a = data_2[j][l]['match'].split(' vs ')[0]
                    arr_2b = data_2[j][l]['match'].split(' vs ')[1]

                    # Find Match
                    if re.findall(arr_1a, arr_2a) or re.findall(arr_2a, arr_1a):
                        if re.findall(arr_1b, arr_2b) or re.findall(arr_2b, arr_1b):
                            data = {}
                            data[i] = data_1[i][k]
                            data[j] = data_2[j][l]

                            # Send Information
                            return data


# Calculator
