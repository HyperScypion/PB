import string
import random


class Salt:
    def __init__(self, size: int) -> None:
        self.size = size
        self.result = ""

    def generate(self) -> str:
        for i in range(self.size):
            self.result += random.choice(string.ascii_letters)
        return self.result

