from tkinter import *
from chess_modules.board import Board
from chess_modules.rules import validate_move, detect_square, detect_piece,\
    get_displacement, check_own_king_safety, numeric_repper, pawn_move_validator
from chess_modules.positions import piece_positions_dict, notation_dict, numeric_to_lettered

# CLEAR AUXILIARY MOVES LOG TEXT FILE
with open("./moves_log.txt", "w") as file:
    file.write("")

# SIMPLE TURN COUNTER FLAG VARIABLE (reminder: turn % 2 is used to detect white's/black's turn)
turn = 1

# MOMENTARY GAME STATE FLAG VARIABLES
selection_coordinates = []
selection_square = ""
selected_piece = ""
target_square = ""

# TKINTER RUN-THROUGH WORKAROUND:
delegated_piece = ""


# INTERFACE CONTROL MECHANICS
def action():
    board.canvas.bind("<Button-1>", actions_core)


# GAME MECHANICS CENTRE
def actions_core(event):
    global turn
    global selection_coordinates
    global selection_square
    global selected_piece
    global target_square
    global delegated_piece

    # CHOOSE A SQUARE
    selection_coordinates = [event.x, event.y]
    selection_square = detect_square(selection_coordinates)

    # IF PIECE NOT ALREADY CHOSEN, CHOOSE IT
    if not selected_piece:
        selected_piece = detect_piece(selection_square)
        if turn % 2 == 1 and "black" in selected_piece or turn % 2 == 0 and "white" in selected_piece:
            selected_piece = ""

    # IF PIECE IS CHOSEN, CHOOSE SQUARE TO MOVE TO
    elif selected_piece:

        # SIMPLE CHECK IF PLAYER WANTS TO CHOOSE ANOTHER PIECE INSTEAD
        if (turn % 2 == 1 and "white" in selected_piece) or (turn % 2 == 0 and "black" in selected_piece):
            if "white" in selected_piece and "white" in detect_piece(selection_square):
                selected_piece = detect_piece(selection_square)

            elif "black" in selected_piece and "black" in detect_piece(selection_square) and turn % 2 == 0:
                selected_piece = detect_piece(selection_square)

            # WHEN THE PIECE IS FINALIZED, MOVEMENT MECHANICS IS ACTIVATED
            else:
                # SAFETY STARTING POSITION PLACEHOLDER
                origin_square = piece_positions_dict[selected_piece]

                # SQUARE SELECTION REDEFINED TO TARGET SQUARE
                target_square = selection_square

                # IF PAWN PROMOTION - MECHANICS
                if ("white_pawn" in selected_piece and int(target_square[1]) == 8) \
                        or ("black_pawn" in selected_piece and int(target_square[1]) == 1):

                    initial_numeric, final_numeric = numeric_repper(selected_piece, target_square)
                    if pawn_move_validator(selected_piece, target_square, initial_numeric, final_numeric):

                        piece_to_take = detect_piece(target_square)

                        try:

                            check_own_king_safety(selected_piece, target_square)

                            board.canvas.move(getattr(board, selected_piece),
                                              *get_displacement(selected_piece, target_square))

                            del piece_positions_dict[piece_to_take]
                            board.canvas.delete(getattr(board, piece_to_take))

                            piece_positions_dict[selected_piece] = target_square
                            delegated_piece = selected_piece

                            # CHOOSE PROMOTION PRODUCT CONTEXT MENU
                            query_window = Toplevel()
                            query_window.title("*PROMOTION*")

                            def promote_to_queen():
                                init_num, fin_num = numeric_repper(delegated_piece, target_square)

                                board.canvas.delete(getattr(board, delegated_piece))
                                del piece_positions_dict[delegated_piece]

                                if "white" in delegated_piece:
                                    board.white_queen_A = board.canvas.create_image([fin_num[0] * 100 - 50, 50],
                                                                                    image=board.white_queen_img)
                                    piece_positions_dict["white_queen_A"] = target_square
                                elif "black" in delegated_piece:
                                    board.black_queen_A = board.canvas.create_image([fin_num[0] * 100 - 50, 750],
                                                                                    image=board.black_queen_img)
                                    piece_positions_dict["black_queen_A"] = target_square

                                query_window.destroy()

                            def promote_to_rook():
                                init_num, fin_num = numeric_repper(delegated_piece, target_square)

                                board.canvas.delete(getattr(board, delegated_piece))
                                del piece_positions_dict[delegated_piece]

                                if "white" in delegated_piece:
                                    board.white_rook_A = board.canvas.create_image([fin_num[0] * 100 - 50, 50],
                                                                                   image=board.white_rook_img)
                                    piece_positions_dict["white_rook_A"] = target_square
                                elif "black" in delegated_piece:
                                    board.black_rook_A = board.canvas.create_image([fin_num[0] * 100 - 50, 750],
                                                                                   image=board.black_rook_img)
                                    piece_positions_dict["black_rook_A"] = target_square

                                query_window.destroy()

                            def promote_to_bishop():
                                init_num, fin_num = numeric_repper(delegated_piece, target_square)

                                board.canvas.delete(getattr(board, delegated_piece))
                                del piece_positions_dict[delegated_piece]

                                if "white" in delegated_piece:
                                    board.white_bishop_A = board.canvas.create_image([fin_num[0] * 100 - 50, 50],
                                                                                     image=board.white_bishop_img)
                                    piece_positions_dict["white_bishop_A"] = target_square
                                elif "black" in delegated_piece:
                                    board.black_bishop_A = board.canvas.create_image([fin_num[0] * 100 - 50, 750],
                                                                                     image=board.black_bishop_img)
                                    piece_positions_dict["black_bishop_A"] = target_square

                                query_window.destroy()

                            def promote_to_knight():
                                init_num, fin_num = numeric_repper(delegated_piece, target_square)

                                board.canvas.delete(getattr(board, delegated_piece))
                                del piece_positions_dict[delegated_piece]

                                if "white" in delegated_piece:
                                    board.white_knight_A = board.canvas.create_image([fin_num[0] * 100 - 50, 50],
                                                                                     image=board.white_knight_img)
                                    piece_positions_dict["white_knight_A"] = target_square
                                elif "black" in delegated_piece:
                                    board.black_knight_A = board.canvas.create_image([fin_num[0] * 100 - 50, 750],
                                                                                     image=board.black_knight_img)
                                    piece_positions_dict["black_knight_A"] = target_square

                                query_window.destroy()

                            if "white" in selected_piece:
                                Label(master=query_window, text="Select the promotion grade: ")\
                                    .grid(column=1, row=0, columnspan=2)
                                Button(master=query_window, image=board.white_queen_img,
                                       command=promote_to_queen).grid(column=0, row=1)
                                Button(master=query_window, image=board.white_rook_img,
                                       command=promote_to_rook).grid(column=1, row=1)
                                Button(master=query_window, image=board.white_bishop_img,
                                       command=promote_to_bishop).grid(column=2, row=1)
                                Button(master=query_window, image=board.white_knight_img,
                                       command=promote_to_knight).grid(column=3, row=1)
                            elif "black" in selected_piece:
                                Label(master=query_window, text="Select the promotion grade: ")\
                                    .grid(column=1, row=0, columnspan=2)
                                Button(master=query_window, image=board.black_queen_img,
                                       command=promote_to_queen).grid(column=0, row=1)
                                Button(master=query_window, image=board.black_rook_img,
                                       command=promote_to_rook).grid(column=1, row=1)
                                Button(master=query_window, image=board.black_bishop_img,
                                       command=promote_to_bishop).grid(column=2, row=1)
                                Button(master=query_window, image=board.black_knight_img,
                                       command=promote_to_knight).grid(column=3, row=1)

                            with open("./moves_log.txt", "a") as log:
                                log.write(f"{turn}. {notation_dict[selected_piece]}{origin_square}-{target_square} "
                                          f"({selected_piece})\n")
                            turn += 1

                        except ValueError:
                            pass

                # IF EN PASSANT - MECHANICS
                elif "pawn" in selected_piece and piece_positions_dict[selected_piece][0] != target_square[0]\
                        and target_square not in piece_positions_dict.values():

                    initial_numeric, final_numeric = numeric_repper(selected_piece, target_square)

                    if "white" in selected_piece and initial_numeric[1] == 5 \
                            and abs(final_numeric[0] - initial_numeric[0]) == 1 and final_numeric[1] == 6:

                        logfile = open("./moves_log.txt", "a+")
                        logfile.seek(0)

                        try:
                            possible_enemy_pawn_at = [final_numeric[0], final_numeric[1] - 1]
                            exact_location = numeric_to_lettered[possible_enemy_pawn_at[0]] + str(possible_enemy_pawn_at[1])
                            detected_pawn_name = detect_piece(exact_location)

                            if detected_pawn_name:

                                result = None
                                x = turn - 1
                                for line in logfile:
                                    if int(line[0]) == x:
                                        if detected_pawn_name in line and (exact_location[0] + "7") in line:
                                            result = True

                                if result:
                                    check_own_king_safety(selected_piece, target_square)

                                    board.canvas.move(getattr(board, selected_piece),
                                                      *get_displacement(selected_piece, target_square))

                                    del piece_positions_dict[detected_pawn_name]
                                    board.canvas.delete(getattr(board, detected_pawn_name))

                                    piece_positions_dict[selected_piece] = target_square

                                    logfile.write(f"{turn}. {origin_square}-{target_square} ({selected_piece})\n")

                                    turn += 1

                        except ValueError:
                            pass

                        finally:
                            logfile.close()

                    elif "black" in selected_piece and initial_numeric[1] == 4 \
                            and abs(final_numeric[0] - initial_numeric[0]) == 1 and final_numeric[1] == 3:

                        logfile = open("./moves_log.txt", "a+")
                        logfile.seek(0)

                        try:
                            possible_enemy_pawn_at = [final_numeric[0], final_numeric[1] + 1]
                            exact_location = numeric_to_lettered[possible_enemy_pawn_at[0]] + str(possible_enemy_pawn_at[1])
                            detected_pawn_name = detect_piece(exact_location)

                            if detected_pawn_name:

                                result = None
                                x = turn - 1
                                for line in logfile:
                                    if int(line[0]) == x:
                                        if detected_pawn_name in line and (exact_location[0] + "2") in line:
                                            result = True

                                if result:
                                    check_own_king_safety(selected_piece, target_square)

                                    board.canvas.move(getattr(board, selected_piece),
                                                      *get_displacement(selected_piece, target_square))

                                    del piece_positions_dict[detected_pawn_name]
                                    board.canvas.delete(getattr(board, detected_pawn_name))

                                    piece_positions_dict[selected_piece] = target_square

                                    logfile.write(f"{turn}. {origin_square}-{target_square} ({selected_piece})\n")

                                    turn += 1

                        except ValueError:
                            pass

                        finally:
                            logfile.close()

                # KING-ROOK CASTLING MECHANICS
                # reminder: NOT POSSIBLE IF: move from check / to check / through check / or passage not free
                elif (selected_piece == "white_king" and target_square == "g1")\
                        or (selected_piece == "white_king" and target_square == "c1")\
                        or (selected_piece == "black_king" and target_square == "g8")\
                        or (selected_piece == "black_king" and target_square == "c8"):

                    logfile = open("./moves_log.txt", "a+")
                    logfile.seek(0)
                    file_text = logfile.read()

                    try:
                        check_own_king_safety(selected_piece, origin_square)

                        if selected_piece == "white_king":
                            if target_square == "g1"\
                                    and "white_king" not in file_text and "white_rook_2" not in file_text\
                                    and "f1" not in piece_positions_dict.values()\
                                    and "g1" not in piece_positions_dict.values():
                                if validate_move(selected_piece, "f1") \
                                        and check_own_king_safety(selected_piece, "f1"):
                                    piece_positions_dict[selected_piece] = "f1"
                                    if validate_move(selected_piece, target_square) \
                                            and check_own_king_safety(selected_piece, target_square):

                                        board.canvas.move(board.white_king, 200, 0)
                                        piece_positions_dict[selected_piece] = target_square
                                        board.canvas.move(board.white_rook_2, -200, 0)
                                        piece_positions_dict["white_rook_2"] = "f1"

                                        logfile.write(f"{turn}. O-O\n")

                                        turn += 1
                                    else:
                                        piece_positions_dict[selected_piece] = origin_square
                            elif target_square == "c1"\
                                    and "white_king" not in file_text and "white_rook_1" not in file_text\
                                    and "d1" not in piece_positions_dict.values()\
                                    and "c1" not in piece_positions_dict.values()\
                                    and "b1" not in piece_positions_dict.values():
                                if validate_move(selected_piece, "d1") \
                                        and check_own_king_safety(selected_piece, "d1"):
                                    piece_positions_dict[selected_piece] = "d1"
                                    if validate_move(selected_piece, target_square) \
                                            and check_own_king_safety(selected_piece, target_square):

                                        board.canvas.move(board.white_king, -200, 0)
                                        piece_positions_dict[selected_piece] = target_square
                                        board.canvas.move(board.white_rook_1, 300, 0)
                                        piece_positions_dict["white_rook_1"] = "d1"

                                        logfile.write(f"{turn}. O-O-O\n")

                                        turn += 1
                                    else:
                                        piece_positions_dict[selected_piece] = origin_square

                        elif selected_piece == "black_king":
                            if target_square == "g8"\
                                    and "black_king" not in file_text and "black_rook_2" not in file_text\
                                    and "f8" not in piece_positions_dict.values()\
                                    and "g8" not in piece_positions_dict.values():
                                if validate_move(selected_piece, "f8") \
                                        and check_own_king_safety(selected_piece, "f8"):
                                    piece_positions_dict[selected_piece] = "f8"
                                    if validate_move(selected_piece, target_square) \
                                            and check_own_king_safety(selected_piece, target_square):

                                        board.canvas.move(board.black_king, 200, 0)
                                        piece_positions_dict[selected_piece] = target_square
                                        board.canvas.move(board.black_rook_2, -200, 0)
                                        piece_positions_dict["black_rook_2"] = "f8"

                                        logfile.write(f"{turn}. O-O\n")

                                        turn += 1
                                    else:
                                        piece_positions_dict[selected_piece] = origin_square
                            elif target_square == "c8"\
                                    and "black_king" not in file_text and "black_rook_1" not in file_text\
                                    and "d8" not in piece_positions_dict.values()\
                                    and "c8" not in piece_positions_dict.values()\
                                    and "b8" not in piece_positions_dict.values():
                                if validate_move(selected_piece, "d8") \
                                        and check_own_king_safety(selected_piece, "d8"):
                                    piece_positions_dict[selected_piece] = "d8"
                                    if validate_move(selected_piece, target_square) \
                                            and check_own_king_safety(selected_piece, target_square):

                                        board.canvas.move(board.black_king, -200, 0)
                                        piece_positions_dict[selected_piece] = target_square
                                        board.canvas.move(board.black_rook_1, 300, 0)
                                        piece_positions_dict["black_rook_1"] = "d8"

                                        logfile.write(f"{turn}. O-O-O\n")

                                        turn += 1
                                    else:
                                        piece_positions_dict[selected_piece] = origin_square
                    except ValueError:
                        pass

                    finally:
                        logfile.close()

                # EVERY OTHER MOVE TYPE - DELEGATING MECHANICS SYSTEM
                elif validate_move(selected_piece, target_square):
                    try:
                        check_own_king_safety(selected_piece, target_square)

                        board.canvas.move(getattr(board, selected_piece),
                                          *get_displacement(selected_piece, target_square))
                        if target_square in [x for x in piece_positions_dict.values()
                                             if x != piece_positions_dict[selected_piece]]:
                            board.canvas.delete(getattr(board, detect_piece(target_square)))
                            del piece_positions_dict[detect_piece(target_square)]
                        piece_positions_dict[selected_piece] = target_square

                        with open("./moves_log.txt", "a") as log:
                            log.write(f"{turn}. {notation_dict[selected_piece]}{origin_square}-{target_square} "
                                      f"({selected_piece})\n")

                        turn += 1

                    except ValueError:
                        piece_positions_dict[selected_piece] = origin_square
                        pass
                else:
                    pass

                # FLAG FREE-UP AFTER EITHER SUCCESS OR FAILURE
                selected_piece = ""


# MAIN GUI CYCLE/LOOP
gui = Tk()
board = Board(gui)
action()
gui.mainloop()
