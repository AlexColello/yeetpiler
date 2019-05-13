import math

def make_yeet(num):

    num += 16 # Makes the number of capitalized letters at least 4, the length of the yeet
    capitalized_letters = int(math.log(num, 2))

    num_e = max(2, capitalized_letters - 2)
    base = 'Y' + 'E' * num_e + 'T'

    output = ""
    for i in range(capitalized_letters):

        capitalized = not ((num >> i) & 1)
        output += chr(ord(base[i]) + capitalized * 32)

    output += base[len(output):].lower()
    return output


for i in range(65):
    print('{} {}'.format(make_yeet(i), i))


class YeetGenerator():

    def __init__(self):
        self.count = 0

    def next(self):
        output = make_yeet(self.count)
        self.count += 1
        return output

            
