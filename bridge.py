import pygame

class Bridge:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.world = game.world
        self.joints = []
        self.cost = 0
        self.stress = 0
        self.capacity = 1
        self.first_train = None
        self.train_off_screen = False
        self.train_was_created = False
        self.level_completed = False
        self.sounds = {"wooo":loadSound("sounds/wooo.wav"), "death":loadSound("sounds/death.wav"), "startup":loadSound("sounds/startup.wav")}

    def restart(self):
        self.world.run_physics = False
        self.train_off_screen = False
        self.level_completed = False
        self.train_was_created = False

    def create_world(self):
        self.world.set_color((100,150,50))
        rect = pygame.Rect((-400,800), (750, -250))
        rect.normalize()
        pygame.draw.rect(self.screen, (100,180,255), rect, 3)
        self.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
            dynamic=False)
        rect = pygame.Rect((1600,800), (-750, -250))
        rect.normalize()
        pygame.draw.rect(self.screen, (100,180,255), rect, 3)
        self.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
            dynamic=False)
        self.world.reset_color()

    def add_cost(self, value):
        self.cost = self.cost + value
        print "cost now", value

    def joint_added(self, joint):
        print "joint added!"
        self.joints.append(joint)
        self.add_cost(100)
        self.capacity += 500

    def box_added(self):
        self.add_cost(10)

    def for_each_frame(self):
        self.stress = 0
        for joint in self.joints:
            force = joint.GetReactionForce().Length()
            self.stress += force

            if force > 500:
                print "destroy joint!"
                self.world.world.DestroyJoint(joint)
                self.joints.remove(joint)
                self.capacity -= 500
            else:
                vec = joint.GetAnchor1()
                coord = int(self.world.meter_to_screen(vec.x)),int(780 - self.world.meter_to_screen(vec.y))
                pygame.draw.circle(self.screen, (int(force/2),255-int(force/2),0), coord, 4)

        pos = self.first_train.GetPosition()
        if pos.x > 14.0:
            if not self.level_completed:
                self.level_completed = True
                self.sounds['wooo'].play()
        elif pos.y < 0.0:
            if not self.train_off_screen:
                self.sounds['death'].play()
                print "TRAIN FELL OFF!", pos.x
                self.train_off_screen = True

    def create_train(self, worldpoint = (-100,490), train = (100, 50), wheelrad = 20, cars = 3, force = False):
        if not force and self.train_was_created:
            return
        self.sounds['startup'].play()
        self.train_was_created = True
        points = []
        self.train_off_screen = False
        for i in range(0,cars):
            startpoint = (worldpoint[0]-(train[0]+7)*i, worldpoint[1])
            points.append(startpoint)
            rect = pygame.Rect(startpoint, train)
            rect.normalize()
            pygame.draw.rect(self.screen, (200, 50, 100), rect, 3)
            rect = self.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
                dynamic = True, density=10.0, restitution=0.16, friction=0.5)
            if i == 0:
                self.first_train = rect
                
            self.world.set_color((0,0,0))
            rearwheel = (startpoint[0]+wheelrad,startpoint[1]+train[1]-wheelrad/2)
            pygame.draw.circle(self.screen, (0,0,0), rearwheel, wheelrad, 3)
            self.world.add.ball(rearwheel,wheelrad, dynamic=True, density=10.0, 
                restitution=0.16, friction=0.5)
    
            frontwheel = (startpoint[0]+train[0]-wheelrad,startpoint[1]+train[1]-wheelrad/2)
            pygame.draw.circle(self.screen, (0,0,0), frontwheel, wheelrad, 3)
            self.world.add.ball(frontwheel,wheelrad, dynamic=True, density=10.0, 
                restitution=0.16, friction=0.5)
            self.world.reset_color()
            
            rearaxle = self.world.get_bodies_at_pos(rearwheel)
            frontaxle = self.world.get_bodies_at_pos(frontwheel)
            if len(rearaxle) == 2:
                self.world.add.jointMotor(rearaxle[0],rearaxle[1],rearwheel)
            if len(frontaxle) == 2:
                self.world.add.jointMotor(frontaxle[0],frontaxle[1],frontwheel)
            
        for i in range(1,len(points)):
            backlink = (points[i][0]+train[0]-1,points[i][1]+train[1]-1)
            frontlink = (points[i-1][0]+1,points[i-1][1]+train[1]-1)
            btrain = self.world.get_bodies_at_pos(backlink)
            ftrain = self.world.get_bodies_at_pos(frontlink)
            if len(ftrain) and len(btrain):
                self.world.add.distanceJoint(btrain[0], ftrain[0], backlink, frontlink)

# function for loading sounds (mostly borrowed from Pete Shinners pygame tutorial)
def loadSound(name):
    # if the mixer didn't load, then create an empy class that has an empty play method
    # this way the program will run if the mixer isn't present (sans sound)
    class NoneSound:
        def play(self): pass
        def set_volume(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except:
        print "error with sound: " + name
        return NoneSound()
    return sound

