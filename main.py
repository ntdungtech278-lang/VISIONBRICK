 
import pygame
import random
 
 
pygame.init()
 
timer = pygame.time.Clock()
fps = 60 
 
white = (255, 255, 255) 
black = (0, 0, 0) 
gray = (128, 128, 128) 
red = (255, 0, 0) 
orange = (255, 128, 0) 
green = (0, 255, 0) 
blue = (0, 0, 255) 
purple = (255, 0, 255) 
 
# tốc độ và hướng di chuyển của thanh ray
player_speed = 8 
player_direction = 0 
 
WIDTH = 400
HEIGHT = 700
player_x = 140
ball_x = WIDTH / 2
ball_y = HEIGHT - 30  
ball_x_direction = 0  
ball_y_direction = 0  
ball_x_speed = 5
ball_y_speed = 5 
 
# điểm số
score = 0  

 
board = [[5,5,5,5,5],
         [4,4,4,4,4], 
         [3,3,3,3,3], 
         [2,2,2,2,2], 
         [1,1,1,1,1]] 
colors = [red, orange, green, blue, purple] 
 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
 
front = pygame.font.Font('freesansbold.ttf', 30)
 
 
# hàm vẽ các viên gạch và tạo vùng va chạm
def draw_board(board): 
    board_squares = []
    for i in range(len(board)): 
        for j in range(len(board[i])): 
            if board[i][j] > 0:
                piece = pygame.draw.rect(screen, colors[(board[i][j]) - 1], [j * 80, i * 30, 78, 28])
                top = pygame.rect.Rect((j * 80, i * 30), (78, 1))
                bot = pygame.rect.Rect((j * 80, i * 30 + 27), (78, 1)) 
                right = pygame.rect.Rect((j * 80 + 77, i * 30), (1, 28)) 
                left = pygame.rect.Rect((j * 80, i * 30), (1, 28)) 
                board_squares.append([top, bot, left, right, (i, j)])
    return board_squares 
 
 
# hàm tạo bàn gạch mới ngẫu nhiên
def creat_new_board(): 
    board = [] 
    rows = random.randint(4, 7) 
    for i in range(rows): 
        row = [] 
        for j in range(5): 
            row.append(random.randint(1, 5)) 
        board.append(row) 
    return board 
 
 
 
active = False
run = True
new_game = True  
while run:  
    screen.fill(gray)
    timer.tick(fps)
 
    if new_game:  
        board = creat_new_board()
        new_game = False 
 
    squares = draw_board(board)
    # print(squares) 
 
    player = pygame.draw.rect(screen, black, [player_x, HEIGHT - 20, 120, 15], 0, 3)
    ball = pygame.draw.circle(screen, white, (ball_x, ball_y), 10)
 
 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False 
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not active:
                active = True 
                ball_y_direction = -1  
                ball_x_direction = random.choice([-1, 1])
                score = 0  
            if event.key == pygame.K_RIGHT and active:
                player_direction = 1 
            if event.key == pygame.K_LEFT and active:
                player_direction = -1 
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_direction = 0 
            if event.key == pygame.K_LEFT:
                player_direction = 0 
 
    # xử lí hướng bay của bóng khi chạm biên trái/phải
    if ball_x <= 10 or ball_x >= WIDTH - 10:
        ball_x_direction *= -1
 
    # xử lí va chạm giữa bóng và các viên gạch
    for i in range(len(squares)): 
        # top, bot, left, right, coords
        if (ball.colliderect(squares[i][0]) and ball_y_direction == 1) or \
            (ball.colliderect(squares[i][1]) and ball_y_direction == -1):
            ball_y_direction *= -1  
            board[squares[i][4][0]][squares[i][4][1]] -= 1
            score += 1  
        if (ball.colliderect(squares[i][2]) and ball_x_direction == 1) or \
            (ball.colliderect(squares[i][3]) and ball_x_direction == -1):
            ball_x_direction *= -1
            board[squares[i][4][0]][squares[i][4][1]] -= 1 
            score += 1   
 
 
    # xử lí va chạm giữa bóng và thanh ray
    if ball.colliderect(player):
        if player_direction == ball_x_direction:
            ball_x_speed += 1 
        elif player_direction == - ball_x_direction and ball_x_speed > 1:
            ball_x_speed -= 1  
        elif player_direction == - ball_x_direction and ball_x_speed == 1:
            ball_x_direction *= -1

        ball_y_direction *= -1 
        ball_y = player.top - 10
 
    # cập nhật vị trí bóng
    ball_y += ball_y_direction * ball_y_speed  
    ball_x += ball_x_direction * ball_x_speed  
 
    # xử lí va chạm với mép trên
    if ball_y <= 10:  
        ball_y = 10  
        ball_y_direction *= -1 
 
 
    # giới hạn thanh ray trong phạm vi màn hình
    tmp = player_x + player_direction * player_speed 
    if tmp < 0:
        player_x = 0 
    if tmp > WIDTH - 120:  
        player_x = WIDTH - 120 
    if 0 <= tmp <= WIDTH - 120:  
        player_x = tmp
 
    # xử lí khi bóng rơi hoặc phá hết gạch
    if ball_y >= HEIGHT - 10 or len(squares) == 0:  
        active = False 
        player_x = 140
        ball_x = WIDTH / 2
        ball_y = HEIGHT - 30  
        ball_x_direction = 0  
        ball_y_direction = 0  
        ball_x_speed = 5
        ball_y_speed = 5 
        board = [[5,5,5,5,5],
                [4,4,4,4,4], 
                [3,3,3,3,3], 
                [2,2,2,2,2]]
        new_game = True 
 
 
    score_text = front.render(f'Score {score}', True, black)
    screen.blit(score_text, (10, 5))
    # hiển thị hướng dẫn khi chưa bắt đầu chơi
    if not active:  
        start_text = front.render('Space bar to start game', True, black) 
        screen.blit(start_text, (20, 400))  
 
    pygame.display.flip()
 
pygame.quit()
