class creature(object):
    def c(self):
        data_set = {
            'type': 'Non-Humanoid',
            '$type': lambda x: data_set.update({'type': x}),
            'breed': 'Unkown',
            '$breed': lambda x: data_set.update({'breed': x}),
            'color': 'White',
            '$color': lambda x: data_set.update({'color': x}),
            'name': 'Bob',
            '$name': lambda x: data_set.update({'name': x}),
        }

        def ret_item(self, item):
            if item in data_set:
                return data_set[item]
            else:
                return None
        return ret_item
    run1 = c(1)

class human(creature):
    def m(self):
        data_set = {
            'name': 'Juan',
            '$name': lambda x: data_set.update({'name': x}),
            'type': 'Human',
            '$type': lambda x: data_set.update({'type': x}),
            'race': 'Latino',
            '$race': lambda x: data_set.update({'race': x}),
        }
        def h(self, item2):
            if item2 in data_set:
                return data_set[item2]
            else:
                return super(human, self).run1(item2)
        return h
    run2 = m(1)

def create_creature():
    ob1 = human()
    print('Printing details for a Human')
    print(ob1.run2('name'))
    print(ob1.run2('type'))
    print(ob1.run2('race'))


#(exec 'import Onlystring; toReturn = Onlystring.create_creature()')
