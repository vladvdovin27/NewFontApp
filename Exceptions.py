class Wrong(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WrongContent(Wrong):
    def __init__(self, message):
        super().__init__(message)


class WrongPathContent(Wrong):
    def __init__(self, message):
        super().__init__(message)
