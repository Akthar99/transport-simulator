import json 
import pygame
# from graphics import *
SCREEN_HEIGHT, SCREEN_WIDTH = 1280, 720
PATH_DISTANCE = 3000

class RectangleL:
    def __init__(self, width: int, height: int, x: int, y: int):
        self.width = width
        self.height = height
        self.x = x
        self.y = y


class People(pygame.sprite.Sprite):
    def __init__(self,waiting_city, name, color, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.name = name
        self.wait_time: int = 0
        self.waiting_city: City = waiting_city
        self.destination_location: City = None
    
    def get_waiting_city(self):
        return self.waiting_city
    
    def get_wait_time(self):
        return self.wait_time
    
    def get_position(self):
        return self.rect

class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class City(pygame.sprite.Sprite):
    """@name - name of the city (string)
       @people - how many people are waiting (int) 
    """
    def __init__(self, name: str, color,x: int, y: int, amount: int, group):
        super().__init__(group)
        self.cemera_group = group
        self.image = pygame.Surface((200, 200))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.name = name
        self.people = amount

    def get_position(self) -> tuple:
        return self.rect.topleft

    def add_people(self, crowd_list: list):
        if len(crowd_list) < self.people and len(crowd_list) != self.people:
            last_person_pos = (crowd_list[-1].get_position().x, crowd_list[-1].get_position().y)
            if (not len(crowd_list) % 8 == 0):
                p = People(self.name,"person"+str(len(crowd_list)), "black", last_person_pos[0] + 10, last_person_pos[1] + 25 + 10, self.cemera_group)
                crowd_list.append(p)
            else:
                p = People(self.name,"person"+str(len(crowd_list)), "black", last_person_pos[0] + 25 + 10, self.rect.top + 10, self.cemera_group)
                crowd_list.append(p)
        else:
            raise RuntimeError("No more space left in the city" + len(crowd_list))
        

class Bus(pygame.sprite.Sprite):
    def __init__(self, color, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((60, 40)) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position: pygame.math.Vector2
        self.nearest_city: City
        self.speed: int = 5


    def update(self):
        if (self.rect.x >= 3000):
            self.rect.move_ip(0, 0)
        else: 
            self.rect.move_ip(self.speed, 0)


class Map(pygame.sprite.Sprite):
    def __init__(self, color, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((PATH_DISTANCE, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    """
    make a path to bus to follow 
    """
    def init(self):
        pass
        
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] / 2
        self.half_h = self.display_surface.get_size()[1] / 2

    def centered_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    # we can customize the draw method if i want to control the layout how things should draw 
    def custom_draw(self):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


def main():
# making user interface using pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
    clock = pygame.time.Clock()
    running: bool = True
    crowd = []
    cities = []

    camera_group = CameraGroup()
    map = Map("black", PATH_DISTANCE/2, SCREEN_WIDTH/2, camera_group)
    bus = Bus("white", 35, SCREEN_WIDTH/2, camera_group)
    colombo = City(name="Colombo", color="yellow", x=(PATH_DISTANCE/4 * 1), y=SCREEN_WIDTH/2 - 125, amount=64, group=camera_group)
    kalutara = City(name="Kalutara", color="yellow", x=(PATH_DISTANCE/4 * 2), y=SCREEN_WIDTH/2 - 125, amount=64, group=camera_group)

    # add people to colombo city
    for i in range(8):
        for n in range(8):
            person1 = People("colombo","person"+str(i), "black", colombo.get_position()[0] + (i * 25) + 10, colombo.get_position()[1] + (n * 25) + 10, camera_group)
            crowd.append(person1)


    cities.append(colombo)
    cities.append(kalutara)

    for i in range(40):
        p = crowd.pop()
        camera_group.remove(p)

    for i in range(15):
        colombo.add_people(crowd)
    print(crowd[0].get_position().x)
    print(len(crowd))


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill("purple")

        camera_group.update()
        camera_group.centered_camera(bus)
        camera_group.custom_draw()


        pygame.display.flip()

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()