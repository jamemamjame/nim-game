'''
BOT OF NUM GAME

@author: Jame Phankosol
'''

import numpy as np


def get_1dim_list(game_table):
    list_1dim = []
    for set in game_table:
        for val in set:
            list_1dim.append(val[1])
    return list_1dim


def convert_to_bin(game_table):
    return [bin(x)[2:].zfill(5) for x in game_table]


def can_checkamate_with_odd1(game_table):
    # return True if [1,0,0,0,1,4]
    game_table_1dim = get_1dim_list(game_table)
    n_0 = game_table_1dim.count(0)
    n_1 = game_table_1dim.count(1)
    return len(game_table_1dim) - (n_0 + n_1) == 1


def get_nim_sum(game_table):
    game_table_bin = convert_to_bin(get_1dim_list(game_table))
    nim_sum_bin = []
    # loop each digit from left to right
    for j in range(len(game_table_bin[0])):
        # loop each set
        # for i in range(len(game_table_bin)):
        nim_sum_bin.append(sum([int(x[j]) for x in game_table_bin]) % 2)
    return int(''.join([str(x) for x in nim_sum_bin]), 2)


def get_next_game_table(game_table1):
    game_table = list(game_table1)
    # check that this turn can we go to odd1 strategy?
    if can_checkamate_with_odd1(game_table):
        winnable = True
        if get_1dim_list(game_table).count(1) % 2 == 0:
            force_val = 1
        else:
            force_val = 0
        for i in range(len(game_table)):
            for j in range(len(game_table[i])):
                if game_table[i][j][1] > 1:
                    remove_val = game_table[i][j][1] - force_val
                    game_table[i][j][1] = force_val
                    game_table[i][j][0] = game_table[i][j][0] + remove_val
                    print('Checkmate by using odd1 strategy')
                    return game_table, winnable
    # if we can't use odd1 strategy, then keep save pair of binary
    else:
        nim_sum = get_nim_sum(game_table)
        game_table_1dim = get_1dim_list(game_table)
        # if nim_sum != 0, we are on winnable state
        if nim_sum != 0 and (game_table_1dim.count(0) + game_table_1dim.count(1) != len(game_table_1dim)):
            winnable = True
            for i in range(len(game_table)):
                for j in range(len(game_table[i])):
                    cur_val = game_table[i][j][1]
                    if cur_val > 0 and game_table_1dim.count(cur_val) % 2 == 1:
                        for k in range(0, cur_val):
                            game_table[i][j][1] = k
                            if get_nim_sum(game_table) == 0:
                                print('On unbeatable environment, set item to pairs')
                                remove_val = cur_val - k
                                game_table[i][j][0] = game_table[i][j][0] + remove_val
                                return game_table, winnable
                    # try to loop remove -1 to value but cannot do nim_sum = 0, so back to original
                    game_table[i][j][1] = cur_val
            print('Strange case')
            winnable = False
            return None, winnable
        # otherwise, we are on lost state
        else:
            winnable = False
            while True:
                i_idx_set = np.random.randint(0, len(game_table))
                j_idx_set = np.random.randint(0, len(game_table[i_idx_set]))
                cur_val = game_table[i_idx_set][j_idx_set][1]
                if cur_val > 0:
                    break
            remove_val = np.random.randint(1, cur_val + 1)
            remain_val = cur_val - remove_val
            # remain_val = x1 + x2
            x1 = np.random.randint(0, remain_val + 1)
            x2 = remain_val - x1
            if x1 != 0 and x2 != 0:
                old_keed = game_table[i_idx_set][j_idx_set][0]
                game_table[i_idx_set][j_idx_set] = [remove_val, x2]
                game_table[i_idx_set].insert(j_idx_set, [old_keed, x1])
            else:
                game_table[i_idx_set][j_idx_set] = [game_table[i_idx_set][j_idx_set][0] + remove_val, remain_val]
            print('Bot cannot win, bot just random pick out')
            return game_table, winnable


def test_case(game_table):
    print(game_table)
    print(get_next_game_table(game_table))
    print('.')


def print_n_char(char, num):
    for _ in range(num):
        print(char, end='')


def display_game_table(game_table):
    for i in range(len(game_table)):
        for j in range(len(game_table[i])):
            n_ł, n_l = game_table[i][j]
            print_n_char(char=ł, num=n_ł)
            print_n_char(char=l, num=n_l)
        print()


def print_game_detail(game_table, bot_go_first):
    print('Here is beginning of game table:')
    display_game_table(game_table)
    print('First player: %s' % ('BOT' if bot_go_first else 'HUMAN'))
    print()

def can_pick_out(game_table, pick_out):
    pick_i, pick_j, pick_num = pick_out
    if (pick_i >= len(game_table)) or (pick_j + pick_num - 1 >= sum([sum(x) for x in game_table[pick_i]])):
        return False
    # make the sub set to 1d array
    lines = []
    for sub_set in game_table[pick_i]:
        lines += [0] * sub_set[0]
        lines += [1] * sub_set[1]
    if 0 not in lines[pick_j: (pick_j + pick_num)]:
        return True
    else:
        return False

def get_new_game_table_after_pick_out(game_table, pick_out):
    '''
    This function return game_table which easier understand
    :param game_table:
    :param pick_out:
    :return:
    '''
    pick_i, pick_j, pick_num = pick_out

    # make the sub set to 1d array
    lines = []
    for sub_set in game_table[pick_i]:
        lines += [0] * sub_set[0]
        lines += [1] * sub_set[1]

    # set pick out from array
    for i in range(pick_j, (pick_j + pick_num)):
        lines[i] = 0

    tmp_list = []
    i = 0
    while i < len(lines):
        sum_0, sum_1 = 0, 0
        while i < len(lines):
            if lines[i] == 0:
                sum_0 += 1
                i += 1
            else:
                break
        while i < len(lines):
            if lines[i] == 1:
                sum_1 += 1
                i += 1
            else:
                break
        tmp_list.append([sum_0, sum_1])

    game_table[pick_i] = tmp_list
    return game_table


def is_endgame(game_table):
    return sum(get_1dim_list(game_table)) == 0


# ===========================================================
l, ł = '\033[36ml\033[0m', '\033[37mł\033[0m'
# game_table = [
#     [[0, 1]],
#     [[0, 3]],
#     [[0, 6]],
#     [[0, 7]]
# ]
# game_table, winnable = get_next_game_table(game_table)
# print(game_table)
# display_game_table(game_table)
# get_new_game_table([[[1, 2]], [[0, 5]], [[0, 7]]], [2, 3, 2])

if __name__ == '__main__':
    # set game beginning
    BEGIN_TABLE = [30, 15, 27]
    BOT_GO_FIRST = True

    # set game_table to correct format
    game_table = [[[0, BEGIN_TABLE[i]]] for i in range(len(BEGIN_TABLE))]

    # print detail of game
    print_game_detail(game_table, BOT_GO_FIRST)

    # ensure for ready to play
    while True:
        print('Are you ready (y/n)?')
        is_ready = input()
        if is_ready == 'y':
            break
        elif is_ready == 'n':
            exit(0)
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')

    is_bot_turn = BOT_GO_FIRST
    while True:
        # check game end
        if is_endgame(game_table):
            print('\033[33m~ GAME END: %s WIN! ~\033[0m' % ('BOT' if is_bot_turn else 'YOU'))
            break

        print('[ %s TURN ]' % ('BOT' if is_bot_turn else 'YOUR'))
        if is_bot_turn:
            game_table, winnable = get_next_game_table(game_table)
            bot_state = 'Always win' if winnable else 'Maybe lose'
            print('BOT_STATE: %s' % bot_state)
            display_game_table(game_table)
        if not is_bot_turn:
            # loop for get input from user
            while True:
                print('Enter format of pick out:')
                pick_out = input().strip()
                pick_out = [x for x in pick_out.split()]
                if sum([1 for x in pick_out if x.isnumeric()]) == 3:
                    pick_out = [int(x) for x in pick_out]
                    if sum([1 for x in pick_out if x > 0]) == 3:
                        pick_out[0] -= 1
                        pick_out[1] -= 1
                        if can_pick_out(game_table, pick_out):
                            break
                        else:
                            print('Position that you want to move is not correct')
                else:
                    print('Please enter 3 positive integer with split by black space')
            game_table = get_new_game_table_after_pick_out(game_table, pick_out)
            display_game_table(game_table)
        is_bot_turn = not is_bot_turn
        print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
