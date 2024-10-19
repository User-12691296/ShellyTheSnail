import time

class Animation:
    def __init__(self, max_frames, callback=None):
        self.frame = 0
        self.max_frames = max_frames

        self.callback = callback

    def isComplete(self):
        return self.frame > self.max_frames

    def changeFrame(self, df):
        self.frame += df

    def getFrame(self):
        return self.frame

    def getPercentage(self):
        return self.frame/self.max_frames

    def getDelta(self):
        return 1/self.max_frames

    def kill(self):
        if self.callback: self.callback()

    def tick(self):
        self.changeFrame(1)

        if self.isComplete() and self.callback:
            self.callback()

class Animated:
    def __init__(self):
        self.animations = {}

    def create(self, name, max_frames, callback=None):
        self.animations[name] = Animation(max_frames, callback)

    def exists(self, name):
        return bool(self.animations.get(name, False))

    def clear(self):
        for animation in self.animations.values():
            animation.kill()
        self.animations = {}

    def tick(self):
        for name, animation in (*self.animations.items(),):
            animation.tick()
            
            if animation.isComplete():
                del self.animations[name]

    def get(self, name):
        return self.animations.get(name)

    def getFrame(self, name):
        anim = self.get(name)
        
        if anim:
            return anim.getFrame()
        
        return 0

    def getPercentage(self, name):
        anim = self.get(name)

        if anim:
            return anim.getPercentage()

        return 0

    def getDelta(self, name):
        anim = self.get(name)
        
        if anim:
            return anim.getDelta()
        
        return 0

    def isComplete(self, name):
        return self.get(name).isComplete()
