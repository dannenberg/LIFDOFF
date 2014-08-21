class Animation:
    def __init__(self, state, **args):
        if not args:
            args = {state:[(0, 9999999, (0, 0))]}
        if state not in args:
            raise ValueError("State given ("+str(state)+") was not defined.")
        self.state = state
        self.frame = 0
        self.timer = 0
        self.clips = args  # idle = [(1, 50, (0, 0)), (0, 50, (1, 0))]

    def advance_sprite(self, ms):
        self.timer += ms    # add the elapsed time to the timer
        while self.timer > self.clips[self.state][self.frame][1]:    # if the timer is greater than how long we should be on the current frame
            self.timer -= self.clips[self.state][self.frame][1]      # take the frame time from the timer
            self.frame = self.clips[self.state][self.frame][0]       # advance the frame
        return self.clips[self.state][self.frame][2]                 # return the current image position for our sprite

    def clone(self):
        return Animation(self.state, **self.clips)
