import pygame
import os
import random
import pygame.mixer

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("cv_space_running")

RUNNING = [pygame.image.load(os.path.join("resource/suisei_run", "r3.png")),
           pygame.image.load(os.path.join("resource/suisei_run", "r1.png")),
           pygame.image.load(os.path.join("resource/suisei_run", "r4.png")),
           pygame.image.load(os.path.join("resource/suisei_run", "r2.png"))]

JUMPING = pygame.image.load(os.path.join("resource/jump", "j2.png"))

BULLET = [pygame.image.load(os.path.join("resource/bullet", "b1.png")),
          pygame.image.load(os.path.join("resource/bullet", "b2.png")),
          pygame.image.load(os.path.join("resource/bullet", "b3.png"))]


HoShiYoMi = [pygame.image.load(os.path.join("resource/en", "hsy.jpg")),
             pygame.image.load(os.path.join("resource/en", "hsy.jpg"))]

lost = pygame.image.load(os.path.join("resource", "Los.jpg"))

decorate = [pygame.image.load(os.path.join("resource/deco", "d1.jpg")),
            pygame.image.load(os.path.join("resource/deco", "d2.jpg")),
            pygame.image.load(os.path.join("resource/deco", "d3.jpg")),
            pygame.image.load(os.path.join("resource/deco", "d4.jpg")),]


# 載入背景圖片
back = pygame.image.load(os.path.join("resource/bg", "bg.jpg")).convert()
# 載入前景圖片
BG = pygame.image.load(os.path.join("resource/bg", "road.jpg")).convert_alpha()
#set icon
icon = pygame.image.load(os.path.join("resource", 'icon.jpg'))
pygame.display.set_icon(icon)
pygame.mixer.init()

# 載入MP3音樂文件
songs = [(os.path.join("resource/bgm", 'lightnessBoss.mp3')),
         (os.path.join("resource/bgm", 'lightnessOnTheWay.mp3')),
         (os.path.join("resource/bgm", 'mainTitle.mp3')),
         (os.path.join("resource/bgm", '上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')),
         (os.path.join("resource/bgm", '金卡雷 - 引燃夜空的星火.mp3')),
         (os.path.join("resource/bgm", '金卡雷 - 风中花，雪中月.mp3'))]
current_song = random.choice(songs)  # 隨機選擇一首歌曲

def play_next_song():
    global current_song
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play()
    current_song = random.choice(songs)  # 選擇下一首要播放的歌曲

#set main char
class SuiSei:
    X_POS = 120
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.SuiSei_run = True
        self.SuiSei_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.SuiSei_rect = self.image.get_rect()
        self.SuiSei_rect.x = self.X_POS
        self.SuiSei_rect.y = self.Y_POS
        self.jump_sound = pygame.mixer.Sound(os.path.join("resource",'jmu1.mp3'))

    #set logic,run&jump
    def update(self, userInput):
        if self.SuiSei_run:
            self.run()
        if self.SuiSei_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.SuiSei_jump:
            self.SuiSei_run = False
            self.SuiSei_jump = True
            self.jump_sound.play()  # 播放跳躍音效
        elif not (self.SuiSei_jump or userInput[pygame.K_DOWN]):
            self.SuiSei_run = True
            self.SuiSei_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 3]
        self.SuiSei_rect = self.image.get_rect()
        self.SuiSei_rect.x = self.X_POS
        self.SuiSei_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.SuiSei_jump:
            self.SuiSei_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.SuiSei_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.SuiSei_rect.x, self.SuiSei_rect.y))


#background  decoration
class deco:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(500, 1000)
        self.y = random.randint(50, 100)
        self.images = decorate  # 將四幅圖片存入列表
        self.image_index = 0  # 追踪目前使用的圖片索引
        self.width = self.images[self.image_index].get_width()


    def draw(self, screen):
        screen.blit(self.images[self.image_index], (self.x, self.y))

    def update(self):
        self.x -= game_speed - 15
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 1000)
            self.y = random.randint(50, 100)
            self.image_index = (self.image_index + 1) % 4  # 使用取餘數運算子循環圖片索引


#point or Obstacle
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

#Obstacle
class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350

#point
class hosy(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 290
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


FPS = 10
#game run
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = SuiSei()
    Decorate = deco()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 0.5

        text = font.render("Points: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((0, 0, 0))
        # 繪製背景圖片
        SCREEN.blit(back, (0, 0))
        # 繪製前景圖片
        SCREEN.blit(BG, (0, 420))
        #paly music
        if not pygame.mixer.music.get_busy():
            play_next_song()
        userInput = pygame.key.get_pressed()
        Decorate.draw(SCREEN)
        Decorate.update()
        player.draw(SCREEN)
        player.update(userInput)
        #obs
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Cactus(BULLET))
            if random.randint(0, 2) == 1:
                obstacles.append(Cactus(BULLET))
            elif random.randint(0, 2) == 2:
                obstacles.append(hosy(HoShiYoMi))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.SuiSei_rect.colliderect(obstacle.rect):
                if isinstance(obstacle, hosy):
                    points += 50
                    obstacles.remove(obstacle)
                else:
                    death_count += 1
                    menu(death_count)

        score()
        clock.tick(30)
        pygame.display.update()


#menu start & lost
def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            SCREEN.blit(lost, (0, 0))
            score = font.render("Your Score: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
