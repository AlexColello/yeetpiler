import math
    
class WordGenorator():

    def __init__(self, pattern, prefix='', suffix='', starting_pattern=1):
        self.prefix = prefix
        self.pattern = pattern
        self.suffix = suffix
        self.starting_pattern = starting_pattern
        self.count = 0

    def next(self):
        output = self.make_word(self.count)
        self.count += 1
        return output

    def make_word(self, num):

        num += 2**len(self.prefix + self.pattern*self.starting_pattern + self.suffix) # Makes the number of capitalized letters at least 4, the length of the yeet
        capitalized_letters = int(math.log(num, 2))

        num_pattern = max(self.starting_pattern, int((capitalized_letters - len(self.suffix + self.prefix))/len(self.pattern)))
        base = self.prefix + self.pattern * num_pattern + self.suffix

        output = ''
        for i in range(capitalized_letters):

            capitalized = not ((num >> i) & 1)
            output += chr(ord(base[i]) + capitalized * 32)

        output += base[len(output):].lower()
        return output

class YeetGenerator(WordGenorator):

    def __init__(self):
        super().__init__('E', 'Y', 'T', 2)


class DabGenerator(WordGenorator):
    
    def __init__(self):
        super().__init__('A', 'D', 'B')

class TrolololGenerator(WordGenorator):

    def __init__(self):
        super().__init__('OL', prefix='TR', starting_pattern=3)




