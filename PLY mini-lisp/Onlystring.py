class creature(object):
    def c(self):
        data_set = {
            'type': 'Humanoid',
            '$type': lambda x: data_set.update({'type': x}),
            'breed': 'Unkown',
            '$breed': lambda x: data_set.update({'breed': x}),
            'color': 'White',
            '$color': lambda x: data_set.update({'color': x}),
            'name': None,
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
            'name': 'John',
            '$name': lambda x: data_set.update({'name': x}),
            'type': 'Human',
            '$type': lambda x: data_set.update({'type': x}),
            'breed': None,
            '$breed': lambda x: data_set.update({'breed': x}),
        }
        def h(self, item2):
            if item2 in data_set:
                return data_set[item2]
            else:
                return super(human, self).run(item2)
        return h
    run2 = m(1)

def create_person(name, type):
    if type == 'Human' | 'human':
        ob1 = human()
        print('Printing details for a Human')
        print(ob1.run2('$name')(name))
        print(ob1.run2('$type')(type))
    else:
        ob1 = creature()
        print('Printing details for a non-human creature')
        print(ob1.run1('$name')(name))
        print(ob1.run1('$type')(type))
        print(ob1.run1('breed'))
        print(ob1.run1('color'))


