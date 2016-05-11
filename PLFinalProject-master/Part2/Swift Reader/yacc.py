import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = False

# Namespace & built-in functions

name = {}
let_dict = {}
var_dict = {}
global ast
ast = []

def cons(l):
    return [l[0]] + l[1]

name['cons'] = cons

def multi_func(l):
    if l[2] in let_dict:
        l[2] = let_dict[l[2]]
    if l[4] in let_dict:
        l[4] = let_dict[l[4]]
    if l[2] in var_dict:
            l[2] = var_dict[l[2]]
    if l[4] in var_dict:
        l[4] = var_dict[l[4]]
    if l[3] == '+':
        return [l[0],l[1],l[2]+l[4]]
    elif l[3] == '-':
        return [l[0],l[1],l[2]-l[4]]
    elif l[3] == '*':
        return [l[0],l[1],l[2]*l[4]]
    elif l[3] == '/':
        return [l[0],l[1],l[2]/l[4]]



def let(l):
    if length(l) <= 4:
        if l[1] == '=':
            if l[0] in let_dict:
                return l[0] + ' previously declared here'
            elif l[0] in let_dict and let_dict[l[0]] == None:
                let_dict[l[0]]=l[2]
            elif l[0] in var_dict:
                return l[0] + ' previously declared here'
            else:
                let_dict[l[0]]=l[2]
        elif l[1] == ':' and l[3] == '?':
            return optional_value(l,'let')
    elif length(l) > 4:
        l=multi_func(l)
        let(l)

name['let'] = let

def var(l):
    if length(l) <= 4:
        if l[1] == '=':
            if l[0] in var_dict:
                var_dict[l[0]]=l[2]
            elif l[0] in let_dict:
                return l[0] + ' previously declared here'
            else:
                var_dict[l[0]]=l[2]
        elif l[1] == ':' and l[3] == '?':
            return optional_value(l,'var')
    elif length(l) > 4:
        l=multi_func(l)
        var(l)

name['var'] = var

def optional_value(l,type):
    if l[2] == 'String?' | 'Int?' | 'double?' | 'float?':
        if type == 'var':
            var_dict[l[0]]= None
            var_dict[l[0]].type()==l[2]
        elif type == 'let':
            let_dict[l[0]]= None
            let_dict[l[0]].type()==l[2]
    return



def swiftprint(l):
    if length(l) == 1:
        if l[0] in var_dict:
            return var_dict[l[0]]
        elif l[0] in let_dict:
            return let_dict[l[0]]
        else:
            return l[0]
    else:
        _print(l)

name['print'] = swiftprint


def length(l):
    l_count=0
    for i in l:
        l_count+=1
    return l_count

def concat(l):
    return l[0] + l[1]

name['concat'] = concat

def listar(l):
    return l

name['list'] = listar

def car(l):
    return l[0][0]

name['car'] = car

def cdr(l):
    return l[0][1:]

name['cdr'] = cdr

def eq(l):
    return l[0] == l[1]

name['eq'] = eq
name['='] = eq

def _and(l):
    return not False in l

name['and'] = _and

def _or(l):
    return True in l

name['or'] = _or

def cond(l):
    if l[0]:
        return l[1]

name['cond'] = cond

def add(l):
    return sum(l)

name['+'] = add

def minus(l):
    '''Unary minus'''
    return -l[0]

name['-'] = minus

def _print(l):
    print lisp_str(l[0])

name['_print'] = _print

#  Evaluation functions

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
        return [simb] + items

def call(f, l):
    try:
        return f(eval_lists(l))
    except TypeError:
        return f

def eval_lists(l):
    r = []
    for i in l:
        if is_list(i):
            if i:
                r.append(lisp_eval(i[0], i[1:]))
            else:
                r.append(i)
        else:
            r.append(i)
    return r

# Utilities functions

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "#t"
    elif l is False:
        return "#f"
    elif l is None:
        return 'nil'
    else:
        return str(l)

# BNF

def p_exp_atom(p):
    'exp : atom'
    p[0] = p[1]

def p_exp_qlist(p):
    'exp : quoted_list'
    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_quoted_list(p):
    'quoted_list : QUOTE list'
    #p[0] = p[2]
    p[0] = ["quote"] + [p[2]]

def p_list(p):
    'list : LPAREN items RPAREN'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    p[0] = p[1]

def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

def p_call(p):
    'call : LPAREN SIMB items RPAREN'
    if DEBUG: print "Calling", p[2], "with", p[3]
    p[0] = lisp_eval(p[2], p[3])


def p_atom_simbol(p):
    'atom : SIMB'
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_empty(p):
    'atom :'
    pass

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_nil(p):
    'atom : NIL'
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


