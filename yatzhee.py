from random import randint
from random import seed
import numpy as np

score_board = {
  "1s": -1.0,
  "2s": -1.0,
  "3s": -1.0,
  "4s": -1.0,
  "5s": -1.0,
  "6s": -1.0,
  "three_of_a_kind": -1.0,
  "four_of_a_kind": -1.0,
  "full_house": -1.0,
  "large_straight": -1.0,
  "small_straight": -1.0,
  "yahtzee": -1.0,
  "chance": -1.0
}

a_turn = []

def roll_a_die():
  return(randint(1,6))

def roll_x_dice(x):
  global a_turn
  a_turn = []
  for x in range(x):
    a_turn.append(roll_a_die())
  return(a_turn)

def find_better_option(keepers,key,item):
  if key in keepers.keys():
    if item > keepers[key]:
      return True
    else:
      return False
  return True

def E_yahtzee():
  for each in a_turn:
    cnt = a_turn.count(each)
    key = tuple([each] * cnt) + ('yahtzee',)
    prob = (1/6)**(5-cnt)
    score = 50.0
    value = prob * score

    keepers[key] = value

def bonus_probability(current_die, instances):
    ranges = []

    for x in range(1,7):
        if (score_board[str(x)+'s'] != -1):
            ranges.append([score_board[str(x)+'s']])
        elif (score_board[str(x)+'s'] == -1) & (x == current_die):
            ranges.append([instances])
        elif (score_board[str(x)+'s'] == -1) & (x != current_die):
            ranges.append(range(0,6))
        else:
            assert 5 == 6

    numerator = 0
    for a in ranges[0]:
        for b in ranges[1]:
            for c in ranges[2]:
                for d in ranges[3]:
                    for e in ranges[4]:
                        for f in ranges[5]:
                            if np.dot([1,2,3,4,5,6],[int(a),int(b),int(c),int(d),int(e),int(f)])>=63:
                                numerator = numerator + 1

    denominator = 6**sum([len(x)>1 for x in ranges])

    return(numerator*35.0/denominator)

def E_upper(y):
  for each in a_turn:
    if each == y:
      cnt = a_turn.count(y)
      remain = 5-cnt
      key = tuple([each] * cnt) + (str(y)+'s',)

      value = 0
      cumprob = 0
      #successfully rolling more ones
      for x in range(1,remain+1):
        value = value + y * (cnt + x)/(6.0**x)
        cumprob = cumprob + 1/(6.0**x)

      #un-successfully rolling more ones
      value = value + (1-cumprob) * cnt * y

      value = value + bonus_probability(each,cnt)

      if find_better_option(keepers, key, value):
        keepers[key] = value
      break

def E_three_of_a_kind():
  for each in a_turn:
    cnt = a_turn.count(each)
    remain = 3-cnt
    key = tuple([each]*cnt) + ('three_of_a_kind',)
    value = 0

    if remain < 0:
      break
    elif remain == 0:
      value = cnt * each + 2 * 3.5
    elif remain == 1:
      value = (cnt * each + each + 2 * 3.5) / 6.0
    elif remain == 2:
      value = (cnt * each + each + each + 2 * 3.5) / 36.0

    if find_better_option(keepers, key, value):
      keepers[key] = value

def E_four_of_a_kind():
  for each in a_turn:
    cnt = a_turn.count(each)
    remain = 4-cnt
    key = tuple([each]*cnt) + ('four_of_a_kind',)
    value = 0

    if remain < 0:
      break
    elif remain == 0:
      value = cnt * each + 1 * 3.5
    elif remain == 1:
      value = (cnt * each + each + 1 * 3.5) / 6.0
    elif remain == 2:
      value = (cnt * each + each + each + 1 * 3.5) / 36.0
    elif remain == 3:
      value = (cnt * each + each + each + each + 1 * 3.5) / 216.0

    if find_better_option(keepers, key, value):
      keepers[key] = value

def E_full_house():
    pairs = []
    for each in a_turn:
        pairs.append(a_turn.count(each))

    key = []
    if pairs.count(2) == 0 and pairs.count(3) == 0:
        value = 25/216.0
        key.append(a_turn[1])
        key.append(a_turn[2])
    elif pairs.count(2) == 2 and pairs.count(3) == 0:
        value = 25/36.0
        for x in range(0,5):
            if pairs[x] == 2:
                key.append(a_turn[x])
    elif pairs.count(2) == 0 and pairs.count(3) == 3:
        value = 25/6.0
        for x in range(0,5):
            if pairs[x] == 3:
                key.append(a_turn[x])
    elif pairs.count(2) == 4 and pairs.count(3) == 0:
        value = 25/6.0
        for x in range(0,5):
            if pairs[x] == 2:
                key.append(a_turn[x])
    elif pairs.count(2) == 2 and pairs.count(3) == 3:
        value = 25.0
        for x in range(0,5):
            if pairs[x] == 2 or pairs[x] == 3:
                key.append(a_turn[x])
    else:
        print('full house broke')

    key = tuple(key) + ('full_house',)

    if find_better_option(keepers, key, value):
      keepers[key] = value

def E_small_straight():
    target1 = [1,2,3,4]
    target2 = [2,3,4,5]
    target3 = [3,4,5,6]
    key1 = []
    key2 = []
    key3 = []

    for each in a_turn:
        if each in target1:
            target1.remove(each)
            key1.append(each)
        if each in target2:
            target2.remove(each)
            key2.append(each)

    if len(target1) <= len(target2):
        key = tuple(key1)
    else:
        key = tuple(key2)

    key = key + ('small_straight',)

    value = 30.0 / 6 ** min(len(target1),len(target2))

    if find_better_option(keepers, key, value):
      keepers[key] = value

def E_large_straight():
    target = [1,2,3,4,5]
    key = []

    for each in a_turn:
        if each in target:
            target.remove(each)
            key.append(each)

    key = tuple(key) + ('large_straight',)
    value = 40.0 / 6 ** len(target)

    if find_better_option(keepers, key, value):
      keepers[key] = value

def E_chance():
    a_turn.sort(reverse = True)
    values = []

    for x in range(0,5):
        value = sum(a_turn[:x]) + (5-x) * 3.5

        key = tuple(a_turn[:x]) + ('chance',)

        if find_better_option(keepers, key, value):
          keepers[key] = value

def run_open_expectations():
    global keepers
    keepers = {}
    if score_board['1s'] == -1.0:
        E_upper(1)
    if score_board['2s'] == -1.0:
        E_upper(2)
    if score_board['3s'] == -1.0:
        E_upper(3)
    if score_board['4s'] == -1.0:
        E_upper(4)
    if score_board['5s'] == -1.0:
        E_upper(5)
    if score_board['6s'] == -1.0:
        E_upper(6)
    if score_board['three_of_a_kind'] == -1.0:
        E_three_of_a_kind()
    if score_board['four_of_a_kind'] == -1.0:
        E_four_of_a_kind()
    if score_board['full_house'] == -1.0:
        E_full_house()
    if score_board['small_straight'] == -1.0:
        E_small_straight()
    if score_board['large_straight'] == -1.0:
        E_large_straight()
    if score_board['chance'] == -1.0:
        E_chance()

    E_yahtzee()

    sorted_keepers = sorted(keepers.items(), key=lambda x: x[1], reverse = True)
    print(sorted_keepers)

def play():
    while min(score_board.values()) == -1:
        selection = []
        selection = raw_input("Roll or Input or See Score or Log Score or BREAK\n")

        if selection == "Roll".lower():
            roll_x_dice(5)
            print(a_turn)
            run_open_expectations()

        elif selection == "Input".lower():
            global a_turn
            a_turn = [int(i) for i in list(raw_input("well what are ur dice?\n"))]
            run_open_expectations()

        elif selection.lower().strip() == "See Score".lower():
            print(score_board)

        elif selection.lower() == "Log Score".lower():
            score_board_cat = ""
            while score_board_cat not in score_board.keys():
                score_board_cat = raw_input("What Category?\n")

            score_board_score = raw_input("Score?\n")

            score_board[score_board_cat] = score_board_score
        elif selection == "BREAK":
            break
        else:
            print("WRONG")

# keep dice and Roll N dice thru menu

#

#understand that pythonic if __main__ == __main__ weird ass shit

# save the scoreboard to some flat file so can 'recover game?'

#22334 Full House Expected Value
#input should take 5 and only 5 die
#am I scoreing yatzhee's correctly?
#where to take a zero?
#fixed point scores shouldn't ask for score

play()