# ESC180 at the University of Toronto (Introduction to Computer Programming Fall 2024, taught by Michael Guerzhoy)
# Project 2: https://www.cs.toronto.edu/~guerzhoy/180/proj/p2_gomoku.pdf
# Starter Code by Michael Guerzhoy with tests contributed by Siavash Kazemian.
# Program by Jessica Yi, passed 88.5/88.5 test cases.

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != ' ':
                return False
    return True

def is_complete(board, y_end, x_end, length, d_y, d_x):
    col = board[y_end][x_end]
    for i in range(length):
        if not (0 <= y_end - i*d_y < len(board) and 0 <= x_end - i*d_x < len(board[0])):
            return False
        if board[y_end-d_y][x_end-d_x] != col:
            return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    if is_complete(board, y_end, x_end, length, d_y, d_x):

        y_bf = y_end - d_y * (length)
        x_bf = x_end - d_x * (length)

        y_af = y_end + d_y
        x_af = x_end + d_x

        start_open = not (
            not (0 <= y_bf < len(board) and 0 <= x_bf < len(board[0]))
            or board[y_bf][x_bf] != " "
        )

        end_open = not (
            not (0 <= y_af < len(board) and 0 <= x_af < len(board[0]))
            or board[y_af][x_af] != " "
        )

        if start_open and end_open:
            return "OPEN"
        elif not start_open and not end_open:
            return "CLOSED"
        else:
            return "SEMIOPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    def within_bounds(y, x):
        return 0 <= y < len(board) and 0 <= x < len(board[0])

    open_seq_count = 0
    semi_seq_count = 0
    curr_y, curr_x = y_start, x_start

    while within_bounds(curr_y, curr_x):
        if board[curr_y][curr_x] == col:
            seq = [(curr_y, curr_x)]
            y, x = curr_y + d_y, curr_x + d_x

            while within_bounds(y, x) and board[y][x] == col:
                seq.append((y,x))
                y += d_y
                x += d_x

            if len(seq) == length:
                bound_result = is_bounded(
                    board,
                    curr_y + d_y*(len(seq) - 1),
                    curr_x + d_x*(len(seq) - 1),
                    length,
                    d_y,
                    d_x
                )
                if bound_result == "OPEN":
                    open_seq_count += 1
                elif bound_result == "SEMIOPEN":
                    semi_seq_count += 1

            curr_y += (len(seq) * d_y)
            curr_x += (len(seq) * d_x)
        else:
            curr_y += d_y
            curr_x += d_x

    return open_seq_count, semi_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_seq_count = 0, 0

    #(0,1)
    for y in range(len(board)):
        open_count, semi_open_count = detect_row(board, col, y, 0, length, 0, 1)
        open_seq_count += open_count
        semi_seq_count += semi_open_count

    #(1,0)
    for x in range(len(board[0])):
        open_count, semi_open_count = detect_row(board, col, 0, x, length, 1, 0)
        open_seq_count += open_count
        semi_seq_count += semi_open_count

    #(1,1)
    for y in range(len(board)):
        open_count, semi_open_count = detect_row(board, col, y, 0, length, 1, 1)
        open_seq_count += open_count
        semi_seq_count += semi_open_count
    for x in range(1, len(board[0])):
        open_count, semi_open_count = detect_row(board, col, 0, x, length, 1, 1)
        open_seq_count += open_count
        semi_seq_count += semi_open_count

    #(1,-1)
    for y in range(len(board)):
        open_count, semi_open_count = detect_row(board, col, y, len(board)-1, length, 1, -1)
        open_seq_count += open_count
        semi_seq_count += semi_open_count
    for x in range(len(board[0]) - 2, -1, -1):
        open_count, semi_open_count = detect_row(board, col, 0, x, length, 1, -1)
        open_seq_count += open_count
        semi_seq_count += semi_open_count

    return open_seq_count, semi_seq_count

def search_max(board):
    max_score = -float('inf')
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":

                board[y][x] = "b"
                cur_score = score(board)

                if cur_score > max_score:
                    max_score = cur_score
                    best_move = y, x

                board[y][x] = " "
    return best_move

def is_win(board):

    def check_length(board, col, y_start, x_start, d_y, d_x):
        y_end = y_start + 4*d_y
        x_end = x_start + 4*d_x

        if not (0 <= y_end < len(board) and 0 <= x_end < len(board[0])):
            return False

        for i in range(5):
            if board[y_start + i*d_y][x_start + i*d_x] != col:
                return False

        if (0 <= y_start - d_y <len(board)
            and 0 <= x_start - d_x <len(board[0])
            and board[y_start - d_y][x_start - d_x] == col
        ):
            return False
        if (0 <= y_end + d_y <len(board)
            and 0 <= x_end + d_x <len(board[0])
            and board[y_end + d_y][x_end + d_x] == col
        ):
            return False
        return True

    def check_colour(board, col):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if check_length(board, col, y, x, 0, 1):
                    return True
                if check_length(board, col, y, x, 1, 0):
                    return True
                if check_length(board, col, y, x, 1, 1):
                    return True
                if check_length(board, col, y, x, 1, -1):
                    return True
        return False

    if check_colour(board, "b"):
        return "BLACK WON"
    if check_colour(board, "w"):
        return "WHITE WON"

    for y in range(len(board)):
        for x in range (len(board[0])):
            if board[y][x] == " ":
                return "CONTINUE PLAYING"
    return "DRAW"

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res