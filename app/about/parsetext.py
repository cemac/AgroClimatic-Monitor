from flask import Markup
def f(text):
    return Markup(text.lstrip().replace('\n\n','<br><br>'))
    
def about(module):
    '''
    A function to get all the textboxes
    '''
    keys = list(vars(module).keys())
    vals = list(vars(module).values())
    
    rt = {}
    for i,key in enumerate(keys):
        if '_' in key and '_title' in key:
            #print(key,vals[i],vals[i+1])
            rt[vals[i]] = f(vals[i+1])
            
    return rt