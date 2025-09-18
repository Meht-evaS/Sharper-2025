import pygame
import sys
import time

# --- COSTANTI ---
BLOCK_SIZE = 64
ROWS = 9
COLS = 19 # 15 + 4 colonne nere a destra
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
FPS = 60

GREEN = (34, 177, 76)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 80, 255)
BOX_BG = (20, 20, 20)

GARFIELD_SIZE = BLOCK_SIZE // 2
GARFIELD_START_ROW = 5
GARFIELD_START_COL = 0

pygame.init()

arrow_font_name = "dejavusans"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garfield Crossing")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
levelup_font = pygame.font.SysFont(None, 38)
large_font = pygame.font.SysFont(None, 43)
box_font = pygame.font.SysFont(None, 24)
victory_font = pygame.font.SysFont(None, 41)
moves_font = pygame.font.SysFont(arrow_font_name, 52)
moves_title_font = pygame.font.SysFont(None, 32)

MOVES_SYMBOLS = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→"
}

garfield_image = pygame.image.load("img/garfield.png")
garfield_image_size = int(BLOCK_SIZE * 0.9)
garfield_image = pygame.transform.scale(garfield_image, (garfield_image_size, garfield_image_size))

accalappiagatti_image = pygame.image.load("img/accalappiagatti.png")
accalappiagatti_image_size = int(BLOCK_SIZE * 0.9)
accalappiagatti_image = pygame.transform.scale(accalappiagatti_image, (accalappiagatti_image_size, accalappiagatti_image_size))

goal_image_size = int(BLOCK_SIZE * 1.4)
goal_frames = [pygame.transform.scale(pygame.image.load(f"img/frame_{str(i).zfill(2)}.png"), (goal_image_size, goal_image_size)) for i in range(5,12)]
goal_image_static = pygame.transform.scale(pygame.image.load("img/goal.png"), (goal_image_size, goal_image_size))

DEBUG = False

def wrap_text_multiline(text, font, max_width):
    all_lines = []
    for raw_line in text.split('\n'):
        if raw_line.strip() == "":
            all_lines.append("")
            continue
        words = raw_line.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    all_lines.append(current_line)
                current_line = word
        if current_line:
            all_lines.append(current_line)
    return all_lines

def draw_message_box(surface, message, color=RED, style="normal"):
    if style == "victory":
        f = victory_font
        box_height = 240
    elif style == "large":
        f = large_font
        box_height = 240
    elif style == "levelup":
        f = levelup_font
        box_height = 180
    else:
        f = font
        box_height = 180
    box_width = WIDTH // 2
    max_text_width = box_width - 30
    lines = wrap_text_multiline(message, f, max_text_width)
    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 - box_height // 2

    box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(box_surface, WHITE, (0, 0, box_width, box_height), width=3, border_radius=16)
    bg_rect = pygame.Rect(3, 3, box_width-6, box_height-6)
    pygame.draw.rect(box_surface, (0, 0, 0, int(255 * 0.7)), bg_rect, border_radius=13)

    total_text_height = len(lines) * f.get_height()
    vertical_offset = 15
    start_y = (box_height - total_text_height) // 2 + vertical_offset

    for i, line in enumerate(lines):
        text = f.render(line if line != "" else " ", True, color)
        rect = text.get_rect(center=(box_width // 2, start_y + i * f.get_height()))
        box_surface.blit(text, rect)

    surface.blit(box_surface, (box_x, box_y))

class Garfield:
    def __init__(self):
        self.lives = 5
        self.reset()

    def reset(self):
        self.row = GARFIELD_START_ROW
        self.col = GARFIELD_START_COL
        self.x = self.col * BLOCK_SIZE + BLOCK_SIZE // 2
        self.y = self.row * BLOCK_SIZE + BLOCK_SIZE // 2
        self.moves = []
        self.block_target = None
        self.direction = None
        self.in_erba_bassa = False
        self.just_entered_erba_bassa = False

    def move(self, drow, dcol, direction):
        target_row = self.row + drow
        target_col = self.col + dcol

        if self.in_erba_bassa:
            if self.row == 7 and target_row == 7 and target_col >= 4 and target_col <= 10 and direction == "right":
                self.block_target = (target_row, target_col)
                self.direction = direction
                self.moves.append(direction)
                return
        if is_valid_move(self.row, self.col, target_row, target_col, self):
            self.block_target = (target_row, target_col)
            self.direction = direction
            self.moves.append(direction)

    def update(self):
        if self.block_target:
            target_x = self.block_target[1] * BLOCK_SIZE + BLOCK_SIZE // 2
            target_y = self.block_target[0] * BLOCK_SIZE + BLOCK_SIZE // 2

            dx = target_x - self.x
            dy = target_y - self.y
            speed = 4

            if abs(dx) > speed:
                self.x += speed if dx > 0 else -speed
            else:
                self.x = target_x

            if abs(dy) > speed:
                self.y += speed if dy > 0 else -speed
            else:
                self.y = target_y

            if self.x == target_x and self.y == target_y:
                self.row, self.col = self.block_target
                self.block_target = None
                self.direction = None

    def draw(self, surface):
        rect = garfield_image.get_rect(center=(self.x, self.y))
        surface.blit(garfield_image, rect)

class Accalappiagatti:
    def __init__(self):
        self.row = 2
        self.col = GARFIELD_START_COL

    def update(self, garfield_col):
        self.col = garfield_col

    def draw(self, surface):
        x = self.col * BLOCK_SIZE + BLOCK_SIZE // 2
        y = self.row * BLOCK_SIZE + BLOCK_SIZE // 2
        rect = accalappiagatti_image.get_rect(center=(x, y))
        surface.blit(accalappiagatti_image, rect)

def is_valid_move(row, col, target_row, target_col, garfield):
    if target_row < 3 or target_row >= ROWS or target_col < 0 or target_col >= 15:
        return False

    if garfield.in_erba_bassa:
        if row == 8 and target_row == 8 and target_col >= 4 and target_col <= 10 and (target_col == col + 1 or target_col == col - 1):
            return True

    if (
        (target_row == 5 and target_col == 0) or
        (target_row == 8 and target_col == 4) or
        (target_col >= 11)
        or (target_col == 13)
        or (target_col == 14)
    ):
        return True

    is_erba = (
        target_row == 2 or
        target_row == ROWS-1 or
        target_col == 0 or
        target_col >= 11
    )
    if is_erba and target_col not in [13, 14]:
        return False

    return True

def draw_grid(surface, use_anim=False, anim_frame=0):
    for row in range(2):
        for col in range(COLS):
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, BLACK, rect)
    for row in range(2, ROWS):
        for col in range(15):
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if col == 14:
                color = GREEN
            elif row == 2 or row == ROWS-1 or col == 0 or col >= 11:
                color = GREEN
            elif col == 10:
                color = WHITE
            else:
                color = GRAY
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
    for row in range(ROWS):
        for col in range(15, COLS):
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, BLACK, rect)

    goal_center_x = ((12 * BLOCK_SIZE + BLOCK_SIZE // 2) + (13 * BLOCK_SIZE + BLOCK_SIZE // 2)) // 2
    goal_center_y = 5 * BLOCK_SIZE + BLOCK_SIZE // 2
    if use_anim:
        surface.blit(goal_frames[anim_frame], goal_frames[anim_frame].get_rect(center=(goal_center_x, goal_center_y)))
    else:
        surface.blit(goal_image_static, goal_image_static.get_rect(center=(goal_center_x, goal_center_y)))

def draw_status(surface, level, lives, catch_column_msg=None):
    status_text = f"Livello: {level}     Vite: {lives}"
    text = font.render(status_text, True, WHITE)
    surface.blit(text, (20, BLOCK_SIZE // 2 - text.get_height() // 2))
    if catch_column_msg:
        catch_text = font.render(catch_column_msg, True, RED)
        surface.blit(catch_text, (20, BLOCK_SIZE // 2 + text.get_height()))

def draw_moves_box(surface, moves):
    area_x = 15 * BLOCK_SIZE + 12
    area_y = 2 * BLOCK_SIZE + 18
    area_w = 4 * BLOCK_SIZE - 24
    area_h = (ROWS - 2) * BLOCK_SIZE - 36

    box_surface = pygame.Surface((area_w, area_h), pygame.SRCALPHA)
    pygame.draw.rect(box_surface, WHITE, (0, 0, area_w, area_h), width=3, border_radius=20)
    pygame.draw.rect(box_surface, (0, 0, 0, 220), (3, 3, area_w - 6, area_h - 6), border_radius=17)

    title = moves_title_font.render("Lista movimenti", True, WHITE)
    title_rect = title.get_rect(center=(area_w // 2, 24))
    box_surface.blit(title, title_rect)

    moves_area_y = 56
    moves_area_h = area_h - moves_area_y - 10
    line_height = moves_font.get_height() + 4
    max_moves_shown = moves_area_h // line_height

    recent_moves = moves[-max_moves_shown:]
    for i, move in enumerate(recent_moves):
        symbol = MOVES_SYMBOLS.get(move, "?")
        mtext = moves_font.render(symbol, True, WHITE)
        mrect = mtext.get_rect(center=(area_w // 2, moves_area_y + i * line_height + line_height // 2))
        box_surface.blit(mtext, mrect)

    total_moves = len(moves)
    if total_moves > max_moves_shown:
        scrollbar_h = int(moves_area_h * max_moves_shown / total_moves)
        scrollbar_y = int(moves_area_y + (moves_area_h - scrollbar_h) * (total_moves - max_moves_shown) / (total_moves - max_moves_shown))
        pygame.draw.rect(box_surface, (180,180,180), (area_w - 16, scrollbar_y, 10, scrollbar_h), border_radius=7)

    surface.blit(box_surface, (area_x, area_y))

def check_level_1_catch(moves, garfield):
    if not garfield.in_erba_bassa and len(moves) >= 3 and moves[-3:] == ["right", "right", "right"]:
        return True
    return False

def check_level_2_catch(moves, garfield):
    if not garfield.in_erba_bassa:
        if len(moves) > 2 and moves[-2:] == ["right", "right"]:
            return True
        if len(moves) >= 2 and moves[-2:] == ["up", "up"]:
            return True
        if len(moves) >= 2 and moves[-2:] == ["down", "down"]:
            return True
    return False

def check_level_3_catch(garfield):
    moves = garfield.moves
    if not hasattr(garfield, "in_erba_bassa"):
        garfield.in_erba_bassa = False
    if not hasattr(garfield, "just_entered_erba_bassa"):
        garfield.just_entered_erba_bassa = False

    if not garfield.in_erba_bassa and len(moves) >= 3 and moves[-2:] == ["right", "right"]:
        return True
    if len(moves) >= 2 and moves[-2:] == ["up", "up"]:
        return True
    if len(moves) >= 2 and moves[-2:] == ["down", "down"]:
        return True

    if garfield.row == 8 and garfield.col == 4:
        garfield.just_entered_erba_bassa = True
        garfield.in_erba_bassa = True

    if garfield.in_erba_bassa and garfield.row == 7 and garfield.col == 4 and len(moves) > 0 and moves[-1] == "up":
        garfield.in_erba_bassa = False
        garfield.just_entered_erba_bassa = False

    if garfield.in_erba_bassa:
        if garfield.just_entered_erba_bassa:
            if garfield.row == 8 and garfield.col > 4 and moves[-1] == "right":
                garfield.just_entered_erba_bassa = False
        else:
            if garfield.col > 4 and garfield.row != 8 and len(moves) > 0 and moves[-1] == "up":
                return True
            if garfield.row != 8:
                return True
    elif garfield.col > 4:
        return True

    return False

def is_on_goal(garfield):
    return garfield.col == 10 and garfield.row not in [2, ROWS-1]

def is_on_win(garfield):
    return garfield.col > 10

def animate_victory_move(garfield, screen, start_row, start_x, end_row, end_x):
    target_x = end_x
    target_y = end_row * BLOCK_SIZE + BLOCK_SIZE // 2

    garfield.x = start_x
    garfield.y = start_row * BLOCK_SIZE + BLOCK_SIZE // 2

    speed = 8
    moving = True
    while moving:
        clock.tick(FPS)
        dx = target_x - garfield.x
        dy = target_y - garfield.y

        if abs(dx) > speed:
            garfield.x += speed if dx > 0 else -speed
        else:
            garfield.x = target_x

        if abs(dy) > speed:
            garfield.y += speed if dy > 0 else -speed
        else:
            garfield.y = target_y

        if garfield.x == target_x and garfield.y == target_y:
            moving = False

        screen.fill((100, 100, 100))
        draw_grid(screen)
        draw_status(screen, 3, garfield.lives)
        draw_moves_box(screen, garfield.moves)
        garfield.draw(screen)
        pygame.display.flip()

def main():
    level = 1
    garfield = Garfield()
    accalappiagatti = Accalappiagatti()
    running = True
    show_message = None
    message_timer = None
    message_type = None
    last_catch_position = None
    catch_column_msg = None
    victory_animated = False
    frame_idx = 0
    frame_timer = 0
    frame_interval = 0.09  # secondi (~11 fps)
    waiting_for_retry = False
    waiting_gameover_captured = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if waiting_for_retry and not waiting_gameover_captured:
                if event.type == pygame.KEYDOWN:
                    # Reset livello dopo la cattura
                    garfield.reset()
                    accalappiagatti = Accalappiagatti()
                    show_message = None
                    message_type = None
                    message_timer = None
                    waiting_for_retry = False
            elif show_message is None and garfield.block_target is None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        garfield.move(-1, 0, "up")
                    elif event.key == pygame.K_DOWN:
                        garfield.move(1, 0, "down")
                    elif event.key == pygame.K_LEFT:
                        garfield.move(0, -1, "left")
                    elif event.key == pygame.K_RIGHT:
                        garfield.move(0, 1, "right")
            elif show_message is not None:
                if message_type == "gameover" or message_type == "victory":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        level = 1
                        garfield = Garfield()
                        accalappiagatti = Accalappiagatti()
                        show_message = None
                        message_timer = None
                        message_type = None
                        catch_column_msg = None
                        victory_animated = False

        garfield.update()
        accalappiagatti.update(garfield.col)

        caught = False
        if show_message is None:
            if level == 1 and check_level_1_catch(garfield.moves, garfield):
                caught = True
            elif level == 2 and check_level_2_catch(garfield.moves, garfield):
                caught = True
            elif level == 3 and check_level_3_catch(garfield):
                caught = True

            win = is_on_win(garfield)

            if caught:
                last_catch_position = (garfield.row, garfield.col)
                garfield.lives -= 1
                if garfield.lives > 0:
                    show_message = "Sei stato catturato!\n\nPremi un tasto per riprovare il livello..."
                    message_type = "caught"
                    message_timer = time.time()
                    catch_column_msg = f"Sei stato catturato nella colonna: {garfield.col}"
                    waiting_for_retry = True
                    waiting_gameover_captured = False
                else:
                    # Mostra prima "Sei stato catturato!" per 3 secondi, poi game over
                    show_message = "Sei stato catturato!"
                    message_type = "caught_gameover"
                    message_timer = time.time()
                    catch_column_msg = f"Sei stato catturato nella colonna: {garfield.col}"
                    waiting_for_retry = False
                    waiting_gameover_captured = True
            elif win:
                if level < 3:
                    show_message = f"Hai completato il livello {level}!"
                    message_type = "levelup"
                    message_timer = time.time()
                    catch_column_msg = None
                else:
                    show_message = "Complimenti!\nSei riuscito a scappare da AVAST l'accalappiagatti e ad installare il malware!\n\nPremi [R] per ricominciare,\naltrimenti chiudi il gioco."
                    message_type = "victory"
                    message_timer = None
                    catch_column_msg = None

        if show_message is not None:
            if message_type == "caught":
                screen.fill((100, 100, 100))
                draw_grid(screen)
                draw_status(screen, level, garfield.lives, catch_column_msg)
                draw_moves_box(screen, garfield.moves)
                garfield.draw(screen)
                catch_row, catch_col = last_catch_position
                accalappiagatti.row = catch_row
                accalappiagatti.col = catch_col
                accalappiagatti.draw(screen)
                draw_message_box(screen, show_message, RED, style="large")
                pygame.display.flip()
            elif message_type == "caught_gameover":
                # Mostra "Sei stato catturato!" per 3 secondi, poi mostra game over
                screen.fill((100, 100, 100))
                draw_grid(screen)
                draw_status(screen, level, 0, catch_column_msg)
                draw_moves_box(screen, garfield.moves)
                garfield.draw(screen)
                catch_row, catch_col = last_catch_position
                accalappiagatti.row = catch_row
                accalappiagatti.col = catch_col
                accalappiagatti.draw(screen)
                draw_message_box(screen, "Sei stato catturato!", RED, style="large")
                pygame.display.flip()
                if time.time() - message_timer > 3:
                    show_message = "Hai esaurito tutte le vite!\n\nPremi [R] per ricominciare, altrimenti chiudi il gioco."
                    message_type = "gameover"
                    message_timer = None
                    catch_column_msg = None
                    waiting_gameover_captured = False
            elif message_type == "levelup":
                screen.fill((100, 100, 100))
                draw_grid(screen)
                draw_status(screen, level, garfield.lives, catch_column_msg)
                draw_moves_box(screen, garfield.moves)
                garfield.draw(screen)
                accalappiagatti.draw(screen)
                draw_message_box(screen, show_message, RED, style="levelup")
                pygame.display.flip()
                if time.time() - message_timer > 2:
                    level += 1
                    garfield.lives += 1
                    garfield.reset()
                    accalappiagatti = Accalappiagatti()
                    show_message = None
                    message_type = None
                    message_timer = None
                    catch_column_msg = None
            elif message_type == "gameover":
                screen.fill((100, 100, 100))
                draw_grid(screen)
                draw_status(screen, level, 0, catch_column_msg)
                draw_moves_box(screen, garfield.moves)
                garfield.draw(screen)
                accalappiagatti.draw(screen)
                draw_message_box(screen, show_message, RED, style="large")
                pygame.display.flip()
            elif message_type == "victory":
                center_x = ((12 * BLOCK_SIZE + BLOCK_SIZE // 2) + (13 * BLOCK_SIZE + BLOCK_SIZE // 2)) // 2
                if not victory_animated:
                    animate_victory_move(garfield, screen, garfield.row, garfield.x, 8, center_x)
                    garfield.row = 8
                    garfield.x = center_x
                    garfield.y = 8 * BLOCK_SIZE + BLOCK_SIZE // 2
                    animate_victory_move(garfield, screen, 8, center_x, 6, center_x)
                    garfield.row = 6
                    garfield.x = center_x
                    garfield.y = 6 * BLOCK_SIZE + BLOCK_SIZE // 2
                    victory_animated = True
                now = time.time()
                if now - frame_timer > frame_interval:
                    frame_idx = (frame_idx + 1) % len(goal_frames)
                    frame_timer = now
                screen.fill((100, 100, 100))
                draw_grid(screen, use_anim=True, anim_frame=frame_idx)
                draw_status(screen, level, garfield.lives, catch_column_msg)
                draw_moves_box(screen, garfield.moves)
                garfield.draw(screen)
                accalappiagatti.draw(screen)
                draw_message_box(screen, show_message, RED, style="victory")
                pygame.display.flip()
        else:
            screen.fill((100, 100, 100))
            draw_grid(screen)
            draw_status(screen, level, garfield.lives, catch_column_msg)
            draw_moves_box(screen, garfield.moves)
            garfield.draw(screen)
            accalappiagatti.draw(screen)
            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()