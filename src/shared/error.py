class NotImplementedError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Not yet implemented: {message}")
