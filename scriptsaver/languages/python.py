
NAME = 'python'


KEYWORDS = [
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
    'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global',
    'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
    'raise', 'return', 'try', 'while', 'with', 'yield']


BUILTINS = [
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
        'color': 'orange',
        'italic': True},

    'string': {
        'color': 'yellow',
        'italic': True},

    'self': {
        'color': 'blue',
        'bold': True},

    'defclass':{
        'color': 'CadetBlue',
        'bold': True},

    'comment': {
        'color': 'SeaGreen'},

    'numbers': {
        'color': 'Chocolate'},

    'keyword': {
        'color': 'DarkTurquoise',
        'bold': True},

    'operator': {
        'color': 'BurlyWood'},

    'brace': {
        'color': 'DarkTurquoise',
        'bold': True},

    'builtins': {
        'color': '#dccda5',
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
    [(r'{}'.format(br), 0, STYLES['brace']) for br in BRAKETS] +
    [(r'{}'.format(br), 0, STYLES['builtins']) for br in BUILTINS])
