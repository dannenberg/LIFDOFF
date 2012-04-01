class Animation:
    def __init__(self, state, **args):
        if state not in args:
            raise ValueError("State given ("+str(state)+") was not defined.")
        self.state = state
        self.frame = 0
        self.timer = 0
        for x in args:
            self.__dict__[x] = args[x]  # idle = [(1,50,(0,0)), (0,50,(1,0))]
    
    def advance_sprite(ms):
        self.timer += ms
        while self.timer > self.__dict__[self.state][self.frame][1]:
            self.timer -= self.__dict__[self.state][self.frame][1]
            self.frame = self.__dict__[self.state][self.frame][0]
        return self.__dict__[self.state][self.frame][2]
