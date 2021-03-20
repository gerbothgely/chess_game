from tkinter import *
from chess_modules.positions import starting_coordinates_dict

DARK_COLOUR = "#1b262c"
LIGHT_COLOUR = "#0f4c75"


class Board:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Game")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        self.canvas = Canvas(master=master, height=800, width=800, highlightthickness=0)
        for i in range(0, 801, 200):
            for j in range(0, 801, 200):
                for k in range(0, 801, 100):
                    self.canvas.create_rectangle(0 + i + k, 0 + j + k, 100 + i + k, 100 + j + k, fill=LIGHT_COLOUR)
                    self.canvas.create_rectangle(800 - i - k, 0 + j + k, 700 - i - k, 100 + j + k, fill=DARK_COLOUR)
        self.canvas.grid(column=0, row=0)

        self.white_pawn_img = PhotoImage(file="./chess_pieces/white_pawn.png")
        self.white_pawn_1 = self.canvas.create_image(starting_coordinates_dict["white_pawn_1"],
                                                     image=self.white_pawn_img)
        self.white_pawn_2 = self.canvas.create_image(starting_coordinates_dict["white_pawn_2"],
                                                     image=self.white_pawn_img)
        self.white_pawn_3 = self.canvas.create_image(starting_coordinates_dict["white_pawn_3"],
                                                     image=self.white_pawn_img)
        self.white_pawn_4 = self.canvas.create_image(starting_coordinates_dict["white_pawn_4"],
                                                     image=self.white_pawn_img)
        self.white_pawn_5 = self.canvas.create_image(starting_coordinates_dict["white_pawn_5"],
                                                     image=self.white_pawn_img)
        self.white_pawn_6 = self.canvas.create_image(starting_coordinates_dict["white_pawn_6"],
                                                     image=self.white_pawn_img)
        self.white_pawn_7 = self.canvas.create_image(starting_coordinates_dict["white_pawn_7"],
                                                     image=self.white_pawn_img)
        self.white_pawn_8 = self.canvas.create_image(starting_coordinates_dict["white_pawn_8"],
                                                     image=self.white_pawn_img)
        self.white_rook_img = PhotoImage(file="./chess_pieces/white_rook.png")
        self.white_rook_1 = self.canvas.create_image(starting_coordinates_dict["white_rook_1"],
                                                     image=self.white_rook_img)
        self.white_rook_2 = self.canvas.create_image(starting_coordinates_dict["white_rook_2"],
                                                     image=self.white_rook_img)
        self.white_knight_img = PhotoImage(file="./chess_pieces/white_knight.png")
        self.white_knight_1 = self.canvas.create_image(starting_coordinates_dict["white_knight_1"],
                                                       image=self.white_knight_img)
        self.white_knight_2 = self.canvas.create_image(starting_coordinates_dict["white_knight_2"],
                                                       image=self.white_knight_img)
        self.white_bishop_img = PhotoImage(file="./chess_pieces/white_bishop.png")
        self.white_bishop_1 = self.canvas.create_image(starting_coordinates_dict["white_bishop_1"],
                                                       image=self.white_bishop_img)
        self.white_bishop_2 = self.canvas.create_image(starting_coordinates_dict["white_bishop_2"],
                                                       image=self.white_bishop_img)
        self.white_queen_img = PhotoImage(file="./chess_pieces/white_queen.png")
        self.white_queen = self.canvas.create_image(starting_coordinates_dict["white_queen"],
                                                    image=self.white_queen_img)
        self.white_king_img = PhotoImage(file="./chess_pieces/white_king.png")
        self.white_king = self.canvas.create_image(starting_coordinates_dict["white_king"],
                                                   image=self.white_king_img)

        self.black_pawn_img = PhotoImage(file="./chess_pieces/black_pawn.png")
        self.black_pawn_1 = self.canvas.create_image(starting_coordinates_dict["black_pawn_1"],
                                                     image=self.black_pawn_img)
        self.black_pawn_2 = self.canvas.create_image(starting_coordinates_dict["black_pawn_2"],
                                                     image=self.black_pawn_img)
        self.black_pawn_3 = self.canvas.create_image(starting_coordinates_dict["black_pawn_3"],
                                                     image=self.black_pawn_img)
        self.black_pawn_4 = self.canvas.create_image(starting_coordinates_dict["black_pawn_4"],
                                                     image=self.black_pawn_img)
        self.black_pawn_5 = self.canvas.create_image(starting_coordinates_dict["black_pawn_5"],
                                                     image=self.black_pawn_img)
        self.black_pawn_6 = self.canvas.create_image(starting_coordinates_dict["black_pawn_6"],
                                                     image=self.black_pawn_img)
        self.black_pawn_7 = self.canvas.create_image(starting_coordinates_dict["black_pawn_7"],
                                                     image=self.black_pawn_img)
        self.black_pawn_8 = self.canvas.create_image(starting_coordinates_dict["black_pawn_8"],
                                                     image=self.black_pawn_img)
        self.black_rook_img = PhotoImage(file="./chess_pieces/black_rook.png")
        self.black_rook_1 = self.canvas.create_image(starting_coordinates_dict["black_rook_1"],
                                                     image=self.black_rook_img)
        self.black_rook_2 = self.canvas.create_image(starting_coordinates_dict["black_rook_2"],
                                                     image=self.black_rook_img)
        self.black_knight_img = PhotoImage(file="./chess_pieces/black_knight.png")
        self.black_knight_1 = self.canvas.create_image(starting_coordinates_dict["black_knight_1"],
                                                       image=self.black_knight_img)
        self.black_knight_2 = self.canvas.create_image(starting_coordinates_dict["black_knight_2"],
                                                       image=self.black_knight_img)
        self.black_bishop_img = PhotoImage(file="./chess_pieces/black_bishop.png")
        self.black_bishop_1 = self.canvas.create_image(starting_coordinates_dict["black_bishop_1"],
                                                       image=self.black_bishop_img)
        self.black_bishop_2 = self.canvas.create_image(starting_coordinates_dict["black_bishop_2"],
                                                       image=self.black_bishop_img)
        self.black_queen_img = PhotoImage(file="./chess_pieces/black_queen.png")
        self.black_queen = self.canvas.create_image(starting_coordinates_dict["black_queen"],
                                                    image=self.black_queen_img)
        self.black_king_img = PhotoImage(file="./chess_pieces/black_king.png")
        self.black_king = self.canvas.create_image(starting_coordinates_dict["black_king"],
                                                   image=self.black_king_img)
