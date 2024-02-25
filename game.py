import pygame
import random
import time
from pygame.color import THECOLORS

# Инициализация Pygame
pygame.mixer.pre_init(44100, 16, 4, 4096)
pygame.init()

# Параметры экрана и игры
w, h = 400, 708
fps = 60
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

# Загрузка изображений
bird_images = [pygame.image.load(f"images/{i}.png").convert_alpha() for i in range(3)]
background = pygame.image.load("images/background.png").convert_alpha()
bottom = pygame.image.load("images/bottom.png").convert_alpha()
dead = pygame.image.load("images/dead.png").convert_alpha()
top = pygame.image.load("images/top.png").convert_alpha()
bonus = pygame.image.load("images/bonus.png").convert_alpha()
flappyhop_images = [pygame.image.load(f"images/flappyhop{i}.png").convert_alpha() for i in range(1, 5)]

# Загрузка звуков
jump = pygame.mixer.Sound("sounds/jump.mp3")
Over = pygame.mixer.Sound("sounds/Over.mp3")
zvuk = pygame.mixer.Sound("sounds/bonus.mp3")
Over.set_volume(1)
pygame.mixer.music.set_volume(0.3)

# Инициализация переменных
bird, bird_index = bird_images[0], 0
animation = iter(flappyhop_images)
tempanimation = iter(flappyhop_images)
speed = 3
xbird, ybird = 50, 50
xtop, ytop, xbot, ybot = w, -300, w, 450
distance = -1000
score, second = 0, 3
draw_second, jumpanimation, godmode, nowf, show_bonus = False, False, False, False, False
xbonus, ybonus = w, h / 2
now, now2 = 0, 0
GameOver, scoref = False, True
# Сохранение рекорда
record = 0
try:
    with open('record.txt', 'r') as file:
        record = int(file.read())
except FileNotFoundError:
    pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not GameOver:
                # Прыжок при нажатии на пробел
                ybird -= 75
                jump.play()
                bird = random.choice(bird_images)
                jumpanimation = True
                tempanimation = iter(flappyhop_images)

            if event.key == pygame.K_r and GameOver:
                # Рестарт игры при нажатии на 'R'
                GameOver = False
                bird, xbird, ybird = bird_images[0], 50, 50
                xtop, ytop, xbot, ybot = w, -300, w, 450
                score = 0
                ybonus, show_bonus = -1000, False
                text = pygame.font.Font('pixel.ttf', 76).render(str(score), True, (0, 0, 0))
                scoref = True  # Add this line to reset scoref


    if not GameOver:
        if jumpanimation:
            # Анимация прыжка
            if time.time() - now > 0.15:
                now = time.time()
                try:
                    bird = next(tempanimation)
                except StopIteration:
                    jumpanimation = False
        else:
            now = time.time()

        #Движение труб
        xtop-=speed
        xbot-=speed
        ybird+=speed
        if xtop<-50:
            xtop=w
            ytop=distance-230
            scoref=True
            show_bonus=random.choice((1,0,0,0))
        if xbot<-50:
            xbot=w
            ybot=450+distance
        if ybird > h or ybird < 0:
            Over.play()
            GameOver = True
        distance=random.randint(-210,230)

        #Бонус
        bonus_rect = bonus.get_rect(x=xbonus - 15, y=ybonus)
        bird_rect = bird.get_rect(x=xbird - 30, y=ybird)
        # При столкновении с бонусом
        if bird_rect.colliderect(bonus_rect) and show_bonus:
            second -= 1
            draw_second = True
            nowf = True
            godmode = True
            zvuk.play()
            show_bonus = False

        if nowf:
            now2 = time.time()
            nowf = False

        if time.time() - now2 > 5:
            godmode = False
            second = max(0, second - 1)  # Уменьшаем таймер бонуса, но не ниже 0
        else:
            second = max(0, 5 - round(time.time() - now2))  # Обновляем таймер бонуса

        bot_rect = bottom.get_rect(x=xbot, y=ybot)
        top_rect = top.get_rect(x=xtop, y=ytop)

        xbonus -= speed
        if xbonus < -50:
            xbonus = xbot

        ybonus = bot_rect.topleft[1] - 100

        if (bird_rect.colliderect((bot_rect)) or bird_rect.colliderect((top_rect))) and (not godmode):
            # Обработка столкновения с трубами
            Over.play()
            GameOver = True
            bird = dead

        if xbird > xtop and scoref:
            # Увеличение счета при прохождении трубы
            scoref = False
            score += 1

        outcome = f"Ваш счёт: {score}"
        text1 = pygame.font.Font('pixel.ttf', 76).render(str(second), True, (0, 0, 0))
        text2 = pygame.font.Font('pixel.ttf', 76).render(str(outcome), True, THECOLORS["red1"])

        screen.blit(background, (0, 0))
        screen.blit(top, (xtop, ytop))
        screen.blit(bottom, (xbot, ybot))
        screen.blit(bird, (xbird, ybird))

        if GameOver:
            screen.blit(text2, (100, 300))
            draw_second = False
            if score > record:
                record = score
                with open('record.txt', 'w') as file:
                    file.write(str(record))
            recordText = pygame.font.Font('pixel.ttf', 76).render(str(f"Ваш рекорд: {record}"), True, THECOLORS["red1"])
            screen.blit(recordText, (80, 380))



        if draw_second and second != 0:
            screen.blit(text1, (50, 50))

        if GameOver:
            draw_second = False

        if not GameOver:
            text = pygame.font.Font('pixel.ttf', 76).render(str(score), True, (0, 0, 0))
            screen.blit(text, (300, 50))

        if show_bonus:
            screen.blit(bonus, (xbonus, ybonus))

        pygame.display.update()
    clock.tick(fps)

pygame.quit()
