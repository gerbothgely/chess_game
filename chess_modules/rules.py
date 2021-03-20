from chess_modules.positions import piece_positions_dict, lettered_to_numeric, numeric_to_lettered


# BASE MOVE VALIDATOR
def validate_move(selected_piece, target_square, oppositum=None, propositum=None):
    initial_numeric, final_numeric = numeric_repper(selected_piece, target_square)
    if "pawn" in selected_piece:
        return pawn_move_validator(selected_piece, target_square, initial_numeric, final_numeric)
    if "rook" in selected_piece:
        return rook_move_validator(initial_numeric, final_numeric, oppositum, propositum)
    if "knight" in selected_piece:
        return knight_move_validator(initial_numeric, final_numeric)
    if "bishop" in selected_piece:
        return bishop_move_validator(initial_numeric, final_numeric, oppositum, propositum)
    if "queen" in selected_piece:
        return queen_move_validator(initial_numeric, final_numeric, oppositum, propositum)
    if "king" in selected_piece:
        return king_move_validator(initial_numeric, final_numeric)


# CHECKS IF PIECE CAN MOVE TO POSITION FREELY - WITH NO PIECES IN-BETWEEN TO BLOCK THE WAY
def passage_is_free(initial_numeric, final_numeric, oppositum, propositum):
    vertical_change = final_numeric[0] - initial_numeric[0]
    horizontal_change = final_numeric[1] - initial_numeric[1]
    move_through = []

    # IF MOVING ALONG THE X-AXIS (ONLY)
    if vertical_change == 0:
        if horizontal_change > 0:
            for i in range(1, abs(horizontal_change)):
                x = numeric_to_lettered[initial_numeric[0]] + str(initial_numeric[1] + i)
                move_through.append(x)
        elif horizontal_change < 0:
            for i in range(1, abs(horizontal_change)):
                x = numeric_to_lettered[initial_numeric[0]] + str(initial_numeric[1] - i)
                move_through.append(x)

    # IF MOVING ALONG THE Y-AXIS (ONLY)
    elif horizontal_change == 0:
        if vertical_change > 0:
            for j in range(1, abs(vertical_change)):
                y = numeric_to_lettered[initial_numeric[0] + j] + str(initial_numeric[1])
                move_through.append(y)
        elif vertical_change < 0:
            for j in range(1, abs(vertical_change)):
                y = numeric_to_lettered[initial_numeric[0] - j] + str(initial_numeric[1])
                move_through.append(y)

    # IF MOVING DIAGONALLY (i.e. ALONG BOTH X- AND Y- AXES)
    elif vertical_change > 0 < horizontal_change:
        for i in range(1, abs(vertical_change)):
            z = numeric_to_lettered[initial_numeric[0] + i] + str(initial_numeric[1] + i)
            move_through.append(z)
    elif vertical_change < 0 > horizontal_change:
        for i in range(1, abs(vertical_change)):
            z = numeric_to_lettered[initial_numeric[0] - i] + str(initial_numeric[1] - i)
            move_through.append(z)
    elif vertical_change < 0 < horizontal_change:
        for i in range(1, abs(vertical_change)):
            z = numeric_to_lettered[initial_numeric[0] - i] + str(initial_numeric[1] + i)
            move_through.append(z)
    elif vertical_change > 0 > horizontal_change:
        for i in range(1, abs(vertical_change)):
            z = numeric_to_lettered[initial_numeric[0] + i] + str(initial_numeric[1] - i)
            move_through.append(z)

    # IF PIECE MOVE MAY(!) AFFECT OWN KING'S SAFETY
    if oppositum and propositum:
        transposition_list = [x for x in piece_positions_dict.values() if x != oppositum]
        transposition_list.append(propositum)
        return not bool(set(move_through) & set(transposition_list))

    # IF PIECE MOVE IS EITHER SIMPLY UNSAFE OR CLEARLY SAFE
    elif not oppositum and not propositum:
        list_of_things_occupied = [x for x in piece_positions_dict.values()]
        return not bool(set(move_through) & set(list_of_things_occupied))


# oppositum= AND propositum= ARGUMENTS SIMULATE TRANSPARENT PIECE AND PROJECTED PIECE BEHAVIOUR
# (this allows moving alongside the absolute pin or to attack the pinning piece itself)
def check_own_king_safety(selected_piece, target_square):
    squares_under_threat = []
    if "white" in selected_piece:
        for i in piece_positions_dict.keys():
            if ("black" in i) and ("pawn" not in i):
                for j in "abcdefgh":
                    for k in "12345678":
                        one_of_all_squares = j+k
                        if validate_move(i, one_of_all_squares,
                                         oppositum=piece_positions_dict[selected_piece], propositum=target_square)\
                                and piece_positions_dict[i] != target_square:
                            squares_under_threat.append(one_of_all_squares)
            elif ("black" in i) and ("pawn" in i):
                position = piece_positions_dict[i]
                numeric_position = [lettered_to_numeric[position[0]], int(position[1])]
                a = [numeric_position[0] - 1, numeric_position[1] - 1]
                b = [numeric_position[0] + 1, numeric_position[1] - 1]
                aa = numeric_to_lettered.get(a[0], "") + str(a[1])
                bb = numeric_to_lettered.get(b[0], "") + str(b[1])
                if len(aa) == 2:
                    squares_under_threat.append(aa)
                if len(bb) == 2:
                    squares_under_threat.append(bb)

        if "king" in selected_piece:
            if target_square not in set(squares_under_threat):
                return True
            else:
                raise ValueError
        elif piece_positions_dict["white_king"] not in set(squares_under_threat):
            return True
        else:
            raise ValueError

    elif "black" in selected_piece:
        for i in piece_positions_dict.keys():
            if ("white" in i) and ("pawn" not in i):
                for j in "abcdefgh":
                    for k in "12345678":
                        one_of_all_squares = j+k
                        if validate_move(i, one_of_all_squares,
                                         oppositum=piece_positions_dict[selected_piece], propositum=target_square)\
                                and piece_positions_dict[i] != target_square:
                            squares_under_threat.append(one_of_all_squares)
            elif ("white" in i) and ("pawn" in i):
                position = piece_positions_dict[i]
                numeric_position = [lettered_to_numeric[position[0]], int(position[1])]
                a = [numeric_position[0] - 1, numeric_position[1] + 1]
                b = [numeric_position[0] + 1, numeric_position[1] + 1]
                aa = numeric_to_lettered.get(a[0], "") + str(a[1])
                bb = numeric_to_lettered.get(b[0], "") + str(b[1])
                if len(aa) == 2:
                    squares_under_threat.append(aa)
                if len(bb) == 2:
                    squares_under_threat.append(bb)
        if "king" in selected_piece:
            if target_square not in set(squares_under_threat):
                return True
            else:
                raise ValueError
        elif piece_positions_dict["black_king"] not in set(squares_under_threat):
            return True
        else:
            raise ValueError


def pawn_move_validator(selected_piece, target_square, initial_numeric, final_numeric):
    if "white" in selected_piece:
        if initial_numeric[0] == final_numeric[0] and target_square not in piece_positions_dict.values():
            if initial_numeric[1] == 2 and 2 < final_numeric[1] <= 4:
                return True
            elif initial_numeric[1] > 2 and final_numeric[1] == initial_numeric[1] + 1:
                return True
        elif abs(final_numeric[0] - initial_numeric[0]) == 1 and final_numeric[1] - initial_numeric[1] == 1:
            if "black" in detect_piece(target_square):
                return True
    elif "black" in selected_piece:
        if initial_numeric[0] == final_numeric[0] and target_square not in piece_positions_dict.values():
            if initial_numeric[1] == 7 and 7 > final_numeric[1] >= 5:
                return True
            elif initial_numeric[1] < 7 and final_numeric[1] == initial_numeric[1] - 1:
                return True
        elif abs(final_numeric[0] - initial_numeric[0]) == 1 and final_numeric[1] - initial_numeric[1] == -1:
            if "white" in detect_piece(target_square):
                return True


def rook_move_validator(initial_numeric, final_numeric, oppositum, propositum):
    if passage_is_free(initial_numeric, final_numeric, oppositum, propositum) and initial_numeric != final_numeric:
        if (final_numeric[0] == initial_numeric[0] and 1 <= final_numeric[1] <= 8)\
                or (final_numeric[1] == initial_numeric[1] and 1 <= final_numeric[0] <= 8):
            return True


def knight_move_validator(initial_numeric, final_numeric):
    if (abs(final_numeric[0] - initial_numeric[0]) == 2 and abs(final_numeric[1] - initial_numeric[1]) == 1) or \
            (abs(final_numeric[0] - initial_numeric[0]) == 1 and abs(final_numeric[1] - initial_numeric[1]) == 2)\
            and initial_numeric != final_numeric:
        return True


def bishop_move_validator(initial_numeric, final_numeric, oppositum, propositum):
    if passage_is_free(initial_numeric, final_numeric, oppositum, propositum) and initial_numeric != final_numeric:
        if abs(final_numeric[0] - initial_numeric[0]) == abs(final_numeric[1] - initial_numeric[1]):
            return True


def queen_move_validator(initial_numeric, final_numeric, oppositum, propositum):
    if (rook_move_validator(initial_numeric, final_numeric, oppositum, propositum)
        or bishop_move_validator(initial_numeric, final_numeric, oppositum, propositum))\
            and initial_numeric != final_numeric:
        return True


def king_move_validator(initial_numeric, final_numeric):
    if abs(final_numeric[0] - initial_numeric[0]) <= 1 and abs(final_numeric[1] - initial_numeric[1]) <= 1\
            and initial_numeric != final_numeric:
        return True


# UTILITIES: RULES-BASED AUXILIARY FUNCTIONS
# GET TKINTER MOVE COORDINATES FOR MOVE ON BOARD
def get_displacement(selected_piece, target_square):
    initial_numeric, final_numeric = numeric_repper(selected_piece, target_square)
    x_displacement = final_numeric[0] - initial_numeric[0]
    y_displacement = final_numeric[1] - initial_numeric[1]
    return x_displacement * 100, y_displacement * -100


# REPRESENT A LETTERED (str) BOARD COORDINATE NUMERICALLY (two ints inside list - two lists inside tuple)
def numeric_repper(selected_piece, target_square):
    initial_position = piece_positions_dict[selected_piece]
    initial_list = [letter for letter in initial_position]
    initial_numeric = [lettered_to_numeric[initial_list[0]], int(initial_list[1])]
    final_position = target_square
    final_list = [letter for letter in final_position]
    final_numeric = [lettered_to_numeric[final_list[0]], int(final_list[1])]
    return initial_numeric, final_numeric


# RETURN SELECTED PIECE'S NAME IF SELECTED SQUARE IS OCCUPIED BY ANY
def detect_piece(selection_square):
    for key, value in piece_positions_dict.items():
        if value == selection_square:
            return key
    return ""


# RETURN CHESS COORDINATES FROM TKINTER INTERFACE CLICK
def detect_square(selection_coordinates):
    if 0 < selection_coordinates[0] < 100 and 0 < selection_coordinates[1] < 100:
        return "a8"
    elif 100 < selection_coordinates[0] < 200 and 0 < selection_coordinates[1] < 100:
        return "b8"
    elif 200 < selection_coordinates[0] < 300 and 0 < selection_coordinates[1] < 100:
        return "c8"
    elif 300 < selection_coordinates[0] < 400 and 0 < selection_coordinates[1] < 100:
        return "d8"
    elif 400 < selection_coordinates[0] < 500 and 0 < selection_coordinates[1] < 100:
        return "e8"
    elif 500 < selection_coordinates[0] < 600 and 0 < selection_coordinates[1] < 100:
        return "f8"
    elif 600 < selection_coordinates[0] < 700 and 0 < selection_coordinates[1] < 100:
        return "g8"
    elif 700 < selection_coordinates[0] < 800 and 0 < selection_coordinates[1] < 100:
        return "h8"
    elif 0 < selection_coordinates[0] < 100 and 100 < selection_coordinates[1] < 200:
        return "a7"
    elif 100 < selection_coordinates[0] < 200 and 100 < selection_coordinates[1] < 200:
        return "b7"
    elif 200 < selection_coordinates[0] < 300 and 100 < selection_coordinates[1] < 200:
        return "c7"
    elif 300 < selection_coordinates[0] < 400 and 100 < selection_coordinates[1] < 200:
        return "d7"
    elif 400 < selection_coordinates[0] < 500 and 100 < selection_coordinates[1] < 200:
        return "e7"
    elif 500 < selection_coordinates[0] < 600 and 100 < selection_coordinates[1] < 200:
        return "f7"
    elif 600 < selection_coordinates[0] < 700 and 100 < selection_coordinates[1] < 200:
        return "g7"
    elif 700 < selection_coordinates[0] < 800 and 100 < selection_coordinates[1] < 200:
        return "h7"
    elif 0 < selection_coordinates[0] < 100 and 200 < selection_coordinates[1] < 300:
        return "a6"
    elif 100 < selection_coordinates[0] < 200 and 200 < selection_coordinates[1] < 300:
        return "b6"
    elif 200 < selection_coordinates[0] < 300 and 200 < selection_coordinates[1] < 300:
        return "c6"
    elif 300 < selection_coordinates[0] < 400 and 200 < selection_coordinates[1] < 300:
        return "d6"
    elif 400 < selection_coordinates[0] < 500 and 200 < selection_coordinates[1] < 300:
        return "e6"
    elif 500 < selection_coordinates[0] < 600 and 200 < selection_coordinates[1] < 300:
        return "f6"
    elif 600 < selection_coordinates[0] < 700 and 200 < selection_coordinates[1] < 300:
        return "g6"
    elif 700 < selection_coordinates[0] < 800 and 200 < selection_coordinates[1] < 300:
        return "h6"
    elif 0 < selection_coordinates[0] < 100 and 300 < selection_coordinates[1] < 400:
        return "a5"
    elif 100 < selection_coordinates[0] < 200 and 300 < selection_coordinates[1] < 400:
        return "b5"
    elif 200 < selection_coordinates[0] < 300 and 300 < selection_coordinates[1] < 400:
        return "c5"
    elif 300 < selection_coordinates[0] < 400 and 300 < selection_coordinates[1] < 400:
        return "d5"
    elif 400 < selection_coordinates[0] < 500 and 300 < selection_coordinates[1] < 400:
        return "e5"
    elif 500 < selection_coordinates[0] < 600 and 300 < selection_coordinates[1] < 400:
        return "f5"
    elif 600 < selection_coordinates[0] < 700 and 300 < selection_coordinates[1] < 400:
        return "g5"
    elif 700 < selection_coordinates[0] < 800 and 300 < selection_coordinates[1] < 400:
        return "h5"
    elif 0 < selection_coordinates[0] < 100 and 400 < selection_coordinates[1] < 500:
        return "a4"
    elif 100 < selection_coordinates[0] < 200 and 400 < selection_coordinates[1] < 500:
        return "b4"
    elif 200 < selection_coordinates[0] < 300 and 400 < selection_coordinates[1] < 500:
        return "c4"
    elif 300 < selection_coordinates[0] < 400 and 400 < selection_coordinates[1] < 500:
        return "d4"
    elif 400 < selection_coordinates[0] < 500 and 400 < selection_coordinates[1] < 500:
        return "e4"
    elif 500 < selection_coordinates[0] < 600 and 400 < selection_coordinates[1] < 500:
        return "f4"
    elif 600 < selection_coordinates[0] < 700 and 400 < selection_coordinates[1] < 500:
        return "g4"
    elif 700 < selection_coordinates[0] < 800 and 400 < selection_coordinates[1] < 500:
        return "h4"
    elif 0 < selection_coordinates[0] < 100 and 500 < selection_coordinates[1] < 600:
        return "a3"
    elif 100 < selection_coordinates[0] < 200 and 500 < selection_coordinates[1] < 600:
        return "b3"
    elif 200 < selection_coordinates[0] < 300 and 500 < selection_coordinates[1] < 600:
        return "c3"
    elif 300 < selection_coordinates[0] < 400 and 500 < selection_coordinates[1] < 600:
        return "d3"
    elif 400 < selection_coordinates[0] < 500 and 500 < selection_coordinates[1] < 600:
        return "e3"
    elif 500 < selection_coordinates[0] < 600 and 500 < selection_coordinates[1] < 600:
        return "f3"
    elif 600 < selection_coordinates[0] < 700 and 500 < selection_coordinates[1] < 600:
        return "g3"
    elif 700 < selection_coordinates[0] < 800 and 500 < selection_coordinates[1] < 600:
        return "h3"
    elif 0 < selection_coordinates[0] < 100 and 600 < selection_coordinates[1] < 700:
        return "a2"
    elif 100 < selection_coordinates[0] < 200 and 600 < selection_coordinates[1] < 700:
        return "b2"
    elif 200 < selection_coordinates[0] < 300 and 600 < selection_coordinates[1] < 700:
        return "c2"
    elif 300 < selection_coordinates[0] < 400 and 600 < selection_coordinates[1] < 700:
        return "d2"
    elif 400 < selection_coordinates[0] < 500 and 600 < selection_coordinates[1] < 700:
        return "e2"
    elif 500 < selection_coordinates[0] < 600 and 600 < selection_coordinates[1] < 700:
        return "f2"
    elif 600 < selection_coordinates[0] < 700 and 600 < selection_coordinates[1] < 700:
        return "g2"
    elif 700 < selection_coordinates[0] < 800 and 600 < selection_coordinates[1] < 700:
        return "h2"
    elif 0 < selection_coordinates[0] < 100 and 700 < selection_coordinates[1] < 800:
        return "a1"
    elif 100 < selection_coordinates[0] < 200 and 700 < selection_coordinates[1] < 800:
        return "b1"
    elif 200 < selection_coordinates[0] < 300 and 700 < selection_coordinates[1] < 800:
        return "c1"
    elif 300 < selection_coordinates[0] < 400 and 700 < selection_coordinates[1] < 800:
        return "d1"
    elif 400 < selection_coordinates[0] < 500 and 700 < selection_coordinates[1] < 800:
        return "e1"
    elif 500 < selection_coordinates[0] < 600 and 700 < selection_coordinates[1] < 800:
        return "f1"
    elif 600 < selection_coordinates[0] < 700 and 700 < selection_coordinates[1] < 800:
        return "g1"
    elif 700 < selection_coordinates[0] < 800 and 700 < selection_coordinates[1] < 800:
        return "h1"
