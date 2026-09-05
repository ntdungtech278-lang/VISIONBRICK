#


import pygame # thư viện lập trình game 2D python
import random # module có sẵn của Python, dùng để tạo ra các giá trị ngẫu nhiên.


pygame.init() # khởi tạo pygame

timer = pygame.time.Clock() # bộ đếm thời gian 
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (255, 0, 0)
orange = (255, 128, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)

# tốc độ và bước nhảy của thanh ray 
player_speed = 8
player_direction = 0

WIDTH = 400 # kích thước cửa sổ (pixel) default = 400
HEIGHT = 700 # default = 700
player_x = 140 # điểm bắt đầu của thanh đón bòng 
ball_x = WIDTH / 2 # vị trí bắt đầu của bóng trong game (trục x, y)
ball_y = HEIGHT - 30 
ball_x_direction = 0 
ball_y_direction = 0 
ball_x_speed = 5 # vận tốc di chuyển theo trục x, y của bóng 
ball_y_speed = 5

# điểm số: 
score = 0 


board = [[5,5,5,5,5],  # ma trận 2 * 2, mỗi điểm a[i][j] là 1 viên gạch, giá trị là màu của viên gạch đó
         [4,4,4,4,4],
         [3,3,3,3,3],
         [2,2,2,2,2],
         [1,1,1,1,1]]
colors = [red, orange, green, blue, purple]

screen = pygame.display.set_mode([WIDTH, HEIGHT]) # tạo cửa sổ 

front = pygame.font.Font('freesansbold.ttf', 30) # 


# hàm vẽ gạch 
def draw_board(board):
    board_squares = [] # ? mảng lưu các phần tử bao gầm thông tin (block và vị trí của nó), phần tử tạo ở cuối sẽ được thêm vào cuối cùng của board_squares 
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0: # mảng vẫn có màu => vẽ phần tử có tọa độ x, y và màu tương ứng, thêm vào mảng board_squares 
                piece = pygame.draw.rect(screen, colors[(board[i][j]) - 1], [j * 80, i * 30, 78, 28]) # vẽ block 
                top = pygame.rect.Rect((j * 80, i * 30), (78, 1)) # tạo vùng ẩn ((x, y), (Width, Height)) => xác định vùng va chạm của block 
                bot = pygame.rect.Rect((j * 80, i * 30 + 27), (78, 1))
                right = pygame.rect.Rect((j * 80 + 77, i * 30), (1, 28))
                left = pygame.rect.Rect((j * 80, i * 30), (1, 28))
                board_squares.append([top, bot, left, right, (i, j)]) # ? thêm phần từ block có vị trí i, j vào cuối mảng vd:[rect, (1, 2)]
    return board_squares


def creat_new_board():
    board = []
    rows = random.randint(4, 7)
    for i in range(rows):
        row = []
        for j in range(5):
            row.append(random.randint(1, 5))
        board.append(row)
    return board



active = False # True = user đang chơi 
run = True # flag, True = phần mềm đang mở 
new_game = True 
while run: 
    screen.fill(gray) # tô toàn bộ màn hình bằng màu xám 
    timer.tick(fps) # giới hạn toàn bộ fps 

    if new_game: 
        board = creat_new_board() # random block 
        new_game = False

    squares = draw_board(board) # mảng squares 2 chiều lưu các viên gạch chưa bị phá, mỗi viên gạch có thuộc tính (trên, dưới, trái, phải, (x, y))
    # print(squares)

    player = pygame.draw.rect(screen, black, [player_x, HEIGHT - 20, 120, 15], 0, 3) # tạo thanh trượt chữ nhật (màn hình được vẽ, màu,[x, y, width, height], độ dày viền, bo góc)
    ball = pygame.draw.circle(screen, white, (ball_x, ball_y), 10) # tạo bóng (màn hình được vẽ, màu, (tọa độ tâm x, y), bán kính)


    for event in pygame.event.get():
        if event.type == pygame.QUIT: # khi người dùng nhất nút đóng cửa sổ 
            run = False

        if event.type == pygame.KEYDOWN: # pygame.KEYDOWN = nhấn nút
            if event.key == pygame.K_SPACE and not active: # K_SPACE = dấu cách 
                active = True
                ball_y_direction = -1 
                ball_x_direction = random.choice([-1, 1]) # giá trị ban đầu nó có thể bắn sang trái hoặc phải theo phương x 
                score = 0 
            if event.key == pygame.K_RIGHT and active: # pygame.K_RIGHT / LEFT = sang phải / trái
                player_direction = 1
            if event.key == pygame.K_LEFT and active: 
                player_direction = -1

        if event.type == pygame.KEYUP: # pygame.KEYUP = thả nút => ko di chuyển 
            if event.key == pygame.K_RIGHT:
                player_direction = 0
            if event.key == pygame.K_LEFT : 
                player_direction = 0

    # xử lí hướng bay của bóng khi bay lên 
    if ball_x <= 10 or ball_x >= WIDTH - 10: # bán kính bóng = 10 
        ball_x_direction *= -1 # đổi hướng  

    # xử lí màu khi bóng chạm vào gạch 
    for i in range(len(squares)):
        # top, bot, left, right, coords (tọa độ)
        if (ball.colliderect(squares[i][0]) and ball_y_direction == 1) or \
            (ball.colliderect(squares[i][1]) and ball_y_direction == -1): # khi bóng chạm vào 1 phần tử của squares[i][0] = top, squares[i][1] = bot
            ball_y_direction *= -1 
            board[squares[i][4][0]][squares[i][4][1]] -= 1 # giảm màu sắc của block => index out ới board[-5]
            score += 1 
        if (ball.colliderect(squares[i][2]) and ball_x_direction == 1) or \
            (ball.colliderect(squares[i][3]) and ball_x_direction == -1): # khi bóng chạm vào trái và phải block 
            ball_x_direction *= -1
            board[squares[i][4][0]][squares[i][4][1]] -= 1
            score += 1  


    # xử lí hương bay của quả bóng khi chạm vào thanh 
    if ball.colliderect(player): # #colliderect là hàm kiểm tra 2 hcn có chạm nhau hay ko 
        if player_direction == ball_x_direction: # player và ball cùng hướng => tăng vận tốc bóng theo x 
            ball_x_speed += 1
        elif player_direction == - ball_x_direction and ball_x_speed > 1: # ngược hướng và vận tốc theo x khác 1 thì giảm vận tốc theo x 
            ball_x_speed -= 1 
        elif player_direction == - ball_x_direction and ball_x_speed == 1:# ngược hướng và vận tốc bằng 1 => đổi hướng theo x
            ball_x_direction *= -1 # đổi hướng theo phương x

        ball_y_direction *= -1
        ball_y = player.top - 10 # đưa tâm bóng ra ngoài thanh player 

    # cập nhật vị trí bóng 
    ball_y += ball_y_direction * ball_y_speed 
    ball_x += ball_x_direction * ball_x_speed 

    # khi bóng chạm mép trên 
    if ball_y <= 10: 
        ball_y = 10 
        ball_y_direction *= -1


    # chặn thanh ray khỏi ra ngoài biên 
    tmp = player_x + player_direction * player_speed
    if tmp < 0: # vì có speed = 8 
        player_x = 0
    if tmp > WIDTH - 120: 
        player_x = WIDTH - 120
    if 0 <= tmp <= WIDTH - 120: 
        player_x = tmp #+= player_direction * player_speed 

    # khi bóng bay ra ngoài hoặc phá hết block 
    if ball_y >= HEIGHT - 10 or len(squares) == 0: 
        active = False
        player_x = 140 # điểm bắt đầu của thanh đón bòng 
        ball_x = WIDTH / 2 # vị trí bắt đầu của bóng trong game (trục x, y)
        ball_y = HEIGHT - 30 
        ball_x_direction = 0 
        ball_y_direction = 0 
        ball_x_speed = 5 # vận tốc di chuyển theo trục x, y của bóng 
        ball_y_speed = 5
        board = [[5,5,5,5,5],  # ma trận 2 * 2, mỗi điểm a[i][j] là 1 viên gạch, giá trị là màu của viên gạch đó
                [4,4,4,4,4],
                [3,3,3,3,3],
                [2,2,2,2,2]]
        new_game = True


    score_text = front.render(f'Score {score}', True, black)
    screen.blit(score_text, (10, 5)) 
    #
    if not active: 
        start_text = front.render('Space bar to start game', True, black)
        screen.blit(start_text, (20, 400)) 

    pygame.display.flip() # cập nhật màn hình 

pygame.quit() # đóng pygame và giải phóng toàn bộ tài nguyên 