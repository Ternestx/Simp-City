# Ernest Toh S10221816B P09 #

import random

# functions #

# game rules #
def show_game_rules():
    print()
    print("Game Rules:")
    print("This city-building strategy game is played over 16 turns.")
    print()
    print("In each turn, you will build one of two randomly-selected buildings in your 4x4 city.")
    print()
    print("In the first turn, you can build anywhere in the city.")
    print()
    print("In subsequent turns, you can only build on squares that are connected to existing buildings. The other building that you did not build is discarded.")
    print()
    print("There are 5 types of buildings, with 8 copies of each:")
    print()
    print("* Beach (BCH): Scores 3 points if it is built on the left or right side of the city, or 1 point otherwise.")
    print("* Factory (FAC): Scores 1 point per factory (FAC) in the city, up to a maximum of 4 points for the first 4 factories. All subsequent factories only score 1 point each.")
    print("* House (HSE): If it is next to a factory (FAC), then it scores 1 point only. Otherwise, it scores 1 point for each adjacent house (HSE) or shop (SHP), and 2 points for each adjacent beach (BCH).")
    print("* Shop (SHP): Scores 1 point per different type of building adjacent to it.")
    print("* Highway (HWY): Scores 1 point per connected highway (HWY) in the same row.")
    print("* Monument (MON): Scores 1 point if it is not built on a corner square (i.e., A1, A4, D1 or D4). 2 points if built on a corner square. If there are at least 3 monuments that are built on corner squares, all monuments score 4 points each (including those that are not built on corner squares)")
    print()
          
# convert letter number pair to corresponding grid square #
def convert(location):

    # check validity #
    valid = False
    valid_letters = ["A", "B", "C", "D"]
    if len(location) == 2:
        if location[0].isalpha() == True and location[1].isdigit() == True:
            if location[0].upper() in valid_letters:
                if int(location[1]) > 0 and int(location[1]) < 5:
                    valid = True

    # convert letter-num pair to board index #
    if valid: 
        num = int(location[1]) - 1
        if location[0].upper() == "A":
            return str(num) + "0"
        elif location[0].upper() == "B":
            return str(num) + "1"
        elif location[0].upper() == "C":
            return str(num) + "2"
        else:
            return str(num) + "3"
    else:
        new_input = input("Please input a valid alphabet and number pair. ")
        return convert(new_input)

# calculate score based on building and location #
def calculate_score(board):
    
    # dictionary to keep track of buildings and score #
    scores = {"BCH" : [], "FAC" : [], "HSE" : [], "SHP" : [], "HWY" : [], "MON" : []}
    
    countFAC = 0
    countMON_corner = 0
    countMON_non_corner = 0
    for x in range(4):
        countHWY = 0
        for y in range(4):
            current_building = board[x][y]

            if current_building != "HWY":
                for z in range(countHWY):
                    scores["HWY"].append(countHWY)
                countHWY = 0
            
            # BCH #
            if current_building == "BCH":
                if y == 0 or y == 3:
                    scores["BCH"].append(3)
                else:
                    scores["BCH"].append(1)

            # FAC #
            elif current_building == "FAC":
                countFAC += 1

            # HSE #
            elif current_building == "HSE":
                count = {"BCH" : 0, "FAC" : 0, "HSE" : 0, "SHP" : 0, "HWY" : 0, "MON" : 0}
                score = {"BCH" : 2, "FAC" : 0, "HSE" : 1, "SHP" : 1, "HWY" : 0, "MON" : 1}
                # up, x-1 #
                if x-1 >= 0 and board[x-1][y] != "   ":
                    count[board[x-1][y]] += 1
                # down, x+1 #
                if x+1 <= 3 and board[x+1][y] != "   ":
                    count[board[x+1][y]] += 1
                # left, y-1 #
                if y-1 >= 0 and board[x][y-1] != "   ":
                    count[board[x][y-1]] += 1
                # right, y+1 #
                if y+1 <= 3 and board[x][y+1] != "   ":
                    count[board[x][y+1]] += 1
                # calculate scores #
                total = 0
                # consider special case of FAC #
                if count["FAC"] > 0:
                    total = 1
                else:
                    for key, value in count.items():
                        total += score[key] * value
                scores["HSE"].append(total)

            # SHP #
            elif current_building == "SHP":
                buildings = []
                # up, x-1 #
                if x-1 >= 0 and board[x-1][y] != "   ":
                    if board[x-1][y] not in buildings:
                        buildings.append(board[x-1][y])
                # down, x+1 #
                if x+1 <= 3 and board[x+1][y] != "   ":
                    if board[x+1][y] not in buildings:
                        buildings.append(board[x+1][y])
                # left, y-1 #
                if y-1 >= 0 and board[x][y-1] != "   ":
                    if board[x][y-1] not in buildings:
                        buildings.append(board[x][y-1])
                # right, y+1 #
                if y+1 <= 3 and board[x][y+1] != "   ":
                    if board[x][y+1] not in buildings:
                        buildings.append(board[x][y+1])
                scores["SHP"].append(len(buildings))

            # HWY #
            elif current_building == "HWY":
                countHWY += 1
                if y == 3:
                    for z in range(countHWY):
                        scores["HWY"].append(countHWY)

            # MON #
            elif current_building == "MON":
                # check for corner square #
                corner_squares = ["00", "03", "30", "33"]
                current_square = str(x) + str(y)
                if current_square in corner_squares:
                    countMON_corner += 1
                else:
                    countMON_non_corner += 1

            # blank space #
            else: 
                continue

    # FAC continued #
    if countFAC <= 4:
        for num in range(countFAC):
            scores["FAC"].append(countFAC)
    else:
        for num1 in range(4):
            scores["FAC"].append(4)
        for num2 in range(countFAC - 4):
            scores["FAC"].append(1)

    # MON continued #
    if countMON_corner >= 3:
        countMON_total = countMON_corner + countMON_non_corner
        for num in range(countMON_total):
            scores["MON"].append(4)
    else:
        for num1 in range(countMON_corner):
            scores["MON"].append(2)
        for num2 in range(countMON_non_corner):
            scores["MON"].append(1)

    return scores

# print remaining buildings #
def see_remaining_buildings(buildings):
    print()
    print("Building        Remaining")
    print("--------        ---------")
    for name, count in buildings.items():
        print(name + "             " + str(count))

# print current score #
def see_current_score(current_score):
    print()
    total = 0
    for name, scores in current_score.items():
        subtotal = sum(scores)
        length = len(scores)
        total += subtotal
        print(name + ": ", end = "")
        for i in range(length):
            print(str(scores[i]) + " ", end = "")
            if i < length - 1:
                print("+ ", end = "")
            else:
                print("= ", end = "")
        print(subtotal)
    print("Total score: " + str(total))
    return total
    
# build a building #
def build_a_building(location, board, buildings, building1, building2, option):
    
    # check for location validity #
    location = convert(location)
    x = int(location[0])
    y = int(location[1])
    legal_placement = False

    global turn 
    if turn == 1:
        legal_placement = True

    else: 
    
        # 1. check if selected location is empty #
        if board[x][y] == "   ":
            # 2. check for orthogonally adjacent locations #
            # up, x-1 #
            if x-1 >= 0 and board[x-1][y] != "   ":
                legal_placement = True
            # down, x+1 #
            elif x+1 <= 3 and board[x+1][y] != "   ":
                legal_placement = True
            # left, y-1 #
            elif y-1 >= 0 and board[x][y-1] != "   ":
                legal_placement = True
            # right, y+1 #
            elif y+1 <= 3 and board[x][y+1] != "   ":
                legal_placement = True
            else:
                print("You must build next to an existing building.")

        else:
            print("You must build on an empty plot of land.")
                    
    # if placement is legal,
    # add new building, update building count and update turn count #
    global keep
    if legal_placement == True:
        keep = False
        turn += 1
        buildings[building1] -= 1
        buildings[building2] -= 1
        if option == "1":
            board[x][y] = building1 
        else:
            board[x][y] = building2
    else:
        keep = True

# print main menu #
def display_main_menu():
    print("Welcome, mayor of Simp City!")
    print("----------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Show high scores")
    print("4. Show game rules")
    print()
    print("0. Exit")
    choice = input("Your choice? ")
    return choice

# print high scores #
def print_high_scores(high_scores):
    sorted_scores = sorted(high_scores.items(), key = lambda x: x[1], reverse = True)
    print()
    print("--------- HIGH SCORES ---------")
    print("Pos Player                Score")
    print("--- ------                -----")
    pos = 1
    for score in sorted_scores:
        name_length = len(score[0])
        space = " " * (25 - name_length)
        if pos != 10:
            print(" " + str(pos) + ". " + score[0] + space + str(score[1]))
        else:
            print(str(pos) + ". " + score[0] + space + str(score[1]))
        pos += 1
    print("-------------------------------")
    print()

def check_for_high_score(high_scores):
    # check if player can make into high score board #
    sorted_scores = sorted(high_scores.items(), key = lambda x: x[1], reverse = True)
    current_score = calculate_score(board)
    player_score = see_current_score(current_score)

    # find minimum in high_scores #
    sorted_scores_asc = sorted(high_scores.items(), key = lambda x: x[1])
    if len(high_scores) != 0:
        minimum_score = sorted_scores_asc[0][1]
    
    if len(high_scores) < 10 or player_score > minimum_score:
        # check for which position to add in #
        pos = 1
        for score in sorted_scores:
            if player_score <= score[1]:
                pos += 1
        print("Congratulations! You made the high score board at position " + str(pos) + "!")
        name = input("Please enter your name (max 20 chars): ")
        if len(high_scores) < 10:
            high_scores[name] = player_score
        elif player_score > minimum_score:
            player_to_delete = sorted_scores_asc[0][0]
            del high_scores[player_to_delete]
            high_scores[name] = player_score
    print_high_scores(high_scores)

# print final layout #
def print_final_layout(board):
    print()
    print("Final layout of Simp City:")
    print("    A     B     C     D   ")
    print(" +-----+-----+-----+-----+")
    for r in range(4):
        print(r + 1, end = "")
        for c in range(4):
            print("| {} ".format(board[r][c]), end = "")
        print("|")
        print(" +-----+-----+-----+-----+")

# start the game according #
def play_game(board, buildings, building1, building2):
    # player score #
    player_score = 0

    global turn 
    while turn <= 16: # max 16 turns in each game #
        # print board #
        print()
        print("Turn {}".format(turn))
        print("    A     B     C     D   ")
        print(" +-----+-----+-----+-----+")

        for r in range(4):
            print(r + 1, end = "")
            for c in range(4):
                print("| {} ".format(board[r][c]), end = "")
            print("|")
            print(" +-----+-----+-----+-----+")

        global keep 
        if keep == False:
            # randomly select 2 buildings #
            building1 = random.choice(list(buildings.keys()))
            while (buildings[building1]) <= 0:
                building1 = random.choice(list(buildings.keys()))        
        
            building2 = random.choice(list(buildings.keys()))
            if building1 != building2:
                while (buildings[building2]) <= 0:
                    building2 = random.choice(list(buildings.keys()))
            else:
                while (buildings[building2]) <= 1:
                    building2 = random.choice(list(buildings.keys()))

        print("1. Build a {}".format(building1))
        print("2. Build a {}".format(building2))

        print("3. See remaining buildings")
        print("4. See current score")
        print()
        print("5. Save game")
        print("0. Exit to main menu")

        # user to select from options 0-5 #
        option = input("Your choice? ")
        check_option_validity(option)
        game_complete = True
        
        if option == "0": # exit #
            game_complete = False
            print()
            print("Returning to main menu...")
            print()
            turn = 17
            continue

        if option == "1" or option == "2": # build #
            
            location = input("Build where? ")
            build_a_building(location, board, buildings, building1, building2, option)

                    
        elif option == "3": # show building count #
            keep = True
            
            # print output table #
            see_remaining_buildings(buildings)

        elif option == "4": # see current score #
            keep = True

            # print score #
            current_score = calculate_score(board)
            see_current_score(current_score)

        elif option == "5":
            keep = True

            # save turn number #
            datafile = open("turn.txt", "w")
            datafile.write("{}\n".format(turn))
            datafile.close()

            # save board #
            datafile = open("board.txt", "w")
            datafile.write("{}\n".format(board))
            datafile.close()

            # save buildings dictionary #
            datafile = open("buildings.txt", "w")
            datafile.write("{}\n".format(buildings))
            datafile.close()

            # save buildings 1 and 2
            datafile = open("building1.txt", "w")
            datafile.write("{}\n".format(building1))
            datafile.close()
            datafile = open("building2.txt", "w")
            datafile.write("{}\n".format(building2))
            datafile.close()

            print("Game saved successfully!")

    if game_complete:
        print_final_layout(board)
        check_for_high_score(high_scores)

    # update high score board #
    high_scores_file = open("scores.txt", "w")
    high_scores_file.write("{}\n".format(high_scores))
    high_scores_file.close()


def check_option_validity(option):
    global keep
    options = ["0", "1", "2", "3", "4", "5"]
    if option not in options:
        keep = True
        print("Please enter a valid option!")

def check_choice_validity(choice):
    choices = ["0", "1", "2", "3", "4"]
    if choice not in choices:
        print("Please enter a valid option!")
        print()
        
### START OF GAME ###
while True:                 
    # main menu #
    choice = display_main_menu()
    check_choice_validity(choice)
    
    # create empty dictionary when high score board is empty #
    # else load high score board #
    high_scores_file = open("scores.txt", "a")
    high_scores_file.write("")
    high_scores_file.close()
    high_scores_file = open("scores.txt", "r")
    high_scores = high_scores_file.readline()

    if high_scores == "":
        high_scores = {}
    else:
        high_scores = eval(high_scores)
        
    if choice == "0":
        print("Thank you for playing the game. See you next time!")
        exit()
        
    elif choice == "1": # initialise new game #
        # initialise new game, 4 x 4 board #
        board = [["   " for row in range(4)] for col in range(4)]
        
        # boolean to decide whether to regenerate buildings #
        global keep 
        keep = False
        
        # keep track of turn number #
        global turn
        turn = 1
        
        # dictionary to keep track of buildings and count #
        buildings = {"BCH" : 8, "FAC" : 8, "HSE" : 8, "SHP" : 8, "HWY" : 8, "MON" : 8}

        play_game(board, buildings, None, None)

    elif choice == "2": # load save game #
        keep = True
        try: 
            # read board file #
            board_file = open("board.txt", "r")
            board = eval(board_file.readline())

            # read turn number #
            turn_file = open("turn.txt", "r")
            turn = int(turn_file.readline())

            # read buildings dictionary #
            buildings_file = open("buildings.txt", "r")
            buildings = eval(buildings_file.readline())
            
            # read buildings 1 and 2
            building1_file = open("building1.txt", "r")
            building1 = (building1_file.readline()).strip()
            building2_file = open("building2.txt", "r")
            building2 = (building2_file.readline()).strip()

            play_game(board, buildings, building1, building2)

        except:
            print("No saved game!")
            print()

                  
    elif choice == "3": # show high scores #
        print_high_scores(high_scores)

    elif choice == "4": # show game rules #
        show_game_rules()
