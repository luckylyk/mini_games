
NAME = 'python2'


KEYWORDS = [
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
    'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global',
    'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
    'raise', 'return', 'try', 'while', 'with', 'yield']


BUILTIN = [
    'abs', 'divmod', 'input', 'open', 'staticmethod', 'all', 'enumerate',
    'int', 'ord', 'str', 'any', 'eval', 'isinstance', 'pow', 'sum',
    'basestring', 'execfile', 'issubclass', 'print', 'super', 'bin', 'file',
    'iter', 'property', 'tuple', 'bool', 'filter', 'len', 'range', 'type',
    'bytearray', 'float', 'list', 'raw_input', 'unichr', 'callable', 'format',
    'locals', 'reduce', 'unicode', 'chr', 'frozenset', 'long', 'reload',
    'vars', 'classmethod', 'getattr', 'map', 'repr', 'xrange', 'cmp',
    'globals', 'max', 'reversed', 'zip', 'compile', 'hasattr', 'memoryview',
    'round', '__import__', 'complex', 'hash', 'min', 'set', 'delattr', 'help',
    'next', 'setattr', 'dict', 'hex', 'object', 'slice', 'dir', 'id', 'oct'
    'sorted']


OPERATORS = [
    '=',
    '==', '!=', '<', '<=', '>', '>=',
    r'\+', r'-', r'\*', r'/', r'//', r'\%', r'\*\*',
    r'\+=', r'-=', r'\*=', r'/=', r'\%=',
    r'\^', r'\|', r'\&', r'\~', r'>>', r'<<']


BRAKETS = [
    r'\{', r'\}', r'\(', r'\)', r'\[', r'\]', r'\n']


STYLES = {
    'string2': {
        'color': 'red',
        'italic': True},

    'string': {
        'color': 'green',
        'italic': True},

    'self': {
        'color': 'yellow',
        'bold': True},

    'defclass':{
        'color': 'orrange',
        'bold': True},

    'comment': {
        'color': 'white'},

    'numbers': {
        'color': 'brown'},

    'keyword': {
        'color': 'BurlyWood',
        'bold': True},

    'operator': {
        'color': 'DarkTurquoise'},

    'brace': {
        'color': 'BurlyWood',
        'bold': True}}

# Multi-line strings (expression, flag, style)
# FIXME: The triple-quotes in these two lines will mess up the
# syntax highlighting from this point onward
RULES = ([
    ("'''", 1, STYLES['string2']),
    ('"""', 2, STYLES['string2']),
    (r'\bself\b', 0, STYLES['self']),
    (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
    (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
    (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
    (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
    (r'#[^\n]*', 0, STYLES['comment']),
    (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
    (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
    (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers'])] + 
    [(r'\b{}\b'.format(kw), 0, STYLES['keyword']) for kw in KEYWORDS] +
    [(r'{}'.format(op), 0, STYLES['operator']) for op in OPERATORS] +
    [(r'{}'.format(br), 0, STYLES['brace']) for br in BRAKETS])
