import pygame
import sys
import ctypes
import pygame.mixer

pygame.init()
pygame.mixer.init()

RED = (255, 93, 115)
MILK = (241, 255, 231)
PINK = (239, 185, 203)
PURPLE = (72, 60, 70)
CHROME = (50, 162, 135)
MARSALA = (108, 70, 78)

font = pygame.font.SysFont("Arial", 25, bold=True)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
history_rect = pygame.Rect(150, 380, 500, 300)
history_surface = pygame.Surface((history_rect.width, history_rect.height))

FPS = 60
digit_count = 4

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bulls and cows")

buttons = [
    {"text": "PLAY", "rect": pygame.Rect(150, 220, 200, 50)},
    {"text": "SETTINGS", "rect": pygame.Rect(150, 290, 200, 50)},
    {"text": "EXIT", "rect": pygame.Rect(150, 360, 200, 50)}
]

bull_icon = pygame.image.load("C:/Users/Дана/Bulls_and_cows/Assets/bull.png")
bull_icon = pygame.transform.scale(bull_icon, (50, 50))

cow_icon = pygame.image.load("C:/Users/Дана/Bulls_and_cows/Assets/cow.png")
cow_icon = pygame.transform.scale(cow_icon, (50, 50))

win_sound = pygame.mixer.Sound("C:/Users/Дана/Bulls_and_cows/Assets/level-win-6416.mp3")
win_sound.set_volume(0.7)
tap_sound = pygame.mixer.Sound("C:/Users/Дана/Bulls_and_cows/Assets/ui-click-43196.mp3")
tap_sound.set_volume(0.7)

game_lib = ctypes.CDLL("C:/Users/Дана/Bulls_and_cows/bulls_cows.so")
game_lib.create_game.argtypes = None
game_lib.create_game.restype = ctypes.POINTER(ctypes.c_void_p)
game_lib.delete_game.argtypes = [ctypes.c_void_p]
game_lib.delete_game.restype = None
start = game_lib.initialize_game
game_lib.initialize_game.argtypes = [ctypes.c_void_p, ctypes.c_int]
game_lib.initialize_game.restype = None
isValid = game_lib.validate_guess
game_lib.validate_guess.argtypes = [ctypes.c_char_p, ctypes.c_int]
game_lib.validate_guess.restype = ctypes.c_bool

class Result(ctypes.Structure):
    _fields_ = [("bulls", ctypes.c_int), ("cows", ctypes.c_int)]

check = game_lib.check_guess
game_lib.check_guess.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
game_lib.check_guess.restype = Result


def create_text(text, color, font):
    return font.render(text, True, color)

def draw_menu():
    screen.fill(PINK)

    title_surf = create_text("Welcome", MILK, title_font)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)

    for button in buttons:
        shadow_rect = button["rect"].copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, PURPLE, shadow_rect, border_radius=10)
        pygame.draw.rect(screen, MARSALA, button["rect"], border_radius=10)
        text_surf = create_text(button["text"], MILK, font)
        text_rect = text_surf.get_rect(center=button["rect"].center)
        screen.blit(text_surf, text_rect)

def draw_settings():
    screen.fill(CHROME)

    title_surf = create_text("Settings", MILK, title_font)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)

    count_surf = create_text(f"Digits: {digit_count}", MILK, font)
    count_rect = count_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(count_surf, count_rect)

    inc_button = pygame.Rect(WIDTH // 2 + 80, HEIGHT // 2 - 70, 40, 40)
    dec_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 - 70, 40, 40)
    pygame.draw.rect(screen, MARSALA, inc_button, border_radius=10)
    pygame.draw.rect(screen, MARSALA, dec_button, border_radius=10)

    inc_text = create_text("+", MILK, font)
    inc_text_rect = inc_text.get_rect(center=inc_button.center)
    screen.blit(inc_text, inc_text_rect)

    dec_text = create_text("-", MILK, font)
    dec_text_rect = dec_text.get_rect(center=dec_button.center)
    screen.blit(dec_text, dec_text_rect)

    back_button = pygame.Rect(10, 10, 50, 40)
    pygame.draw.rect(screen, MARSALA, back_button, border_radius=10)
    pygame.draw.polygon(screen, MILK, [
        (back_button.left + 10, back_button.centery),
        (back_button.right - 10, back_button.top + 10),
        (back_button.right - 10, back_button.bottom - 10)
    ])

    return inc_button, dec_button, back_button

def draw_game(input_text, bulls, cows, history, scroll_offset, invalid_input):
    screen.fill(CHROME)

    title_surf = create_text("Bulls and Cows", MILK, title_font)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surf, title_rect)

    input_rect = pygame.Rect(150, 150, 200, 50)
    input_color = (255, 100, 100) if invalid_input else MILK  
    pygame.draw.rect(screen, input_color, input_rect, border_radius=10)

    input_surf = font.render(input_text, True, CHROME)
    input_rect_text = input_surf.get_rect(midleft=(input_rect.x + 10, input_rect.centery))
    screen.blit(input_surf, input_rect_text)

    submit_button = pygame.Rect(150, 220, 200, 50)
    pygame.draw.rect(screen, MARSALA, submit_button, border_radius=10)
    submit_text = create_text("Submit", MILK, font)
    submit_rect = submit_text.get_rect(center=submit_button.center)
    screen.blit(submit_text, submit_rect)

    back_button = pygame.Rect(10, 10, 50, 40)
    pygame.draw.rect(screen, MARSALA, back_button, border_radius=10)
    pygame.draw.polygon(screen, MILK, [
        (back_button.left + 10, back_button.centery),
        (back_button.right - 10, back_button.top + 10),
        (back_button.right - 10, back_button.bottom - 10)
    ])

    result_y = 300
    x_offset = 150
    for i in range(bulls):
        screen.blit(bull_icon, (x_offset + i * 60, result_y))
    x_offset += bulls * 60
    for i in range(cows):
        screen.blit(cow_icon, (x_offset + i * 60, result_y))    

    history_surface.fill(CHROME)
    history_y = scroll_offset

    for attempt, (guess, bulls, cows) in enumerate(history, start=1):
        history_text = f"{attempt:02}:  {guess}     " + "B" * bulls + "C" * cows  # Додано більше пробілів
        history_surf = font.render(history_text, True, MILK)
        history_surface.blit(history_surf, (50, history_y))
        history_y += 30
    
    screen.blit(history_surface, history_rect.topleft, (0, 0, history_rect.width, history_rect.height))

    return input_rect, submit_button, back_button

def winner_popup(history, digit_count):
    win_sound.play()
    popup_surface = pygame.Surface((400, 200))
    popup_surface.fill((PINK))
    pygame.draw.rect(popup_surface, MILK, popup_surface.get_rect(), 5)

    message = f"You guessed the number in {len(history)} attempts!"
    popup_text = font.render(message, True, MILK)
    popup_rect = popup_text.get_rect(center=popup_surface.get_rect().center)
    popup_surface.blit(popup_text, popup_rect)

    screen.blit(popup_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

def draw_confirmation_win():
    window_width, window_height = 400, 200
    window_rect = pygame.Rect((WIDTH // 2 - window_width // 2, HEIGHT // 2 - window_height // 2, window_width, window_height))
    pygame.draw.rect(screen, MILK, window_rect, border_radius=10)
    pygame.draw.rect(screen, PURPLE, window_rect, width=3, border_radius=10)

    question_text = create_text("The game will be quitted. Are you sure?", CHROME, font)
    question_rect = question_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(question_text, question_rect)

    yes_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 30, 80, 40)
    pygame.draw.rect(screen, MARSALA, yes_button, border_radius=10)
    yes_text = create_text("Yes", MILK, font)
    yes_rect = yes_text.get_rect(center=yes_button.center)
    screen.blit(yes_text, yes_rect)

    no_button = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 30, 80, 40)
    pygame.draw.rect(screen, MARSALA, no_button, border_radius=10)
    no_text = create_text("No", MILK, font)
    no_rect = no_text.get_rect(center=no_button.center)
    screen.blit(no_text, no_rect)

    return yes_button, no_button


def main():
    global digit_count
    clock = pygame.time.Clock()
    run = True
    in_settings = False
    in_game = False
    input_text = ""
    bulls, cows = 0, 0
    game = None
    history = []
    scroll_offset = 0
    confirm_quit = False
    invalid_input = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if in_settings:
                    inc_button, dec_button, back_button = draw_settings()
                    if inc_button.collidepoint(mouse_pos):
                        tap_sound.play()
                        digit_count += 1
                    elif dec_button.collidepoint(mouse_pos) and digit_count > 1:
                        tap_sound.play()
                        digit_count -= 1
                    elif back_button.collidepoint(mouse_pos):
                        tap_sound.play()
                        in_settings = False
                elif in_game:
                    if confirm_quit:
                        yes_button, no_button = draw_confirmation_win()
                        if yes_button.collidepoint(mouse_pos):
                            tap_sound.play()
                            history.clear()
                            if game:
                                game_lib.delete_game(game)
                                game = None
                            in_game = False
                            confirm_quit = False
                        elif no_button.collidepoint(mouse_pos):
                            tap_sound.play()
                            confirm_quit = False
                    else:
                        input_rect, submit_button, back_b = draw_game(input_text, bulls, cows, history, scroll_offset, invalid_input)
                        if submit_button.collidepoint(mouse_pos):
                            tap_sound.play()
                            if len(input_text) == digit_count and isValid(input_text.encode(), len(input_text)):
                                result = check(game, input_text.encode())
                                bulls, cows = result.bulls, result.cows
                                history.append((input_text, bulls, cows))
                                input_text = ""
                                invalid_input = False
                                print(f"Bulls: {bulls}, cows: {cows}")

                                if bulls == digit_count:
                                    winner_popup(history, digit_count)
                                    pygame.display.update()
                                    pygame.time.wait(3000)
                                    history.clear()
                                    game_lib.delete_game(game)
                                    in_game = False
                            else:
                                invalid_input = True
                                print("Invalid guess!")    
                        elif back_b.collidepoint(mouse_pos):
                            tap_sound.play()
                            confirm_quit = True
                else:
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            tap_sound.play()
                            if button["text"] == "PLAY":
                                print(f"Starting game with {digit_count} digits...")
                                game = game_lib.create_game()
                                start(game,digit_count)
                                bulls, cows = 0, 0
                                input_text = ""
                                in_game = True
                            elif button["text"] == "SETTINGS":
                                in_settings = True
                            elif button["text"] == "EXIT":
                                run = False

            if in_game and not confirm_quit and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                invalid_input = False

            if in_game and event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * 30
                scroll_offset = min(scroll_offset, 0)
                max_scroll = -(len(history) * 30 - history_rect.height)
                scroll_offset = max(scroll_offset, max_scroll)
        
        if in_settings:
            draw_settings()
        elif in_game:
            if confirm_quit:
                draw_confirmation_win()
            else:
                draw_game(input_text, bulls, cows, history, scroll_offset, invalid_input)
        else:
            draw_menu()
        pygame.display.flip()

    if game:
        game_lib.delete_game(game)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
