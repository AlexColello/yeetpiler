
class YeetGenerator():

    def __init__(self):
        self.count = 2

    def next(self):
        output = ""
        output += "y"
        count = self.count
        for i in range(self.count):
            output += "e"
        output += "t"
        self.count += 1
        return output

            
