
class LLM_JsonDecodeError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.code = 0x0001