from PyQt5 import QtGui


class Colors(dict):
    '''
    dict containing QColor().
    instance it at the module begining :: colors = Colors()
    To get an Hex color :: colors['#hexcode']
    To get an Rgb color :: colors['150, 225, 0']
    To get an Rgb color with alpha :: colors['150, 225, 0, 50]
    When you get a color
    if the color doesn't exist yet, Colors create and stock for you a
    QtGui.QColor()
    '''

    def __init__(self):
        super(Colors, self).__init__({})

    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            if ',' in name:
                try:
                    value = [int(elt) for elt in name.split(',')]
                except ValueError():
                    print(
                        "{} have to contain only number and ','".format(name))
                value = QtGui.QColor(*value)
            else:
                value = QtGui.QColor(name)
            dict.__setitem__(self, name, value)
            return dict.__getitem__(self, name)
