
from serverscripts.config import *
import pandas as pd
from serverscripts.get_individual import m_new


df = pd.read_csv(PROCESSED+'geojson/search.csv')
for key in df.iterrows():
    code = str(key[1].val)
    m_new(code)
    break
