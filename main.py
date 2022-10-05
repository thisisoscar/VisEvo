import pygame as pg
import random

pg.init()
width = 950
height = 535
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
ages = []

def mutate_rgb(r, g, b):
    if r == False:
        rgb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    else:
        rgb = [r, g, b]
    
    choice = random.randint(0, 2)
    if rgb[choice] + 10 > 255:
        rgb[choice] = random.randint(245, 255)
    elif rgb[choice] - 10 < 0:
        rgb[choice] = random.randint(0, 10)
    else:
        rgb[choice] = random.randint(rgb[choice]-10, rgb[choice]+10)

    return rgb

class Animal(pg.sprite.Sprite):
    def __init__(self, pos, size, colour, speed):
        super().__init__()
        self.image = pg.Surface(size)
        self.given_colour = colour
        self.image.fill(self.given_colour)
        self.rect = self.image.get_rect(center=pos)
        self.age = 0
        
        self.max_health = 100
        self.health = self.max_health
        self.speed = speed


    def update(self):
        self.age += 1
        direction = random.randint(0, 1)
        amount = random.choice((-1, 1))
        if direction == 0:
            self.rect.x += amount * self.speed
        else:
            self.rect.y += amount * self.speed
            
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height

        self.health -= abs(self.speed) + 1
        collisions = [i for i in food_group.sprites() if self.rect.colliderect(i.rect)]
        if pg.sprite.spritecollide(self, food_group, True):
            self.health = self.max_health
            for i in range(len(collisions)):
                animals_group.add(Animal(
                                        [self.rect.centerx, self.rect.centery],
                                        [5,5],
                                        mutate_rgb(self.given_colour[0], self.given_colour[1], self.given_colour[2]),
                                        random.randint(self.speed-1, self.speed+1)
                                        ))

        if self.health <= 0:
            animals_group.remove(self)
            food_group.add(Food(
                                [self.rect.x, self.rect.y],
                                [5,5],
                                [0,255,0]))


class Food(pg.sprite.Sprite):
    def __init__(self, pos, size, colour):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect(center=pos)


animals_group = pg.sprite.Group()
for i in range(3):
    animals_group.add(Animal(
                            [random.randint(0,width), random.randint(0,height)],
                            [5,5],
                            mutate_rgb(False, False, False),
                            random.randint(1, 10)
                            ))

food_group = pg.sprite.Group()
for i in range(5000):
    food_group.add(Food(
                        [random.randint(0,width), random.randint(0,height)],
                        [5,5],
                        [0,255,0]))
    

running = True
while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    
    for i in range(0):
        food_group.add(Food(
                            [random.randint(0,width), random.randint(0,height)],
                            [5,5],
                            [0,255,0]))


    animals_group.update()
    # colour in the oldest ones blue if I wanted
    '''oldest = 0
    for i in animals_group:
        if i.speed > oldest and i.speed != 0:
            oldest = i.speed
    found = False
    for i in animals_group:
        if i.speed == oldest and not found:
            i.image.fill([0, 0, 255])
            found = True
        else:
            i.image.fill([255, 0, 0])'''

    animals_group.draw(screen)
    food_group.draw(screen)
    pg.display.flip()
    clock.tick(60)

    average = 0
    average2 = 0
    average3 = 0
    length = 0
    ages_new = []
    for i in animals_group:
        average += i.speed
        average2 += i.health
        if i.speed != 0:
            average3 += i.age
            length += 1
        ages_new.append(i.age)
    ages.append(ages_new)
    average /= len(animals_group)
    average2 /= len(animals_group)
    average3 /= length
    print(f'{len(animals_group)} {round(average, 3)} {round(average2, 3)} {round(average3, 3)} {len(animals_group) + len(food_group)}')
