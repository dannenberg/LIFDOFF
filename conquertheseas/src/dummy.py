class Dummy:
    def __getattr__(self, name):
        print "I am dummy."
        return lambda x:None
