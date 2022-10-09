from random import randint


def randomString(n=10) -> str:
    return "".join([str(randint(0, 9)) for i in range(n)])
