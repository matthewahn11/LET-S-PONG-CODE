import pygame
import random

# Pygame 초기화
pygame.init()
pygame.mixer.init() # 사운드 믹서 초기화

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LET'S PONG") # 게임 제목 설정

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 설정 (점수 표시용)
font = pygame.font.Font(None, 74)
winner_font = pygame.font.Font(None, 100) # 승리 메시지용 폰트 추가

# 사운드 로딩
try:
    hit_sound = pygame.mixer.Sound("hit_sound.wav") # 공이 패들이나 벽에 부딪힐 때
    score_sound = pygame.mixer.Sound("score_sound.wav") # 득점 시

except pygame.error as e:
    print(f"사운드 파일을 로드할 수 없습니다: {e}. 사운드 파일 (hit_sound.wav, score_sound.wav)이 같은 디렉토리에 있는지 확인하세요.")
    hit_sound = None
    score_sound = None

# 패들 설정
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

player1_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# 공 설정
BALL_SIZE = 20
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# 공 속도 설정
# 초기 공 방향을 랜덤으로 설정
BALL_SPEED_INITIAL = 7 # 초기 공 속도 설정
BALL_SPEED_X = random.choice([-BALL_SPEED_INITIAL, BALL_SPEED_INITIAL])
BALL_SPEED_Y = random.choice([-BALL_SPEED_INITIAL, BALL_SPEED_INITIAL])
BALL_SPEED = [BALL_SPEED_X, BALL_SPEED_Y]

# 점수 설정
player1_score = 0
player2_score = 0
MAX_SCORE = 10 # 게임 종료 조건

# --- 함수 정의 ---

def reset_ball():
    #공을 중앙으로 리셋하고 랜덤한 초기 속도를 부여
    global BALL_SPEED
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    BALL_SPEED[0] = random.choice([-BALL_SPEED_INITIAL, BALL_SPEED_INITIAL]) #
    BALL_SPEED[1] = random.choice([-BALL_SPEED_INITIAL, BALL_SPEED_INITIAL])

def move_ball():
    #공을 이동시키고 벽 및 패들과의 충돌을 처리
    global player1_score, player2_score

    ball.x += BALL_SPEED[0]
    ball.y += BALL_SPEED[1]

    # 벽과의 충돌 처리 (상하 벽)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED[1] *= -1
        if hit_sound: hit_sound.play()

    # 패들과의 충돌 처리
    if ball.colliderect(player1_paddle):
        if BALL_SPEED[0] < 0: # 공이 왼쪽으로 가다가 충돌했을 때만 반사
            BALL_SPEED[0] *= -1
            if hit_sound: hit_sound.play()


    if ball.colliderect(player2_paddle):
        if BALL_SPEED[0] > 0: # 공이 오른쪽으로 가다가 충돌했을 때만 반사
            BALL_SPEED[0] *= -1
            if hit_sound: hit_sound.play()


    # 득점 처리 (좌우 벽)
    if ball.left <= 0: # Player 2 득점
        player2_score += 1
        if score_sound: score_sound.play()
        reset_ball()
    if ball.right >= SCREEN_WIDTH: # Player 1 득점
        player1_score += 1
        if score_sound: score_sound.play()
        reset_ball()

def move_paddles():
    # 키보드 입력에 따라 패들을 움직임
    keys = pygame.key.get_pressed() #

    # Player 1 (왼쪽) 패들 조작: W(상), S(하)
    if keys[pygame.K_w]:
        player1_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        player1_paddle.y += PADDLE_SPEED

    # Player 2 (오른쪽) 패들 조작: UP(상), DOWN(하)
    if keys[pygame.K_UP]:
        player2_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        player2_paddle.y += PADDLE_SPEED

    # 패들이 화면 밖으로 나가지 않도록 제한
    player1_paddle.top = max(0, player1_paddle.top)
    player1_paddle.bottom = min(SCREEN_HEIGHT, player1_paddle.bottom)
    player2_paddle.top = max(0, player2_paddle.top)
    player2_paddle.bottom = min(SCREEN_HEIGHT, player2_paddle.bottom)

def draw_objects():
    # 게임 화면에 모든 객체를 그리기
    screen.fill(BLACK) # 배경 채우기
    pygame.draw.rect(screen, WHITE, player1_paddle) # 패들 그리기
    pygame.draw.rect(screen, WHITE, player2_paddle)
    pygame.draw.ellipse(screen, WHITE, ball) # 공 그리기
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT)) # 중앙 선 그리기

    # 점수 표시
    score_text = font.render(f"{player1_score} : {player2_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

# --- 게임 루프 ---
running = True
game_over = False
clock = pygame.time.Clock() # 프레임 속도 제어를 위함

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        move_paddles() # 패들 이동 업데이트
        move_ball()    # 공 이동 및 충돌 업데이트

        # 게임 종료 조건 확인
        if player1_score >= MAX_SCORE:
            winner_text = winner_font.render("Player 1 Wins!", True, WHITE)
            game_over = True
        elif player2_score >= MAX_SCORE:
            winner_text = winner_font.render("Player 2 Wins!", True, WHITE)
            game_over = True

    draw_objects() # 모든 객체 그리기

    if game_over:
        # 승리 메시지 표시
        screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2))
        pygame.display.flip() # 화면 업데이트
        pygame.time.wait(3000) # 3초 대기
        running = False # 게임 종료

    pygame.display.flip() # 모든 요소를 화면에 업데이트

    # 프레임 속도 제어
    clock.tick(60) # 60 FPS

pygame.quit()

