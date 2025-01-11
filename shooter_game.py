from pygame import *
from random import randint
from time import time as timer

# Шрифти і написи
font.init()
font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (180, 0, 0))
font2 = font.Font(None, 36)

# Музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Зображення
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_ast = 'asteroid.png'

score = 0
goal = 25
lost = 0
max_lost = 20
life = 12

difficulty = 1  # За замовчуванням складність 1

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

menu = True  # Додано змінну для роботи меню

# Функція для налаштування швидкості відповідно до складності
# Функція для налаштування швидкості відповідно до складності
def set_difficulty_speed(difficulty_level):
    if difficulty_level == 1:
        monster_count = 5
        asteroid_count = 3
        reload_time = 1.5  
        return 1  # Легко
    elif difficulty_level == 2:
        monster_count = 7
        asteroid_count = 4
        reload_time = 1.3
        return 2  # Середня
    elif difficulty_level == 3:
        monster_count = 10
        asteroid_count = 5
        reload_time = 1
        return 3  # Складно
    elif difficulty_level == 4:
        monster_count = 15
        asteroid_count = 7
        reload_time = 0.8
        return 4  # Божевільно
    elif difficulty_level == 5:
        monster_count = 40
        asteroid_count = 25
        reload_time = 0.6
        return 4.35  # Божевільно+

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN and menu:
            x, y = e.pos
            if win_width // 2 - 100 <= x <= win_width // 2 + 100:
                if win_height // 2 - 50 <= y <= win_height // 2:
                    difficulty = 1
                    menu = False
                elif win_height // 2 + 10 <= y <= win_height // 2 + 60:
                    difficulty = 2
                    menu = False
                elif win_height // 2 + 70 <= y <= win_height // 2 + 120:
                    difficulty = 3
                    menu = False
                elif win_height // 2 + 130 <= y <= win_height // 2 + 180:
                    difficulty = 4  # Crazy
                    menu = False
                elif win_height // 2 + 190 <= y <= win_height // 2 + 240:
                    difficulty = 5  # Crazy+
                    menu = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not menu:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if menu:
        window.blit(background, (0,0))

        title = font1.render("Shooter Game", True, (255, 255, 255))
        easy = font2.render("Легко", True, (255, 255, 255))
        medium = font2.render("Середня", True, (255, 255, 255))
        hard = font2.render("Складно", True, (255, 255, 255))
        crazy = font2.render("Божевільно", True, (255, 255, 255))
        crazy_plus = font2.render("Божевільно+", True, (255, 255, 255))
        # Створюємо кнопки
        window.blit(title, (win_width // 2 - title.get_width() // 2, win_height // 2 - 150))
        draw.rect(window, (0, 255, 0), (win_width // 2 - 100, win_height // 2 - 50, 200, 50))
        draw.rect(window, (255, 255, 0), (win_width // 2 - 100, win_height // 2 + 10, 200, 50))
        draw.rect(window, (255, 0, 0), (win_width // 2 - 100, win_height // 2 + 70, 200, 50))
        draw.rect(window, (255, 150, 0), (win_width // 2 - 100, win_height // 2 + 130, 200, 50))
        draw.rect(window, (255, 89, 0), (win_width // 2 - 100, win_height // 2 + 190, 200, 50))
        # Встановлюємо кнопки на головне меню
        window.blit(easy, (win_width // 2 - easy.get_width() // 2, win_height // 2 - 40))
        window.blit(medium, (win_width // 2 - medium.get_width() // 2, win_height // 2 + 20))
        window.blit(hard, (win_width // 2 - hard.get_width() // 2, win_height // 2 + 80))
        window.blit(crazy, (win_width // 2 - crazy.get_width() // 2, win_height // 2 + 140))
        window.blit(crazy_plus, (win_width // 2 - crazy_plus.get_width() // 2, win_height // 2 + 200))

        display.update()
        continue

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        # Встановлення швидкості для монстрів і астероїдів в залежності від складності
        monster_speed = set_difficulty_speed(difficulty)
        asteroid_speed = set_difficulty_speed(difficulty) - 1  # Для астероїдів трохи менше

        # Оновлення швидкості для нових монстрів і астероїдів
        for monster in monsters:
            monster.speed = monster_speed
        for asteroid in asteroids:
            asteroid.speed = asteroid_speed

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        now_time = timer()
        if rel_time:
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3 + score // 10 * difficulty))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 10:
            life_color = (0, 150, 0)
        elif life == 5:
            life_color = (150, 150, 0)
        else:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 10

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 2))
            asteroids.add(asteroid)

    time.delay(50)
