import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

MAX_SHIPS_FONT = pygame.font.SysFont('comicsans', 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (69, 139, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (139, 69, 0)
GREY = (131, 139, 139)

MAX_SHIP_CHOICES = 3
MAX_GUESSES = 1

grid_boxes_left = [
    [(110, 110), (185, 110), (260, 110), (335, 110), (410, 110), (485, 110), (560, 110)],
    [(110, 185), (185, 185), (260, 185), (335, 185), (410, 185), (485, 185), (560, 185)],
    [(110, 260), (185, 260), (260, 260), (335, 260), (410, 260), (485, 260), (560, 260)],
    [(110, 335), (185, 335), (260, 335), (335, 335), (410, 335), (485, 335), (560, 335)],
    [(110, 410), (185, 410), (260, 410), (335, 410), (410, 410), (485, 410), (560, 410)],
    [(110, 485), (185, 485), (260, 485), (335, 485), (410, 485), (485, 485), (560, 485)],
    [(110, 560), (185, 560), (260, 560), (335, 560), (410, 560), (485, 560), (560, 560)]
    ]

grid_boxes_right = [
    [(850, 110), (925, 110), (1000, 110), (1075, 110), (1150, 110), (1225, 110), (1300, 110)],
    [(850, 185), (925, 185), (1000, 185), (1075, 185), (1150, 185), (1225, 185), (1300, 185)],
    [(850, 260), (925, 260), (1000, 260), (1075, 260), (1150, 260), (1225, 260), (1300, 260)],
    [(850, 335), (925, 335), (1000, 335), (1075, 335), (1150, 335), (1225, 335), (1300, 335)],
    [(850, 410), (925, 410), (1000, 410), (1075, 410), (1150, 410), (1225, 410), (1300, 410)],
    [(850, 485), (925, 485), (1000, 485), (1075, 485), (1150, 485), (1225, 485), (1300, 485)],
    [(850, 560), (925, 560), (1000, 560), (1075, 560), (1150, 560), (1225, 560), (1300, 560)]
    ]

FPS = 60

def get_ship_grid_box(mouse_pos : tuple, selected_boxes : list, player : int, max_choices : int):
    if len(selected_boxes) >= max_choices:
        return
    if mouse_pos[0] < 630 and mouse_pos[0] > 105 and (player == 1 or player == 3):
        if mouse_pos[1] > 105 and mouse_pos[1] < 630:
            column = 6 - ((630 - mouse_pos[0]) // 75)
            row = 6 - ((630 - mouse_pos[1]) // 75)
            #print("Row: " + str(row) + " Column: " + str(column))
            #print("[0]: " + str(grid_boxes_left[row][column][0]) + " [1]: " + str(grid_boxes_left[row][column][1]))
            selected_boxes.append((grid_boxes_left[row][column][0]+37, grid_boxes_left[row][column][1]+37))
    elif mouse_pos[0] < 1375 and mouse_pos[0] > 850 and (player == 2 or player == 4):
        if mouse_pos[1] > 105 and mouse_pos[1] < 630:
            column = 6 - ((1375 - mouse_pos[0]) // 75)
            row = 6 - ((630 - mouse_pos[1]) // 75)
            #print("Row: " + str(row) + " Column: " + str(column))
            #print("Mouse pos: " + str(mouse_pos[0]) + "," + str(mouse_pos[1]))
            selected_boxes.append((grid_boxes_right[row][column][0]+37, grid_boxes_right[row][column][1]+37))

def draw_grids():
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


def draw_game(mouse_pos : tuple, selected_boxes_1 : list, selected_boxes_2 : list, guess_box_1 : list, guess_box_2 : list, past_guesses_1 : list, past_guesses_2 : list, player : int):
    if len(selected_boxes_1) == 0 or len(selected_boxes_2) == 0:
        pygame.quit()
    
    WIN.fill(BLUE)

    draw_grids()

    pygame.draw.circle(WIN, RED, mouse_pos, 10)
    pygame.draw.rect(WIN, WHITE, BORDER)

    if player == 1 or player == 3:
        if len(guess_box_1) >= MAX_GUESSES:
            max_choices_error = MAX_SHIPS_FONT.render("You have reached the maximum number of choices!", 1, RED)
            clear_choices = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_choices_error, (372 - (max_choices_error.get_width() // 2), 750))
            WIN.blit(clear_choices, (372 - (clear_choices.get_width() // 2), 800))
            WIN.blit(enter_continue, (372 - (enter_continue.get_width() // 2), 850))

        if len(guess_box_1) > 0:
            pygame.draw.circle(WIN, BLACK, guess_box_1[0], 20)

        for (guess, is_hit) in past_guesses_1:
            if is_hit:
                pygame.draw.circle(WIN, GREEN, guess, 20)
            else:
                pygame.draw.circle(WIN, RED, guess, 20)

        hit = False
        if len(guess_box_2) > 0:
            for box in selected_boxes_1:
                if guess_box_2[0] == box:
                    selected_boxes_1.remove(box)
                    hit = True
        if hit and len(guess_box_2) > 0:
            past_guesses_2.append((guess_box_2[0], True))
        elif not hit and len(guess_box_2) > 0:
            past_guesses_2.append((guess_box_2[0], False))

        guess_box_2.clear()

        pygame.draw.rect(WIN, BLACK, pygame.Rect(850, 105, 530, 530))
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)
        WIN.blit(cannot_see, (1110 - (cannot_see.get_width() // 2), 330))

        if player == 3:
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected 1 spot for enemy ships.", 1, RED)
            WIN.blit(choose_more, (372 - (choose_more.get_width() // 2), 750))

    elif player == 2 or player == 4:
        if len(guess_box_2) >= MAX_GUESSES:
            max_choices_error = MAX_SHIPS_FONT.render("You have reached the maximum number of choices!", 1, RED)
            clear_choices = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_choices_error, (1110 - (max_choices_error.get_width() // 2), 750))
            WIN.blit(clear_choices, (1110 - (clear_choices.get_width() // 2), 800))
            WIN.blit(enter_continue, (1110 - (enter_continue.get_width() // 2), 850))

        if len(guess_box_2) > 0:
            pygame.draw.circle(WIN, BLACK, guess_box_2[0], 20)

        for (guess, is_hit) in past_guesses_2:
            if is_hit:
                pygame.draw.circle(WIN, GREEN, guess, 20)
            else:
                pygame.draw.circle(WIN, RED, guess, 20)

        hit = False
        if len(guess_box_1) > 0:
            for box in selected_boxes_2:
                if guess_box_1[0] == box:
                    selected_boxes_2.remove(box)
                    hit = True
        if hit and len(guess_box_1) > 0:
            past_guesses_1.append((guess_box_1[0], True))
        elif not hit and len(guess_box_1) > 0:
            past_guesses_1.append((guess_box_1[0], False))

        guess_box_1.clear()

        pygame.draw.rect(WIN, BLACK, pygame.Rect(105, 105, 530, 530))
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)
        WIN.blit(cannot_see, (372 - (cannot_see.get_width() // 2), 330))

        if player == 4:
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected 1 spot for enemy ships.", 1, RED)
            WIN.blit(choose_more, (1110 - (choose_more.get_width() // 2), 750))

    pygame.display.update()


def draw_window(mouse_pos, selected_boxes_1, selected_boxes_2, player):
    WIN.fill(BLUE)

    draw_grids()

    pygame.draw.circle(WIN, RED, mouse_pos, 10)
    pygame.draw.rect(WIN, WHITE, BORDER)

    if player == 1 or player == 3:
        if len(selected_boxes_1) >= MAX_SHIP_CHOICES:
            max_ships_error = MAX_SHIPS_FONT.render("You have reached the maximum number of ships!", 1, RED)
            clear_ships = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_ships_error, (372 - (max_ships_error.get_width() // 2), 750))
            WIN.blit(clear_ships, (372 - (clear_ships.get_width() // 2), 800))
            WIN.blit(enter_continue, (372 - (enter_continue.get_width() // 2), 850))

        for box in selected_boxes_1:
            pygame.draw.circle(WIN, BLACK, box, 20)

        pygame.draw.rect(WIN, BLACK, pygame.Rect(850, 105, 530, 530))
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)
        WIN.blit(cannot_see, (1110 - (cannot_see.get_width() // 2), 330))

        if player == 3:
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected 3 spots for ships.", 1, RED)
            WIN.blit(choose_more, (372 - (choose_more.get_width() // 2), 750))

    elif player == 2 or player == 4:
        if len(selected_boxes_2) >= MAX_SHIP_CHOICES:
            max_ships_error = MAX_SHIPS_FONT.render("You have reached the maximum number of ships!", 1, RED)
            clear_ships = MAX_SHIPS_FONT.render("To clear selections, press spacebar.", 1, RED)
            enter_continue = MAX_SHIPS_FONT.render("To continue, press Enter.", 1, RED)
            WIN.blit(max_ships_error, (1110 - (max_ships_error.get_width() // 2), 750))
            WIN.blit(clear_ships, (1110 - (clear_ships.get_width() // 2), 800))
            WIN.blit(enter_continue, (1110 - (enter_continue.get_width() // 2), 850))

        for box in selected_boxes_2:
            pygame.draw.circle(WIN, BLACK, box, 20)

        pygame.draw.rect(WIN, BLACK, pygame.Rect(105, 105, 530, 530))
        cannot_see = MAX_SHIPS_FONT.render("You cannot see the opponent's choices!", 1, RED)
        WIN.blit(cannot_see, (372 - (cannot_see.get_width() // 2), 330))

        if player == 4:
            choose_more = MAX_SHIPS_FONT.render("You have not yet selected 3 spots for ships.", 1, RED)
            WIN.blit(choose_more, (1110 - (choose_more.get_width() // 2), 750))

    pygame.display.update()


def main():
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
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not to_game:
                        if player == 1 or player == 3:
                            get_ship_grid_box(mouse_pos, selected_boxes_1, player, MAX_SHIP_CHOICES)
                        elif player == 2 or player == 4:
                            get_ship_grid_box(mouse_pos, selected_boxes_2, player, MAX_SHIP_CHOICES)
                    else:
                        if player == 1 or player == 3:
                            get_ship_grid_box(mouse_pos, guess_box_1, player, MAX_GUESSES)
                        elif player == 2 or player == 4:
                            get_ship_grid_box(mouse_pos, guess_box_2, player, MAX_GUESSES)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not to_game:
                        if player == 1 or player == 3:
                            selected_boxes_1.clear()
                        elif player == 2 or player == 4:
                            selected_boxes_2.clear()
                    else:
                        if player == 1 or player == 3:
                            guess_box_1.clear()
                        elif player == 2 or player == 4:
                            guess_box_2.clear()

                if event.key == pygame.K_RETURN:
                    if not to_game:
                        if player == 1:
                            if len(selected_boxes_1) == 3:
                                player = 2
                            else:
                                player = 3
                        elif player == 2:
                            if len(selected_boxes_2) == 3:
                                to_game = True
                                player = 1
                            else:
                                player = 4
                    
                    else:
                        if player == 1:
                            if len(guess_box_1) == MAX_GUESSES:
                                player = 2
                            else:
                                player = 3
                        elif player == 2:
                            if len(guess_box_2) == MAX_GUESSES:
                                player = 1
                            else:
                                player = 4


        if not to_game:
            if len(selected_boxes_1) == MAX_SHIP_CHOICES and player == 3:
                player = 1

            if len(selected_boxes_2) == MAX_SHIP_CHOICES and player == 4:
                player = 2
        else:
            if len(guess_box_1) == MAX_GUESSES and player == 3:
                player = 1

            if len(guess_box_2) == MAX_GUESSES and player == 4:
                player = 2
        #print(str(player))

        if to_game:
            draw_game(mouse_pos, selected_boxes_1, selected_boxes_2, guess_box_1, guess_box_2, past_guesses_1, past_guesses_2, player)
        else:
            draw_window(mouse_pos, selected_boxes_1, selected_boxes_2, player)

    pygame.quit()

if __name__ == "__main__":
    main()