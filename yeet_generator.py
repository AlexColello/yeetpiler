import math

def make_yeet(num):

    output = ""

    if num == 0:
        iterations = 4
    else:
        iterations = max(4, int(math.log(num, 2)) + 1)

    # print('{} {}'.format(num, iterations))

    for i in range(iterations):
        if i == 0:
            base = 'Y'
        elif i == iterations - 1:
            base = 'T'
        else:
            base = 'E'

        capitalized = not ((num >> i) & 1)

        output += chr(ord(base) + capitalized * 32)
    return output


# for i in range(65):
#     print('{} {}'.format(make_yeet(i), i))


class YeetGenerator():

    def __init__(self):
        self.count = 0

    def next(self):
        output = make_yeet(self.count)
        self.count += 1
        return output

            
