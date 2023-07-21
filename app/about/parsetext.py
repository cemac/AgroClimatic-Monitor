"""template file
.. module:: about
    :platform: Unix
    :synopsis: Flask app template text
.. moduleauthor: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This script contains text variables for pages.
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
from flask import Markup
import markdown

def f(text):
    return Markup(markdown.markdown(text.lstrip().replace('\n\n','<br><br>')))

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
