import pygame
import pygame_gui

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Мальцев Продакшен")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
BALL_RADIUS = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

left_paddle_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
right_paddle_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x = WINDOW_WIDTH // 2 - BALL_RADIUS // 2
ball_y = WINDOW_HEIGHT // 2 - BALL_RADIUS // 2

ball_dx = -BALL_SPEED_X
ball_dy = BALL_SPEED_Y

left_score = 0
right_score = 0

menu_active = True
game_over = False
restart_button = None

font = pygame.font.Font(None, 36)
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == restart_button:
                    menu_active = True
                    left_score = 0
                    right_score = 0
                    game_over = False
                    restart_button.kill()

        manager.process_events(event)

    if menu_active:
        screen.fill(WHITE)

        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 100)
        pygame.draw.rect(screen, BLACK, start_button)

        text = font.render("Начать игру", True, WHITE)
        text_rect = text.get_rect(center=start_button.center)
        screen.blit(text, text_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                menu_active = False
                left_score = 0
                right_score = 0

    elif not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_y > 0:
            left_paddle_y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            left_paddle_y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            right_paddle_y += PADDLE_SPEED

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= BALL_RADIUS or ball_y >= WINDOW_HEIGHT - BALL_RADIUS:
            ball_dy *= -1
        if ball_x <= PADDLE_WIDTH and left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT:
            ball_dx *= -1
        if ball_x >= WINDOW_WIDTH - PADDLE_WIDTH - BALL_RADIUS and right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT:
            ball_dx *= -1
        if ball_x <= 0:
            right_score += 1
            ball_x = WINDOW_WIDTH // 2 - BALL_RADIUS // 2
            ball_y = WINDOW_HEIGHT // 2 - BALL_RADIUS // 2
            ball_dx *= -1
            if right_score == 5:
                game_over = True
                winner_text = font.render("Победил игрок 2!", True, BLACK)
                screen.blit(winner_text, (WINDOW_WIDTH // 2 - 100, 100))
                restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 100, 200), (200, 50)),
                                                              text='Начать заново',
                                                              manager=manager)

        if ball_x >= WINDOW_WIDTH - BALL_RADIUS:
            left_score += 1
            ball_x = WINDOW_WIDTH // 2 - BALL_RADIUS // 2
            ball_y = WINDOW_HEIGHT // 2 - BALL_RADIUS // 2
            ball_dx *= -1
            if left_score == 5:
                game_over = True
                winner_text = font.render("Победил игрок 1!", True, BLACK)
                screen.blit(winner_text, (WINDOW_WIDTH // 2 - 100, 100))
                restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 100, 200), (200, 50)),
                                                              text='Начать заново',
                                                              manager=manager)

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, BLACK, (ball_x, ball_y), BALL_RADIUS)

        left_score_text = font.render(str(left_score), True, BLACK)
        right_score_text = font.render(str(right_score), True, BLACK)
        screen.blit(left_score_text, (WINDOW_WIDTH // 4, 50))
        screen.blit(right_score_text, (WINDOW_WIDTH * 3 // 4, 50))

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
