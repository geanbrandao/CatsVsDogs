
import pygame
import os

# init
pygame.init()
pygame.mixer.init()

# screen setup
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gato vs Cachorro(s ??)")

# colors
BACKGROUND_COLOR = (109, 196, 241)
FONT_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont("consolas", 28, bold=True)
FONT_SMALLER = pygame.font.SysFont("consolar", 24)

# speed control
BG1_SPEED = 1
BG2_SPEED = 2
FLOOR_SPEED = 5
GRAVITY = 1.0

# load assets
def load_assets():
    img_path = os.path.join("assets", "imgs")

    cat_frames = [
        pygame.image.load(os.path.join(img_path, "cat_01.png")),
        pygame.image.load(os.path.join(img_path, "cat_02.png"))
    ]
    cat_jump = pygame.image.load(os.path.join(img_path, "cat_jumping.png"))
    dog_frames = [
        pygame.image.load(os.path.join(img_path, "dog_01.png")),
        pygame.image.load(os.path.join(img_path, "dog_02.png")),
        pygame.image.load(os.path.join(img_path, "dog_03.png"))
    ]
    floor_img = pygame.image.load(os.path.join(img_path, "floor.png"))
    bg1 = pygame.image.load(os.path.join(img_path, "background_01.png"))
    bg2 = pygame.image.load(os.path.join(img_path, "background_02.png"))

    cat_frames = [pygame.transform.scale(img, (64, 64)) for img in cat_frames]
    cat_jump = pygame.transform.scale(cat_jump, (64, 64))
    dog_frames = [pygame.transform.scale(img, (80, 60)) for img in dog_frames]
    floor_img = pygame.transform.scale(floor_img, (1920, 69))
    bg1 = pygame.transform.scale(bg1, (1920, 438))
    bg2 = pygame.transform.scale(bg2, (1920, 500))

    return cat_frames, cat_jump, dog_frames, floor_img, bg1, bg2

def load_sounds():
    sound_path = os.path.join("assets", "sounds")
    jump_sound = pygame.mixer.Sound(os.path.join(sound_path, "cat_jump.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(sound_path, "game_over.wav"))
    background_music = os.path.join(sound_path, "background.wav")
    return jump_sound, game_over_sound, background_music

# reset game stats
def reset_game():
    return {
        "cat_x": 100,
        "cat_y": HEIGHT - 100,
        "cat_vel_y": 0,
        "is_jumping": False,
        "dog_x": WIDTH,
        "dog_speed": 5,
        "score": 0,
        "bg1_x": 0,
        "bg2_x": 0,
        "floor_x": 0,
        "game_over": False,
        "game_started": False,
        "paused": False
    }

# handle user input
def handle_input(state, jump_sound):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not state["game_started"]:
            state["game_started"] = True
        elif not state["is_jumping"]:
            jump_sound.play()
            state["cat_vel_y"] = -20
            state["is_jumping"] = True

# update assets position
def update_cat_position(state):
    if state["is_jumping"]:
        state["cat_y"] += state["cat_vel_y"]
        state["cat_vel_y"] += GRAVITY

        if state["cat_y"] >= HEIGHT - 100:
            state["cat_y"] = HEIGHT - 100
            state["is_jumping"] = False
            state["cat_vel_y"] = 0

def update_dog_position(state):
    state["dog_x"] -= state["dog_speed"]
    if state["dog_x"] < -80:
        state["dog_x"] = WIDTH + 100

def update_background_positions(state):
    state["bg1_x"] -= BG1_SPEED
    state["bg2_x"] -= BG2_SPEED
    state["floor_x"] -= FLOOR_SPEED

    if state["bg1_x"] <= -1920:
        state["bg1_x"] = 0
    if state["bg2_x"] <= -1920:
        state["bg2_x"] = 0
    if state["floor_x"] <= -1920:
        state["floor_x"] = 0

# draw assets
def draw_background(bg1, bg2, floor, state):
    bg2_y = HEIGHT - bg2.get_height() - floor.get_height()
    floor_y = HEIGHT - floor.get_height()

    SCREEN.blit(bg1, (state["bg1_x"], 0))
    SCREEN.blit(bg1, (state["bg1_x"] + 1920, 0))

    SCREEN.blit(bg2, (state["bg2_x"], bg2_y))
    SCREEN.blit(bg2, (state["bg2_x"] + 1920, bg2_y))

    SCREEN.blit(floor, (state["floor_x"], floor_y))
    SCREEN.blit(floor, (state["floor_x"] + 1920, floor_y))

def draw_cat(cat_frames, cat_jump, state, timer, index):
    now = pygame.time.get_ticks()
    if not state["is_jumping"]:
        if now - timer[0] > 150:
            index[0] = (index[0] + 1) % len(cat_frames)
            timer[0] = now
        SCREEN.blit(cat_frames[index[0]], (state["cat_x"], state["cat_y"]))
    else:
        SCREEN.blit(cat_jump, (state["cat_x"], state["cat_y"]))

def draw_dog(dog_frames, state, timer, index):
    now = pygame.time.get_ticks()
    if now - timer[0] > 150:
        index[0] = (index[0] + 1) % len(dog_frames)
        timer[0] = now
    SCREEN.blit(dog_frames[index[0]], (state["dog_x"], HEIGHT - 100))

# Texts
def draw_score(state, high_score):
    score_int = int(state["score"])
    high_int = int(high_score)

    hi_text = FONT.render(f"HI {high_int:05d}", True, FONT_COLOR)
    hi_text.set_alpha(100)
    hi_rect = hi_text.get_rect(topright=(WIDTH - 120, 20))

    score_text = FONT.render(f"{score_int:05d}", True, FONT_COLOR)
    score_rect = score_text.get_rect(topright=(WIDTH - 20, 20))

    SCREEN.blit(hi_text, hi_rect)
    SCREEN.blit(score_text, score_rect)

def draw_game_over():
    over_text = FONT.render("GAME OVER", True, (255, 0, 0))
    over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    SCREEN.blit(over_text, over_rect)

    restart_text = FONT.render("Pressione [R] para recomeçar", True, FONT_COLOR)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    SCREEN.blit(restart_text, restart_rect)

    restart_text = FONT.render("Pressione [E] para sair", True, FONT_COLOR)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    SCREEN.blit(restart_text, restart_rect)

def draw_start_message():
    start_text = FONT.render("Pressione [ESPAÇO] para pular!", True, FONT_COLOR)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    SCREEN.blit(start_text, start_rect)

def draw_pause_message():
    pause_text = FONT.render("PAUSADO - [P] Retomar", True, FONT_COLOR)
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    SCREEN.blit(pause_text, pause_rect)

    name_text = FONT_SMALLER.render("Desenvolvido por Gean Brandão", True, FONT_COLOR)
    name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(name_text, name_rect)

    date_text = FONT_SMALLER.render("Agosto de 2025", True, FONT_COLOR)
    date_rect = date_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    SCREEN.blit(date_text, date_rect)

    exit_hint = FONT_SMALLER.render("[E] - Sair", True, FONT_COLOR)
    exit_hint_rect = exit_hint.get_rect(topleft=(20, 60))
    SCREEN.blit(exit_hint, exit_hint_rect)

def draw_hint_message():
    hint_text = FONT_SMALLER.render("[P] - Pausar", True, FONT_COLOR)
    hint_rect = hint_text.get_rect(topleft=(20, 20))
    SCREEN.blit(hint_text, hint_rect)

# Loop principal
def main():
    clock = pygame.time.Clock()
    fps = 60

    jump_sound, game_over_sound, background_music = load_sounds()
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.3)
    # infinite loop
    pygame.mixer.music.play(-1)

    cat_frames, cat_jump, dog_frames, floor, bg1, bg2 = load_assets()
    state = reset_game()
    high_score = 0

    cat_timer = [0]
    cat_index = [0]
    dog_timer = [0]
    dog_index = [0]

    running = True
    while running:
        clock.tick(fps)
        SCREEN.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and (state["paused"] or state["game_over"]):
                if event.key == pygame.K_e:
                    running = False

            if event.type == pygame.KEYDOWN:
                if state["game_over"]:
                    if event.key == pygame.K_r:
                        state = reset_game()

                elif state["game_started"]:
                    if event.key == pygame.K_p:
                        state["paused"] = not state["paused"]

        draw_background(bg1, bg2, floor, state)
        handle_input(state, jump_sound)

        if state["game_started"] and not state["paused"] and not state["game_over"]:
            draw_hint_message()

        if not state["game_started"]:
            draw_start_message()
        elif state["paused"]:
            draw_cat(cat_frames, cat_jump, state, cat_timer, cat_index)
            draw_dog(dog_frames, state, dog_timer, dog_index)
            draw_pause_message()
        elif not state["game_over"]:
            update_background_positions(state)
            update_cat_position(state)
            update_dog_position(state)
            draw_cat(cat_frames, cat_jump, state, cat_timer, cat_index)
            draw_dog(dog_frames, state, dog_timer, dog_index)

            # score
            state["score"] += 0.5
            if state["score"] > high_score:
                high_score = state["score"]

            # update difficult every 250 points
            if int(state["score"]) % 250 == 0 and int(state["score"]) != 0:
                state["dog_speed"] = 5 + (int(state["score"]) // 250)

        else:
            draw_game_over()

        # collision
        cat_rect = pygame.Rect(state["cat_x"], state["cat_y"], 64, 64)
        dog_rect = pygame.Rect(state["dog_x"], HEIGHT - 100, 80, 60)
        if cat_rect.colliderect(dog_rect) and not state["game_over"]:
            game_over_sound.play()
            state["game_over"] = True

        draw_score(state, high_score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
