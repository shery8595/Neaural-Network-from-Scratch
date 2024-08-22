import pygame
import neat
import os
import random
from gamedino import SH, SW, Dinosaur, Cloud, SCREEN, SmallCactus, SMALL_CACTUS, LargeCactus, LARGE_CACTUS, Bird, BIRD, BG

pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption('Dino')

def eval_genomes(genomes, config):
    nets = []
    dinos = []
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dinosaur())
        genome.fitness = 0
        ge.append(genome)

    run = True
    Clock = pygame.time.Clock()
    cloud = Cloud()
    
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles

    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 480
    points = 0
    font = pygame.font.Font(r'D:\arial.ttf', 20)
    obstacles = []

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (520, 30)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run and len(dinos) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))

        for i, dino in enumerate(dinos):
            dino.update()  # Update dino based on its state
            
            # Neural network input: Dino's y-position, horizontal distance to obstacle, vertical distance to obstacle
            if len(obstacles) > 0:
                input_data = (
                    dino.dino_rect.y,  # Dino's y-position
                    obstacles[0].rect.x - dino.dino_rect.x,  # Horizontal distance to the obstacle
                    obstacles[0].rect.y - dino.dino_rect.y,  # Vertical distance to the obstacle
                    dino.dino_rect.y - obstacles[0].rect.y,  # Relative height difference
                    dino.dino_rect.x,  # Dino's current x-position
                    obstacles[0].rect.width,  # Width of the obstacle
                    obstacles[0].rect.height  # Height of the obstacle
                )

                output = nets[i].activate(input_data)
                if output[0] > output[1] and output[0] > output[2]:  # Jump if the output is above a threshold
                    dino.dino_jump = True
                    dino.dino_duck = False
                    dino.dino_run = False
                elif output[1] > output[0] and output[1] > output[2]:  # Duck if the second output is above a threshold
                    dino.dino_duck = True
                    dino.dino_jump = False
                    dino.dino_run = False
                elif output[2] > output[0] and  output[2] > output[1]:
                    dino.dino_duck = False
                    dino.dino_jump = False
                    dino.dino_run = True
                    
                # Fitness for staying alive
            ge[i].fitness += 0.1
            
            # Fitness for distance covered (additional reward)
            ge[i].fitness += 0.01
                    

            dino.draw(SCREEN)

        # Handle obstacles
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            for i, dino in enumerate(dinos):
                if dino.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 5
                    dinos.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    break  # Break out of the for loop after removing dino

            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)

        cloud.draw(SCREEN)
        cloud.update()
        background()
        score()
        Clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    config_path = r'C:\Users\hp\python programs\neat-dino.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    winner = p.run(eval_genomes, 50)
