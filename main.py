import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

MENU_IMAGE = pygame.image.load('menu.png')
MENU = pygame.transform.scale(MENU_IMAGE, (WIDTH, HEIGHT))

MAX_SHIPS_FONT = pygame.font.SysFont('comicsans', 20)
PLAYER_FONT = pygame.font.SysFont('comicsans', 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (69, 139, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (139, 69, 0)
GREY = (131, 139, 139)

FPS = 60

# MAX_SHIP_CHOICES = 4
# MAX_GUESSES = 2

grid_boxes_left = [ # coordinates of top-left corner of each grid in left (player 1) side
    [(110, 110), (185, 110), (260, 110), (335, 110), (410, 110), (485, 110), (560, 110)],
    [(110, 185), (185, 185), (260, 185), (335, 185), (410, 185), (485, 185), (560, 185)],
    [(110, 260), (185, 260), (260, 260), (335, 260), (410, 260), (485, 260), (560, 260)],
    [(110, 335), (185, 335), (260, 335), (335, 335), (410, 335), (485, 335), (560, 335)],
    [(110, 410), (185, 410), (260, 410), (335, 410), (410, 410), (485, 410), (560, 410)],
    [(110, 485), (185, 485), (260, 485), (335, 485), (410, 485), (485, 485), (560, 485)],
    [(110, 560), (185, 560), (260, 560), (335, 560), (410, 560), (485, 560), (560, 560)]
    ]

grid_boxes_right = [ # coordinates of top-left corner of each grid in right (player 2) side
    [(850, 110), (925, 110), (1000, 110), (1075, 110), (1150, 110), (1225, 110), (1300, 110)],
    [(850, 185), (925, 185), (1000, 185), (1075, 185), (1150, 185), (1225, 185), (1300, 185)],
    [(850, 260), (925, 260), (1000, 260), (1075, 260), (1150, 260), (1225, 260), (1300, 260)],
    [(850, 335), (925, 335), (1000, 335), (1075, 335), (1150, 335), (1225, 335), (1300, 335)],
    [(850, 410), (925, 410), (1000, 410), (1075, 410), (1150, 410), (1225, 410), (1300, 410)],
    [(850, 485), (925, 485), (1000, 485), (1075, 485), (1150, 485), (1225, 485), (1300, 485)],
    [(850, 560), (925, 560), (1000, 560), (1075, 560), (1150, 560), (1225, 560), (1300, 560)]
    ]

def get_ship_grid_box(mouse_pos : tuple, selected_boxes : list, past_guesses : list, player : int, max_choices : int, is_guessing : bool): # get coordinates of mouse click location according to grid
    if len(selected_boxes) >= max_choices:  # if reached maximum number of choices or guesses, do nothing
        return
    
    if player == 1 or player == 3: # if first player playing
        if mouse_pos[0] < 630 and mouse_pos[0] > 105: # check if inside coordinates vertically of left grid
            if mouse_pos[1] > 105 and mouse_pos[1] < 630: # check if inside coordinates horizontally of left grid
                column = 6 - ((630 - mouse_pos[0]) // 75) # calculate which column user clicked in
                row = 6 - ((630 - mouse_pos[1]) // 75) # calculate which row user clicked in

                if is_guessing: # 2nd part of the game, guessing oponent ship locations
                    coords = (grid_boxes_right[row][column][0]+37, grid_boxes_right[row][column][1]+37) # determine acoording to previously defined grid box locations, which one the user clicked
                    for cords, bol in past_guesses:
                        if coords == cords: # cannot guess previously guessed locations (past tries)
                            return
                    for cords in selected_boxes:
                        if coords == cords: # cannot guess previously guessed locations (current tries, if more than 1)
                            return
                    selected_boxes.append(coords) # if everything ok, add guess to list

                else: # 1st part of the game, choosing your own ship locations
                    coords = (grid_boxes_left[row][column][0]+37, grid_boxes_left[row][column][1]+37) # determine acoording to previously defined grid box locations, which one the user clicked
                    if coords not in selected_boxes: # cannot choose previously chosen locations for ships
                        selected_boxes.append(coords) # if everything ok, add choice to list

    if player == 2 or player == 4: # if second player playing
        if mouse_pos[0] < 1375 and mouse_pos[0] > 850: # check if inside coordinates vertically of right grid
            if mouse_pos[1] > 105 and mouse_pos[1] < 630: # check if inside coordinates horizontally of right grid
                column = 6 - ((1375 - mouse_pos[0]) // 75) # calculate which column user clicked in
                row = 6 - ((630 - mouse_pos[1]) // 75) # calculate which row user clicked in

                if is_guessing: # 2nd part of the game, guessing oponent ship locations
                    coords = (grid_boxes_left[row][column][0]+37, grid_boxes_left[row][column][1]+37) # determine acoording to previously defined grid box locations, which one the user clicked
                    for cords, bol in past_guesses: # cannot guess previously guessed locations (past tries)
                        if coords == cords:
                            return
                    for cords in selected_boxes:
                        if coords == cords: # cannot guess previously guessed locations (current tries, if more than 1)
                            return
                    selected_boxes.append(coords) # if everything ok, add guess to list

                else: # 1st part of the game, choosing your own ship locations
                    coords = (grid_boxes_right[row][column][0]+37, grid_boxes_right[row][column][1]+37) # determine acoording to previously defined grid box locations, which one the user clicked
                    if coords not in selected_boxes: # cannot choose previously chosen locations for ships
                        selected_boxes.append(coords) # calculate which row user clicked in

def draw_grids(): # draw left and right-side grids

    x = 105
    y = 105

    while x <= 630: # draw left-side grid
        pygame.draw.rect(WIN, GREY, pygame.Rect(x, 105, 5, 530))
        x += 75
        pygame.draw.rect(WIN, GREY, pygame.Rect(105, y, 530, 5))
        y += 75

    x = 850
    y = 105

    while x <= 1375: # draw right-side grid
        pygame.draw.rect(WIN, GREY, pygame.Rect(x, 105, 5, 530))
        x += 75
        pygame.draw.rect(WIN, GREY, pygame.Rect(850, y, 530, 5))
        y += 75

def draw_secs(player_text : PLAYER_FONT, secs : int): # draw seconds left before restart
    pygame.draw.rect(WIN, BLUE, pygame.Rect((WIDTH // 2) - (player_text.get_width() // 2), (HEIGHT // 2) - (player_text.get_height() // 2) + 100, player_text.get_width(), player_text.get_height()))

    wait_text = PLAYER_FONT.render("Wait " + str(secs) + " seconds to play again.", 1, BLACK)
    WIN.blit(wait_text, ((WIDTH // 2) - (wait_text.get_width() // 2), (HEIGHT // 2) - (wait_text.get_height() // 2) + 100))

    pygame.display.update()


def draw_winner(player : int, secs : int): # create screen of winning player
    WIN.fill(BLUE)

    player_text = ""

    if player == 1:
        player_text = PLAYER_FONT.render("Player 2 won!", 1, BLACK)
    else:
        player_text = PLAYER_FONT.render("Player 1 won!", 1, BLACK)

    wait_text = PLAYER_FONT.render("Wait " + str(secs) + " seconds to play again.", 1, BLACK)

    WIN.blit(player_text, ((WIDTH // 2) - (player_text.get_width() // 2), (HEIGHT // 2) - (player_text.get_height() // 2)))
    WIN.blit(wait_text, ((WIDTH // 2) - (wait_text.get_width() // 2), (HEIGHT // 2) - (wait_text.get_height() // 2) + 100))

    pygame.display.update()

    pygame.time.delay(1000) # wait 5 seconds and start game again
    draw_secs(wait_text, 4)
    pygame.time.delay(1000)
    draw_secs(wait_text, 3)
    pygame.time.delay(1000)
    draw_secs(wait_text, 2)
    pygame.time.delay(1000)
    draw_secs(wait_text, 1)
    pygame.time.delay(1000)


def draw_game(mouse_pos : tuple, selected_boxes_1 : list, selected_boxes_2 : list, guess_box_1 : list, guess_box_2 : list, past_guesses_1 : list, past_guesses_2 : list, player : int, max_ship_choices : int, max_guesses : int): # 2nd part of game, players guessing
    if len(selected_boxes_1) == 0 or len(selected_boxes_2) == 0: # if someone guessed all right places, end game
        draw_winner(player, 5)
        return 10
    
    WIN.fill(BLUE)

    player1 = PLAYER_FONT.render("Player 1", 1, BLACK)
    player2 = PLAYER_FONT.render("Player 2", 1, BLACK)

    WIN.blit(player1, ((WIDTH // 4) - (player1.get_width() // 2), 40))
    WIN.blit(player2, ((WIDTH // 4) + (WIDTH // 2) - (player2.get_width() // 2), 40))

    draw_grids()

    pygame.draw.circle(WIN, RED, mouse_pos, 10)
    pygame.draw.rect(WIN, WHITE, BORDER)

    if player == 1 or player == 3: # if player 1 playing
        if len(guess_box_1) >= max_guesses: # if maximum number of guesses reached, show messages below
            max_choices_error = MAX_SHIPS_FONT.render("You have reached the maximum number of choices!", 1, RED)
            clear_choices = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_choices_error, (372 - (max_choices_error.get_width() // 2), 750))
            WIN.blit(clear_choices, (372 - (clear_choices.get_width() // 2), 800))
            WIN.blit(enter_continue, (372 - (enter_continue.get_width() // 2), 850))


        if len(guess_box_1) > 0:
            for guess in guess_box_1: # print current guesses
                pygame.draw.circle(WIN, BLACK, (guess[0] - 740, guess[1]), 20)

        for (guess, is_hit) in past_guesses_1: # print past guesses with according color, green for hit, red for miss
            if is_hit:
                pygame.draw.circle(WIN, GREEN, (guess[0] - 740, guess[1]), 20)
            else:
                pygame.draw.circle(WIN, RED, (guess[0] - 740, guess[1]), 20)

        hit = False
        if len(guess_box_2) > 0:
            for guess in guess_box_2:
                for box in selected_boxes_1:
                    if guess == box: # if guessed correct location
                        selected_boxes_1.remove(box) # remove ship for opponent's still living ships
                        hit = True
                        past_guesses_2.append((guess, hit)) # add to past guesses list

                if not hit:
                    hit = False
                    past_guesses_2.append((guess, hit)) # add to past guesses list


        guess_box_2.clear() # reset current guessing list

        pygame.draw.rect(WIN, BLACK, pygame.Rect(850, 105, 530, 530))                           # cover opponent's choices
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)    # cover opponent's choices
        WIN.blit(cannot_see, (1110 - (cannot_see.get_width() // 2), 330))                       # cover opponent's choices

        if player == 3: # if player pressed Enter but hasn't used all of his guesses
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected " + str(max_guesses) + " spot(s) for enemy ships.", 1, RED)
            WIN.blit(choose_more, (372 - (choose_more.get_width() // 2), 750))

    elif player == 2 or player == 4: # if player 2 playing
        if len(guess_box_2) >= max_guesses: # if maximum number of guesses reached, show messages below
            max_choices_error = MAX_SHIPS_FONT.render("You have reached the maximum number of choices!", 1, RED)
            clear_choices = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_choices_error, (1110 - (max_choices_error.get_width() // 2), 750))
            WIN.blit(clear_choices, (1110 - (clear_choices.get_width() // 2), 800))
            WIN.blit(enter_continue, (1110 - (enter_continue.get_width() // 2), 850))

        if len(guess_box_2) > 0:
            for guess in guess_box_2: # print current guesses
                pygame.draw.circle(WIN, BLACK, (guess[0] + 740, guess[1]), 20)

        for (guess, is_hit) in past_guesses_2: # print past guesses with according color, green for hit, red for miss
            if is_hit:
                pygame.draw.circle(WIN, GREEN, (guess[0] + 740, guess[1]), 20)
            else:
                pygame.draw.circle(WIN, RED, (guess[0] + 740, guess[1]), 20)

        hit = False
        if len(guess_box_1) > 0:
            for guess in guess_box_1:
                for box in selected_boxes_2:
                    if guess == box: # if guessed correct location
                        selected_boxes_2.remove(box) # remove ship for opponent's still living ships
                        hit = True
                        past_guesses_1.append((guess, hit)) # add to past guesses list

                if not hit:
                    hit = False
                    past_guesses_1.append((guess, hit)) # add to past guesses list

        guess_box_1.clear() # reset current guessing list

        pygame.draw.rect(WIN, BLACK, pygame.Rect(105, 105, 530, 530))                           # cover opponent's choices
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)    # cover opponent's choices
        WIN.blit(cannot_see, (372 - (cannot_see.get_width() // 2), 330))                        # cover opponent's choices

        if player == 4: # if player pressed Enter but hasn't used all of his guesses
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected " + str(max_guesses) + " spot(s) for enemy ships.", 1, RED)
            WIN.blit(choose_more, (1110 - (choose_more.get_width() // 2), 750))

    pygame.display.update()


def draw_window(mouse_pos, selected_boxes_1, selected_boxes_2, player, max_ship_choices): # 1st part of game, players choosing ship locations
    WIN.fill(BLUE)

    player1 = PLAYER_FONT.render("Player 1", 1, BLACK)
    player2 = PLAYER_FONT.render("Player 2", 1, BLACK)

    WIN.blit(player1, ((WIDTH // 4) - (player1.get_width() // 2), 40))
    WIN.blit(player2, ((WIDTH // 4) + (WIDTH // 2) - (player2.get_width() // 2), 40))

    draw_grids()

    pygame.draw.circle(WIN, RED, mouse_pos, 10)
    pygame.draw.rect(WIN, WHITE, BORDER)

    write_choices = MAX_SHIPS_FONT.render("Choose " + str(max_ship_choices) + " spots for your ships.", 1, RED)
    WIN.blit(write_choices, ((WIDTH//2) - (write_choices.get_width() // 2), 30))

    if player == 1 or player == 3: # if player 1 playing
        if len(selected_boxes_1) >= max_ship_choices: # if trying to select more locations than has permission to
            max_ships_error = MAX_SHIPS_FONT.render("You have reached the maximum number of ships!", 1, RED)
            clear_ships = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_ships_error, (372 - (max_ships_error.get_width() // 2), 750))
            WIN.blit(clear_ships, (372 - (clear_ships.get_width() // 2), 800))
            WIN.blit(enter_continue, (372 - (enter_continue.get_width() // 2), 850))

        for box in selected_boxes_1: # draw selected ship locations
            pygame.draw.circle(WIN, BLACK, box, 20)

        pygame.draw.rect(WIN, BLACK, pygame.Rect(850, 105, 530, 530))                           # cover opponent's choices
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)    # cover opponent's choices
        WIN.blit(cannot_see, (1110 - (cannot_see.get_width() // 2), 330))                       # cover opponent's choices

        if player == 3: # if player pressed Enter but hasn't used all of his choices
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected " + str(max_ship_choices) + " spots for ships.", 1, RED)
            WIN.blit(choose_more, (372 - (choose_more.get_width() // 2), 750))

    elif player == 2 or player == 4: # if player 2 playing
        if len(selected_boxes_2) >= max_ship_choices: # if trying to select more locations than has permission to
            max_ships_error = MAX_SHIPS_FONT.render("You have reached the maximum number of ships!", 1, RED)
            clear_ships = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_ships_error, (1110 - (max_ships_error.get_width() // 2), 750))
            WIN.blit(clear_ships, (1110 - (clear_ships.get_width() // 2), 800))
            WIN.blit(enter_continue, (1110 - (enter_continue.get_width() // 2), 850))

        for box in selected_boxes_2: # draw selected ship locations
            pygame.draw.circle(WIN, BLACK, box, 20)

        pygame.draw.rect(WIN, BLACK, pygame.Rect(105, 105, 530, 530))                           # cover opponent's choices
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)    # cover opponent's choices
        WIN.blit(cannot_see, (372 - (cannot_see.get_width() // 2), 330))                        # cover opponent's choices

        if player == 4: # if player pressed Enter but hasn't used all of his choices
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected " + str(max_ship_choices) + " spots for ships.", 1, RED)
            WIN.blit(choose_more, (1110 - (choose_more.get_width() // 2), 750))

    pygame.display.update()


def main(max_ship_choices, max_guesses):
    selected_boxes_1 = []
    selected_boxes_2 = []
    guess_box_1 = []
    guess_box_2 = []
    past_guesses_1 = []
    past_guesses_2 = []
    clock = pygame.time.Clock()
    player = 1
    run = True
    to_game = False
    while run:
        clock.tick(FPS) # set FPS to, in this case, 60
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window closed, close pygame
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if mouse left-click (used to select choice/guess location)
                    if not to_game: # if in first part of game (choosing ship locations)
                        if player == 1 or player == 3: # if player 1 playing
                            get_ship_grid_box(mouse_pos, selected_boxes_1, past_guesses_1, player, max_ship_choices, False)
                        elif player == 2 or player == 4: # if player 2 playing
                            get_ship_grid_box(mouse_pos, selected_boxes_2, past_guesses_1, player, max_ship_choices, False)

                    else: # if in second part of game (guessing opponent's ship locations)
                        if player == 1 or player == 3: # if player 1 playing
                            get_ship_grid_box(mouse_pos, guess_box_1, past_guesses_1, player, max_guesses, True)
                        elif player == 2 or player == 4: # if player 2 playing
                            get_ship_grid_box(mouse_pos, guess_box_2, past_guesses_2, player, max_guesses, True)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # if spacebar pressed (used to reset options (choices or guesses))
                    if not to_game: # if in first part of game (choosing ship locations)
                        if player == 1 or player == 3: # if player 1 playing
                            selected_boxes_1.clear() # reset ship location choices list 
                        elif player == 2 or player == 4: # if player 2 playing
                            selected_boxes_2.clear() # reset ship location choices list 

                    else: # if in second part of game (guessing opponent's ship locations)
                        if player == 1 or player == 3: # if player 1 playing
                            guess_box_1.clear() # reset guess location choices list
                        elif player == 2 or player == 4: # if player 2 playing
                            guess_box_2.clear() # reset guess location choices list

                if event.key == pygame.K_RETURN: # if enter pressed (used to confirm selection of choices/guesses)
                    if not to_game: # if in first part of game (choosing ship locations)
                        if player == 1: # if player 1 playing
                            if len(selected_boxes_1) == max_ship_choices: # if reached maximum number of choices
                                player = 2
                            else:
                                player = 3

                        elif player == 2: # if player 2 playing
                            if len(selected_boxes_2) == max_ship_choices: # if reached maximum number of choices
                                to_game = True # go to second part of game (guessing opponent's ships part)
                                player = 1
                            else:
                                player = 4
                    
                    else: # if in first part of game (choosing ship locations)
                        if player == 1: # if player 1 playing
                            if len(guess_box_1) == max_guesses: # if reached maximum number of guesses
                                player = 2
                            else:
                                player = 3

                        elif player == 2: # if player 2 playing
                            if len(guess_box_2) == max_guesses: # if reached maximum number of guesses
                                player = 1
                            else:
                                player = 4


        if not to_game: # if in first part of game (choosing ship locations)
            if len(selected_boxes_1) == max_ship_choices and player == 3: # if player 1 playing
                player = 1

            if len(selected_boxes_2) == max_ship_choices and player == 4: # if player 2 playing
                player = 2

        else:
            if len(guess_box_1) == max_guesses and player == 3: # if player 1 playing
                player = 1

            if len(guess_box_2) == max_guesses and player == 4: # if player 2 playing
                player = 2

        if to_game: # if in second part of game (guessing opponent's ship locations)
            if draw_game(mouse_pos, selected_boxes_1, selected_boxes_2, guess_box_1, guess_box_2, past_guesses_1, past_guesses_2, player, max_ship_choices, max_guesses) == 10: # if someone won
                run = False

        else: # if in first part of game (choosing ship locations)
            draw_window(mouse_pos, selected_boxes_1, selected_boxes_2, player, max_ship_choices)

    menu()

def choose_choices_num(ships_num): # select number of guessed per try
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # set FPS to, in this case, 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window closed, close pygame
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # if 1 pressed
                    main(ships_num, 1)
                    break
                elif event.key == pygame.K_2: # if 2 pressed
                    main(ships_num, 2)
                    break
                elif event.key == pygame.K_3: # if 3 pressed
                    main(ships_num, 3)
                    break

        WIN.fill(BLUE)

        ships_selected = MAX_SHIPS_FONT.render("You have selected " + str(ships_num) + " ships to add.", 1, RED)
        choose_choices = MAX_SHIPS_FONT.render("Choose the number of guesses you have, from 1 to 3.", 1, RED)
        press_num = MAX_SHIPS_FONT.render("Press the numbers to select.", 1, RED)

        WIN.blit(ships_selected, ((WIDTH // 2) - (ships_selected.get_width() // 2), (HEIGHT // 2) - (ships_selected.get_height() // 2) - 100))
        WIN.blit(choose_choices, ((WIDTH // 2) - (choose_choices.get_width() // 2), (HEIGHT // 2) - (choose_choices.get_height() // 2)))
        WIN.blit(press_num, ((WIDTH // 2) - (press_num.get_width() // 2), (HEIGHT // 2) - (press_num.get_height() // 2) + 100))

        pygame.display.update()

    pygame.quit()

def choose_ships_num(): # select number of ships to deploy
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # set FPS to, in this case, 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window closed, close pygame
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # if 1 pressed
                    choose_choices_num(1) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_2: # if 2 pressed
                    choose_choices_num(2) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_3: # if 3 pressed
                    choose_choices_num(3) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_4: # if 4 pressed
                    choose_choices_num(4) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_5: # if 5 pressed
                    choose_choices_num(5) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_6: # if 6 pressed
                    choose_choices_num(6) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_7: # if 7 pressed
                    choose_choices_num(7) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_8: # if 8 pressed
                    choose_choices_num(8) # go to choosing number of guessed menu
                    break
                elif event.key == pygame.K_9: # if 9 pressed
                    choose_choices_num(9) # go to choosing number of guessed menu
                    break

        WIN.fill(BLUE)

        choose_ships = MAX_SHIPS_FONT.render("Choose the number of ships to add, from 1 to 9.", 1, RED)
        press_num = MAX_SHIPS_FONT.render("Press the numbers to select.", 1, RED)

        WIN.blit(choose_ships, ((WIDTH // 2) - (choose_ships.get_width() // 2), (HEIGHT // 2) - (choose_ships.get_height() // 2)))
        WIN.blit(press_num, ((WIDTH // 2) - (press_num.get_width() // 2), (HEIGHT // 2) - (press_num.get_height() // 2) + 100))

        pygame.display.update()

    pygame.quit()



def menu():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # set FPS to, in this case, 60

        WIN.blit(MENU, (0, 0)) # show menu image
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window closed, close pygame
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # if 1 pressed
                    choose_ships_num() # go to choosing number of ships menu
                    run = False

    pygame.quit()

if __name__ == "__main__":
    menu()