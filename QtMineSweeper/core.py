class MineSweeperStatus(object):
    '''
    MineSweeper game status
    '''
    READY_TO_START = 0
    GAME_IN_PROGRESS = 1
    GAME_OVER_DEFEAT = 2
    GAME_OVER_VICTORY = 3


class FieldIndexStates(object):
    '''
    all description of field indexes
    '''
    class STATE(int):
        pass

    CLOSED = STATE(False)
    OPENED = STATE(True)

    class CONTENT(str):
        '''
        content of the index
        '''
        pass

    EMPTY = CONTENT('empty')
    BOMB = CONTENT('bomb')

    class MARK(str):
        '''
        for display a closed index
        '''
        pass

    BASIC = MARK('basic')
    FLAG = MARK('flag')
    NUMBER = MARK('number')
    INTERROGATION = MARK('interrogation')


class FieldSize(object):
    '''
    class represent the size of the board
    '''

    def __init__(self, height=10, width=10):
        self._height = height
        self._width = width

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width
