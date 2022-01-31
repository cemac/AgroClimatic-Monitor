
from serverscripts.config import *
import pandas as pd
from serverscripts.get_individual_batch import m_new


codelist = pd.read_csv(PROCESSED+'geojson/search.csv')
for key in codelist.iterrows():
    code = str(key[1].val)
    try:
        m_new(code)
    except:
        continue
