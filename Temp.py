class Temp(object):
    def __init__(self, pnumber, number):
        self.pnumber = pnumber
        self.code = number

    def serialize(self):
        return {
            'number': self.code
        }