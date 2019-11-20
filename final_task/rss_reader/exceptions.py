class TimeOutExeption(Exception):
    def __init__(self, msg):
        super().__init__('Problems with internet connection: ' + str(msg))
