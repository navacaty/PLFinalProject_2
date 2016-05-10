def Onlystring(values):
    def is_string(value):
        try:
            return value == str(value)
        except:
            return False
    def make_sent(value):
        return value + "is a string item"
    for item in values:
        if is_string(item):
            print(make_sent(item))
