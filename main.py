import pygame, sys,random

def draw_ground(): #размешение земли на экране
    screen.blit(ground_surf, (ground_x, 900))
    screen.blit(ground_surf, (ground_x + 1920, 900))

def create_let(): #
    random_let_pos = random.choice(let_height)
    bottom_let = let_surf.get_rect(midtop = (2000,random_let_pos))
    top_let = let_surf.get_rect(midbottom = (2000, random_let_pos - 350))
    return bottom_let, top_let

def move_let(lets): #все препятсвия сдвинуть влево
    for let in lets:
        let.centerx -= 8 #скорость перемещения препятствий
    visible_lets = [let for let in lets if let.right > -50]
    return visible_lets

def draw_lets(lets): #показать на экране препятствия
    for let in lets:
        if let.bottom >= 1080:
            screen.blit(let_surf, let)
        else: #перевернуть препятствие
            flip_let = pygame.transform.flip(let_surf,False,True)
            screen.blit(flip_let,let)

def check_collision(lets):
    global score, can_score
    for let in lets:
        if skat_rect.colliderect(let): #косание препятсвий
            death_sound.play() #проигрывание звука соприкосновения
            can_score = True
            return False

    if skat_rect.top <= -100 or skat_rect.bottom >= 900: #выход за пределы экрана
        death_sound.play()
        can_score = True
        return  False

    return  True

def rotate_skat(skat):
    new_skat = pygame.transform.rotozoom(skat, -skat_moment *3, 1) #угол наклона
    return new_skat

def skat_animation(): #отрисвока прямоугольника вокруг персонажа
    new_skat = skat_frames[skat_index]
    new_skat_rect = new_skat.get_rect(center = (100, skat_rect.centery))
    return new_skat, new_skat_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surf = game_font.render(f'{(int(score))}',True,(255,255,255))
        score_rect = score_surf.get_rect(center = (960,100))
        screen.blit(score_surf,score_rect)
    if game_state == 'game_over': #f-строка объединяет переменную str с любой другой переменной
        score_surf = game_font.render(f'Score: {(int(score))}', True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(960, 100))
        screen.blit(score_surf, score_rect)

        high_score_surf = game_font.render(f'High score: {(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surf.get_rect(center=(960, 850))
        screen.blit(high_score_surf, high_score_rect)

def update_score(score, high_score): #обновление хай скора
    if score > high_score:
        high_score = score
    return high_score

def let_score_check(): #усповие получения очка
    global score, can_score

    if let_list:
        for let in let_list:
            if 95 < let.centerx < 105 and can_score:
                score +=1
                score_sound.play()
                can_score = False
            if let.centerx < 0:
                can_score = True

pygame.init()
pygame.display.set_caption("sea paradise")
screen = pygame.display.set_mode((1920,1080)) #разрешение экрана
clock = pygame.time.Clock()  #переменная для частоты кадров
game_font = pygame.font.Font('SkazkaForSerge.ttf',40) #шрифт



#Игровые переменные
gravity = 0.25 #сила гравитации
skat_moment = 0
game_active = True
score = 0
high_score = 0
can_score = True

# Задний фон
bg_surf = pygame.image.load('assets/bg.png').convert_alpha() #

# Земля
ground_surf = pygame.image.load('assets/gr.png').convert_alpha()
ground_x = 0

# Скат
skat_one = pygame.transform.scale(pygame.image.load('assets/1.png'),(118,82)).convert_alpha()
skat_two = pygame.transform.scale(pygame.image.load('assets/2.png'),(118,82)).convert_alpha()
skat_three = pygame.transform.scale(pygame.image.load('assets/3.png'),(118,82)).convert_alpha()
skat_four = pygame.transform.scale(pygame.image.load('assets/4.png'),(118,82)).convert_alpha()
skat_five = pygame.transform.scale(pygame.image.load('assets/5.png'),(118,82)).convert_alpha()
skat_six = pygame.transform.scale(pygame.image.load('assets/6.png'),(118,82)).convert_alpha()
skat_seven = pygame.transform.scale(pygame.image.load('assets/7.png'),(118,82)).convert_alpha()
skat_eight = pygame.transform.scale(pygame.image.load('assets/8.png'),(118,82)).convert_alpha()
skat_frames = [skat_one,skat_two,skat_three, skat_four, skat_five, skat_six, skat_seven, skat_eight] #список анимаций
skat_index = 0
skat_surf = skat_frames[skat_index]
skat_rect = skat_surf.get_rect(center = (100, 450)) #создать прямоугольник вокруг поверхности

pygame.display.set_icon(skat_one)

SKATFLIP = pygame.USEREVENT + 1 #создание события
pygame.time.set_timer(SKATFLIP, 80) #время проигрывания анимации


#Препятствия
let_surf = pygame.image.load('assets/let.png').convert_alpha()
let_surf = pygame.transform.scale2x(let_surf)
let_list = []
SPAWNLET = pygame.USEREVENT #создание события
pygame.time.set_timer(SPAWNLET, 1200) #время появления препятствия
let_height = [450,500,550,650,700,750,800] #высота препятствий

game_over_surf = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha()) #экран проигрыша
game_over_rect = game_over_surf.get_rect(center = (960,540))

flap_sound = pygame.mixer.Sound('sounds/audio_wing.mp3')
death_sound = pygame.mixer.Sound('sounds/audio_hit.mp3')
score_sound = pygame.mixer.Sound('sounds/audio_point.mp3')
score_sound_countdown = 100



while True:
    for event in pygame.event.get(): #событие закрытия окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #завершение цикла

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: #прыжок
                skat_moment = 0
                skat_moment -= 11 #сила прыжка
                flap_sound.play() #проигрывание звука
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True #перезапуск игры
                let_list.clear()
                skat_rect.center = (100, 450)
                skat_moment = 0
                score = 0

        if event.type == SPAWNLET:
            let_list.extend(create_let())

        if event.type == SKATFLIP: #событие анимации
            if skat_index < 7:
                skat_index += 1
            else:
                skat_index = 0
            skat_surf,skat_rect = skat_animation()


    screen.blit(bg_surf,(0,0)) #помещение bg

    if game_active:

        #skat
        skat_moment += gravity
        rotated_skat = rotate_skat(skat_surf)
        skat_rect.centery += skat_moment
        screen.blit(rotated_skat,skat_rect)
        game_active = check_collision(let_list)

        #let
        let_list = move_let(let_list)
        draw_lets(let_list)

        #score
        let_score_check()

        score_display('main_game')

        ground_x -= 1
        draw_ground()
        if ground_x <= -1920:
            ground_x = 0

    else:
        screen.blit(game_over_surf,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

        #передвижение земли
        ground_x -= 1
        draw_ground()
        if ground_x <= -1920:
            ground_x = 0




    #обновление экрана и частота кадров
    pygame.display.update()
    clock.tick(120)
