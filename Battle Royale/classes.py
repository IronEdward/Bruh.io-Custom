class Gun:
    decay_rate = 2
    class submachine_gun:
        def __init__(self):
            self.speed = 35
            self.force = 2
            self.decay = 50
            self.bullet_size = 3
    class shotgun:
        def __init__(self):
            self.speed = 30
            self.force = 20
            self.decay = 100
            self.bullet_size = 6
    class pistol:
        def __init__(self):
            self.speed = 20
            self.force = 10
            self.decay = 70
            self.bullet_size = 4
    class rifle:
        def __init__(self):
            self.speed = 60
            self.force = 25
            self.decay = 200
            self.bullet_size = 2

class Item:
    class health_small:
        hp = 10
    class health_med:
        hp = 25
    class health_big:
        hp = 50

blue = (0,0,139)
black = (0,0,0)