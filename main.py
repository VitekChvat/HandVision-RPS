import time

import cv2
import mediapipe as mp

import pygame
import sys

import random

"""AI - proměnné - Začátek"""

# Inicializace MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Zapnutí kamery
cap = cv2.VideoCapture(0)
"""AI - proměnné - Konec"""


"""Pygame - proměnné - Začátek"""
# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kámen - Nůžky - Papír")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Herní smyčka
running = True

# FPS
FPS = 60
clock = pygame.time.Clock()

# Načtení obrázku
# Nahraď 'obrazek.png' tvým souborem v projektu
paper = pygame.image.load("Images/Paper").convert_alpha()
red_cross = pygame.image.load("Images/RedCross.png").convert_alpha()
rock = pygame.image.load("Images/Rock.webp").convert_alpha()
scisors = pygame.image.load("Images/Scisors.webp").convert_alpha()
continuee = pygame.image.load("Images/Continue.jpg").convert_alpha()
question_mark = pygame.image.load("Images/QuestionMark.png").convert_alpha()

# Změna velikosti obrázku (například na 200x200 px)
paper_resized = pygame.transform.scale(paper, (200, 200))
red_cross_resized = pygame.transform.scale(red_cross, (200, 200))
rock_resized = pygame.transform.scale(rock, (200, 200))
scisors_resized = pygame.transform.scale(scisors, (200, 200))
continuee_resized = pygame.transform.scale(continuee, (500, 700))
question_mark_resized = pygame.transform.scale(question_mark, (200, 200))

# Font a text
pygame.font.init()
font = pygame.font.SysFont(None, 48)  # (název fontu, velikost) None=default
text_surface = font.render("YOU" + (" "*38) + "BOT", True, BLACK)
text_surface_2 = font.render("TO CONTINUE", True, BLACK)
text_surface_3 = font.render("VS", True, RED)
# text_surface_4 je už zabraná
text_surface_5 = font.render("TO START", True, BLACK)
# text_surface_6 je už zabraná

# Pro logiku hry
continue_boolean = False
round_finish = False

# Časovač
start_ticks = 0
countdown = 5  # počáteční hodnota v sekundách

# Jestli hra teprve začla
game_start = True

# Proměnné pro bota
gestures_list = ["kamen", "nuzky", "papir"]
bot_choice = ""
bot_allready_choiced = False
gestures_list_for_results = ["kamen", "nuzky", "papir", "kamen"]

# Proměnné potřebné pro kontrolování výhry
winner = ""
score_list = [0, 0]

"""Pygame - proměnné - Konec"""

# Gesto pro kámen, nůžky, papír
gesture = ""

while running:
    """AI - Kód - Začátek"""
    ret, frame = cap.read()
    if not ret:
        break

    # Zrcadlové otočení pro přirozené ovládání
    frame = cv2.flip(frame, 1)

    # Konverze barev BGR  -> RGB pro MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Kreslení bodů a spojnic na ruce
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Seznam všech bodů (landmarks)
            landmarks = hand_landmarks.landmark

            # Logika pro zjištění počtu zvednutých prstů
            fingers = []

            # Palec (x souřadnice)
            if landmarks[4].x < landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Ostatní prsty (y souřadnice)
            for tip_id in [8, 12, 16, 20]:
                if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            """total_fingers = sum(fingers)
            print("Počet zvednutých prstů:", total_fingers)"""

            # Zjistění gesta uživatele
            if sum(fingers[1:]) == 4:
                gesture = "papir"
            elif sum(fingers[1:]) == 0:
                gesture = "kamen"
            elif fingers[1] == 1 and fingers[2] == 1:
                gesture = "nuzky"
            elif fingers[1] == 1:
                gesture = "pokracovani"
            else:
                gesture = "nic"

    cv2.imshow("Kamen - Nuzky - Papir - (kamera)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC pro ukončení
        running = False
    """AI - Kód - Konec"""


    """Pygame - Kód - Začátek"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vyčištění obrazovky
    screen.fill(WHITE)

    # Logika hry + Kreslení
    if continue_boolean:
        if gesture == "papir": screen.blit(paper_resized, (50, 70))
        if gesture == "kamen": screen.blit(rock_resized, (50, 70))
        if gesture == "nuzky": screen.blit(scisors_resized, (50, 70))
        if gesture == "nic" or gesture == "pokracovani": screen.blit(red_cross_resized, (50, 70))

        screen.blit(text_surface, (100, 20))
        screen.blit(text_surface_3, (330, 150))

        # Výpočet odpočtu
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000  # převedení na sekundy
        remaining = max(0, countdown - int(seconds_passed))  # zbývající čas, nejméně 0
        # Render textu
        text_surface_4 = font.render(str(remaining) + "s", True, GREEN)
        screen.blit(text_surface_4, (330, 20))

        if remaining == 0:
            # Ukazování obrázků u bota
            if bot_choice == "papir": screen.blit(paper_resized, (450, 70))
            if bot_choice == "kamen": screen.blit(rock_resized, (450, 70))
            if bot_choice == "nuzky": screen.blit(scisors_resized, (450, 70))

            # Kontrola vyher, proher, remíz
            for i in range(len(gestures_list_for_results) - 1):
                if (gestures_list_for_results[i] == bot_choice and gestures_list_for_results[i+1] == gesture) or gesture == "nic":
                    winner = "bot"
                    score_list[0] += 1
                    break
                elif gestures_list_for_results[i] == gesture and gestures_list_for_results[i+1] == bot_choice:
                    winner = "user"
                    score_list[1] += 1
                    break
                elif gestures_list_for_results[i] == gesture and gestures_list_for_results[i] == bot_choice:
                    winner = "none"
                    break

            # Resetování hodnot
            continue_boolean = False
            gesture = ""
            bot_allready_choiced = False
            round_finish = True

        else:
            screen.blit(question_mark_resized, (450, 70))

    else:
        screen.blit(continuee_resized, (100, -150))

        if game_start:  screen.blit(text_surface_5, (280, 370))
        else: screen.blit(text_surface_2, (250, 370))

        if gesture == "pokracovani":
            continue_boolean = True
            game_start = False
            start_ticks = pygame.time.get_ticks()  # aktuální čas při startu

        if not bot_allready_choiced:
            bot_choice = random.choice(gestures_list)
            bot_allready_choiced = True

    # Zobrazování skóre
    text_surface_6 = font.render("SCORE:" + (" "*15) + "YOU: " + str(score_list[1]) + (" "*16) + "BOT: " + str(score_list[0]), True, BLACK)
    screen.blit(text_surface_6, (20, 460))

    # Aktualizace obrazovky
    pygame.display.flip()

    if round_finish:
        # Chvilku pauza, aby se mohl uživatel podívat na výsledky
        time.sleep(1)
        # Animace blikání
        if winner == "bot":
            for i in range(2):
                pygame.draw.rect(screen, GREEN, (350, 0, 350, 500))
                pygame.draw.rect(screen, RED, (0, 0, 350, 500))
                pygame.display.flip()
                time.sleep(0.25)
                screen.fill(WHITE)
                pygame.display.flip()
                time.sleep(0.25)
        elif winner == "user":
            for i in range(2):
                pygame.draw.rect(screen, RED, (350, 0, 350, 500))
                pygame.draw.rect(screen, GREEN, (0, 0, 350, 500))
                pygame.display.flip()
                time.sleep(0.25)
                screen.fill(WHITE)
                pygame.display.flip()
                time.sleep(0.25)
        elif winner == "none":
            for i in range(2):
                pygame.draw.rect(screen, YELLOW, (0, 0, 700, 500))
                pygame.display.flip()
                time.sleep(0.25)
                screen.fill(WHITE)
                pygame.display.flip()
                time.sleep(0.25)

        round_finish = False

    # FPS limit
    clock.tick(FPS)
    """Pygame - Kód - Konec"""

cap.release()
cv2.destroyAllWindows()

# Ukončení Pygame
pygame.quit()
sys.exit()
