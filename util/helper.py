import random


def random_char(start, end):
    return chr(random.randint(start, end))

def random_string(len):
    code_str = ''
    for _ in range(len):
        flag = random.randint(0, 2)
        start, end = (ord('a'), ord('z')) if flag == 1 else (ord('A'), ord('Z')) if flag == 2 else (ord('0'), ord('9'))
        code_str += random_char(start, end)
    return code_str