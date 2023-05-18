class AlreadyDoneError(Exception):
    def __init__(self, msg="You already perform that action", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
    pass

class GameStartedError(Exception):
    def __init__(self, msg="The game have already started", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
    pass

class NoGameError(Exception):
    def __init__(self, msg="There is no current game instance", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
    pass