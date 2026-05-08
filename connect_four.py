import random

ROWS = 6
COLS = 7
EMPTY = '.'
P1 = 'X'
P2 = 'O'


def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board


def print_board(board):
    print()
    for r in range(ROWS):
        line = '| '
        for c in range(COLS):
            line += board[r][c] + ' '
        line += '|'
        print(line)
    print('  ' + ' '.join(str(i + 1) for i in range(COLS)))
    print()


def drop_piece(board, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return r
    return -1


def is_valid_move(board, col):
    return board[0][col] == EMPTY


def get_valid_columns(board):
    valid = []
    for c in range(COLS):
        if is_valid_move(board, c):
            valid.append(c)
    return valid


def check_win(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


def is_board_full(board):
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True


def score_position(board, piece):
    score = 0

    for c in range(COLS):
        column = []
        for r in range(ROWS):
            column.append(board[r][c])
        if column[ROWS - 1] == EMPTY:
            continue

    center_col = COLS // 2
    center_count = 0
    for r in range(ROWS):
        if board[r][center_col] == piece:
            center_count += 1
    score += center_count * 3

    opponent = P1 if piece == P2 else P2

    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board[r][c], board[r][c+1], board[r][c+2], board[r][c+3]]
            score += evaluate_window(window, piece, opponent)

    for r in range(ROWS - 3):
        for c in range(COLS):
            window = [board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]]
            score += evaluate_window(window, piece, opponent)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]]
            score += evaluate_window(window, piece, opponent)

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]]
            score += evaluate_window(window, piece, opponent)

    return score


def evaluate_window(window, piece, opponent):
    score = 0
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent)

    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2

    if opp_count == 3 and empty_count == 1:
        score -= 4

    return score


def ai_move(board, piece):
    valid_cols = get_valid_columns(board)
    best_score = -9999
    best_col = random.choice(valid_cols)

    for col in valid_cols:
        row = drop_piece(board, col, piece)
        s = score_position(board, piece)
        board[row][col] = EMPTY

        if s > best_score:
            best_score = s
            best_col = col

    return best_col


def get_player_move(board):
    while True:
        try:
            col = int(input("Pick a column (1-7): ")) - 1
        except ValueError:
            print("Enter a number between 1 and 7.")
            continue

        if col < 0 or col >= COLS:
            print("Column out of range.")
            continue

        if not is_valid_move(board, col):
            print("Column is full.")
            continue

        return col


def choose_mode():
    print("1) Two players")
    print("2) vs Computer")
    while True:
        choice = input("Select mode: ").strip()
        if choice == '1':
            return False
        elif choice == '2':
            return True
        else:
            print("Enter 1 or 2.")


def main():
    print("Connect Four")
    print()
    vs_ai = choose_mode()

    board = create_board()
    current = P1
    game_over = False

    print_board(board)

    while not game_over:
        if current == P2 and vs_ai:
            print("Computer is thinking...")
            col = ai_move(board, P2)
            print(f"Computer picks column {col + 1}")
        else:
            print(f"Player {current}'s turn")
            col = get_player_move(board)

        drop_piece(board, col, current)
        print_board(board)

        if check_win(board, current):
            if current == P2 and vs_ai:
                print("Computer wins!")
            else:
                print(f"Player {current} wins!")
            game_over = True
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            if current == P1:
                current = P2
            else:
                current = P1


if __name__ == "__main__":
    main()
