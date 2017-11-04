

gVec = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
gCol = ('A','B','C','D','E','F','G','H')
gRow = ('1','2','3','4','5','6','7','8')

def pos_str2pos_index(pos_str):
    pos_index = []
    for i, c in enumerate(gRow):
        if pos_str[1] == c:
            pos_index.append(i)

    for i, c in enumerate(gCol):
        if pos_str[0] == c:
            pos_index.append(i)


    return pos_index

def pos_str2pos_index_flat(pos_str):
    pos_index = pos_str2pos_index(pos_str)
    index = pos_index[0] * 8 + pos_index[1]
    return index


#==== Main ====#
record_X = []    # MLP input (board list)
record_y = []    # MLP output(class(0-64) list)
temp_X = []
temp_y = []
temp2_X = []
temp2_y = []
board = []
row = []

f = open("data/Othello.01e4.ggf", "r")
line_cnt = 1
for line in f:
    print('Line Count = ' + str(line_cnt))
    idx = line.find("BO[8")
    #if idx == -1:
    if line_cnt > 10:
        #continue
        break

    idx += 5
    # make board initial state
    for i in range(idx, idx+9*8):
        if line[i] == '-':
            row.append(0)
        elif line[i] == 'O':
            row.append(2)
        elif line[i] == '*':
            row.append(1)

        if (i-idx)%9 == 8:
            board.append(row)
            row = []
            if len(board) == 8:
                break

    #print(board)

    row = []
    #print_board(board)

    line_cnt += 1

    # record progress of game
    i = idx+9*8+2
    temp_y = []
    while line[i] != ';':
        if (line[i] == 'B' or line[i] == 'W') and line[i+1] == '[':
            temp_X.append(board)
            pos_str = line[i+2] + line[i+3]
            if pos_str == "pa":    # pass
                temp_y.append(64)
                # board state is not change
                #print_board(board)
            else:
                if line[i] == 'B':
                    clr = 1
                elif line[i] == 'W':
                    clr = 2
                else:
                    clr = 0
                    assert False, "Stone Color is illegal."

                pos_index_flat = pos_str2pos_index_flat(pos_str)
                temp_y.append(pos_index_flat)
                #board = update_board(board, pos_str, clr)

        i += 1

    print(temp_y)
    print(len(temp_y))
    temp_y = []

    """
            if (line[i] == 'B' and (build_type == 'black' or build_type == 'black_win')) or \
               (line[i] == 'W' and (build_type == 'white' or build_type == 'white_win')):
                temp2_X.append(temp_X[0])
                temp2_y.append(temp_y[0])
                print 'X = '
                print_board(temp_X[0])
                print 'y = ' + str(temp_y[0]) + ' (' + \
                               str(pos_str2pos_index(pos_str)) + ') ' + \
                               '(' + pos_str + ')'
                print ''

            temp_X = []
            temp_y = []

        i += 1

    print "End of game"
    print_board(board)

    winner = who_is_winner(board)
    if (winner == 1 and build_type == 'black_win') or \
       (winner == 2 and build_type == 'white_win') or \
       build_type == 'black' or build_type == 'white':
        record_X.extend(temp2_X)
        record_y.extend(temp2_y)

    board = []
    temp2_X = []
    temp2_y = []
    line_cnt += 1
    """

f.close()
