import random

import pygame

from Camera import Camera
from Player import Player
from Enemy import Enemy
from Wall import createWalls


def reset():
    global player, enemies, turrets, bullets, walls, bg, camera, clock, screen, font20, score, width, height, sounds
    global LEFTPRESSED, RIGHTPRESSED, UPPRESSED, DOWNPRESSED, FIREPRESSED, TURRETPRESSED, RUNPRESSED, done, playing, debugMode
    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.init()

    width = 800
    height = 600
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("TD - by David")


    # indoor_bg = pygame.image.load("images/bgs/indoor_background.jpg")
    # forest_bg = pygame.image.load("images/bgs/forest_background.jpg")
    # grass_bg = pygame.image.load("images/bgs/grass_background.jpg")
    # rock_bg = pygame.image.load("images/bgs/rock_background.jpg")
    # ALL_BGS = [indoor_bg, forest_bg, rock_bg, grass_bg]
    # bg = ALL_BGS[random.randrange(0, ALL_BGS.__len__())]
    pygame.mixer.music.load("Sound/BGM.wav")
    pygame.mixer.music.play(-1)

    sounds = {
        "PlayerHitSound" : pygame.mixer.Sound("Sound/PlayerHit.wav"),
        "EnemyHitSound" : pygame.mixer.Sound("Sound/ZombieHit.wav"),
        "TurretDieSound" :  pygame.mixer.Sound("Sound/TurretDie.wav"),
        "WallDieSound" :  pygame.mixer.Sound("Sound/WallDie.wav")}

    font20 = pygame.font.Font("freesansbold.ttf", 20)

    player = Player(width / 2, height / 2)
    score = 0

    LEFTPRESSED = False
    RIGHTPRESSED = False
    UPPRESSED = False
    DOWNPRESSED = False
    FIREPRESSED = False
    TURRETPRESSED = False
    RUNPRESSED = False

    debugMode = True
    done = False
    playing = False
    player = Player(width / 2, height / 2)
    camera = Camera()
    enemies = []
    turrets = []
    bullets = []
    walls = createWalls()
    # bg = ALL_BGS[random.randrange(0, ALL_BGS.__len__())]
    bg = pygame.image.load("images/bgs/indoor_background.jpg")

if __name__ == '__main__':
    reset()


def spawnEnemy():
    minX = -950
    maxX = 950
    minY = -700
    maxY = 700

    if player.collider.centerX < width / 2:
        minX = width + 100
    if player.collider.centerX > width / 2:
        maxX = -100
    if player.collider.centerY < height / 2:
        minY = height + 100
    if player.collider.centerY > height / 2:
        maxY = -100
    if minX < maxX:
        if minY < maxY:
            enemies.append(Enemy(random.randrange(minX, maxX), random.randrange(minY, maxY), score))


BLACK = (0, 0, 0)
numEnemies = 100

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                playing = False
            else:
                playing = True
    screen.fill(BLACK)
    s = pygame.Surface((500, 60), pygame.SRCALPHA)
    s.fill((150, 150, 150, 100))
    screen.blit(s, (width / 2 - 250, height / 2 - 30))
    pygame.draw.rect(screen, BLACK, [width / 2 - 250, height / 2 - 30, 500, 60], 1)
    deadOutput = font20.render("Press any Key to Continue", 1, BLACK)
    rect = deadOutput.get_rect(center=(width / 2, height / 2))
    screen.blit(deadOutput, rect)
    pygame.display.flip()
    while playing:
        clock.tick(50)
        fps = clock.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    playing = False
                elif event.key == pygame.K_a:
                    LEFTPRESSED = True
                elif event.key == pygame.K_d:
                    RIGHTPRESSED = True
                elif event.key == pygame.K_w:
                    UPPRESSED = True
                elif event.key == pygame.K_s:
                    DOWNPRESSED = True
                elif event.key == pygame.K_SPACE:
                    TURRETPRESSED = True
                elif event.key == pygame.K_LSHIFT:
                    RUNPRESSED = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                FIREPRESSED = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    LEFTPRESSED = False
                elif event.key == pygame.K_d:
                    RIGHTPRESSED = False
                elif event.key == pygame.K_w:
                    UPPRESSED = False
                elif event.key == pygame.K_s:
                    DOWNPRESSED = False
                elif event.key == pygame.K_SPACE:
                    TURRETPRESSED = False
                elif event.key == pygame.K_LSHIFT:
                    RUNPRESSED = False
            elif event.type == pygame.MOUSEBUTTONUP:
                FIREPRESSED = False

        if RUNPRESSED:
            if player.moveSpeed != player.runSpeed:
                player.moveSpeed = player.runSpeed
        else:
            if player.moveSpeed != player.walkSpeed:
                player.moveSpeed = player.walkSpeed

        if LEFTPRESSED and not RIGHTPRESSED:
            player.moveLeft()
        elif RIGHTPRESSED and not LEFTPRESSED:
            player.moveRight()
        elif not LEFTPRESSED and not RIGHTPRESSED:
            player.stopHorizontal()

        if UPPRESSED and not DOWNPRESSED:
            player.moveUp()
        elif DOWNPRESSED and not UPPRESSED:
            player.moveDown()
        elif not UPPRESSED and not DOWNPRESSED:
            player.stopVertical()

        if TURRETPRESSED:
            player.placeTurret(turrets)
        if FIREPRESSED:
            player.shoot(bullets)
        if player.active:
            player.update(walls, camera)
        else:
            reset()
            playing = False

        for i in range(enemies.__len__() - 1, -1, -1):
            if not enemies[i].active:
                enemies.remove(enemies[i])
                score += 10
                if score % 100 == 0:
                    player.numTurrets += 1
            else:
                enemies[i].update(walls, turrets, player)
                if enemies[i].collider.collideWithCircle(player.collider) and enemies[i].active and player.active:
                    sounds["PlayerHitSound"].play()
                    enemies[i].attack(player)
                    vx = -(player.centerX - enemies[i].centerX)
                    vy = -(player.centerY - enemies[i].centerY)
                    player.centerX -= vx
                    player.centerY -= vy
                    camera.offsetX -= vx
                    camera.offsetY -= vy
        for i in range(turrets.__len__() - 1, -1, -1):
            if not turrets[i].active:
                sounds["TurretDieSound"].play()

                turrets.remove(turrets[i])
            else:
                turrets[i].update(bullets)
                for j in range(enemies.__len__()):
                    if enemies[j].collider.collideWithCircle(turrets[i].collider) and enemies[j].active and turrets[i].active:
                        enemies[j].attack(turrets[i])
        for i in range(bullets.__len__() - 1, -1, -1):
            if not bullets[i].active:
                bullets.remove(bullets[i])
            elif bullets[i].life > 0:
                bullets[i].update()
                for j in range(enemies.__len__()):
                    if enemies[j].collider.collideWithCircle(bullets[i].collider) and enemies[j].active and bullets[i].active:
                        sounds["EnemyHitSound"].play()
                        bullets[i].attack(enemies[j])
                        bullets[i].active = False
                        # vx = -(enemies[j].centerX - bullets[i].centerX) * 10
                        # vy = -(enemies[j].centerY - bullets[i].centerY) * 10
                        # enemies[j].centerX -= vx
                        # enemies[j].centerY -= vy


        for i in range(walls.__len__() - 1, -1, -1):
            if not walls[i].active:
                sounds["WallDieSound"].play()
                walls.remove(walls[i])
            else:
                walls[i].update()
                for j in range(bullets.__len__() - 1, -1, -1):
                    if walls[i].collider.collideWithCircle(bullets[j].collider) and bullets[j].active:
                        bullets[j].active = False

        if enemies.__len__() < numEnemies:
            spawnEnemy()

        screen.fill(BLACK)
        rect = bg.get_rect()
        rect.x = -950 - camera.offsetX
        rect.y = -700 - camera.offsetY
        screen.blit(bg, rect)
        for i in range(walls.__len__()):
            walls[i].draw(screen, camera)
        for i in range(enemies.__len__()):
            enemies[i].draw(screen, turrets, player, camera)
        for i in range(turrets.__len__()):
            turrets[i].draw(screen, enemies, camera)
        for i in range(bullets.__len__()):
            bullets[i].draw(screen, camera)
        player.draw(screen, camera)

        s = pygame.Surface((500, 60), pygame.SRCALPHA)
        s.fill((150, 150, 150, 100))
        screen.blit(s, (0, 0))
        pygame.draw.rect(screen, BLACK, [0, 0, 500, 60], 1)
        pygame.draw.rect(screen, (255, 0, 0), [10, 20, 100 * (player.health / 100), 20], 0)
        pygame.draw.rect(screen, BLACK, [10, 20, 100, 20], 1)
        turretCountOutput = font20.render("Turrets: " + str(player.numTurrets), 1, BLACK)
        screen.blit(turretCountOutput, (120, 10))
        enemyCountOutput = font20.render("Enemies: " + str(enemies.__len__()), 1, BLACK)
        screen.blit(enemyCountOutput, (120, 30))
        scoreOutput = font20.render("Score: " + str(score), 1, BLACK)
        screen.blit(scoreOutput, (300, 20))
        if not player.active:
            s = pygame.Surface((500, 60), pygame.SRCALPHA)
            s.fill((150, 150, 150, 100))
            screen.blit(s, (width / 2 - 250, height / 2 - 30))
            pygame.draw.rect(screen, BLACK, [width / 2 - 250, height / 2 - 30, 500, 60], 1)
            deadOutput = font20.render("You Died! Final Score: " + str(score), 1, BLACK)
            rect = deadOutput.get_rect(center=(width/2, height/2))
            screen.blit(deadOutput, rect)
        if debugMode:
            s = pygame.Surface((80, 30), pygame.SRCALPHA)
            s.fill((150, 150, 150, 100))
            screen.blit(s, (width - 80, height - 30))
            pygame.draw.rect(screen, BLACK, [width - 80, height - 30, 80, 30], 1)
            debugFpsOutput = font20.render("FPS: " + str(int(fps)), 1, BLACK)
            rect = debugFpsOutput.get_rect(bottom=height, right=width)
            screen.blit(debugFpsOutput, rect)
        pygame.display.flip()
        print(str(FIREPRESSED))