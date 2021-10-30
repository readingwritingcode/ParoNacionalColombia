#!pip install spacyTextblob >/dev/null

from spacytextblob.spacytextblob import SpacyTextBlob

import spacy

from spacy import displacy

nlp = spacy.load("es_core_news_sm")

import pandas as pd
from pathlib import Path

import os

# read dir data
for _, _dirs, _files in os.walk('./data'):
    
    for f in _files:
        
        vf = f.split('.')[0]
        
        print(vf)
        
# make dir inside imgs with mane author
        try:
            os.mkdir('./data/imgs/%s' % vf)
        except FileExistsError:
            pass
        
# create data frames for authors
        df = pd.read_csv("./data/%s" % f)

# proccess tweets in dataframe
        for i in df.index:
    
            print(df.loc[i,'text'])
    
            doc = nlp(df.loc[i,'text'])

# Generate sintax dependency tree
            svg = displacy.render(doc,style='dep',jupyter=False)
    
            print('./data/imgs/%s%d.svg' % (vf,i))
    
            output_path = Path('./data/imgs/%s/%s%d.svg' % (vf,vf,i))
    
            output_path.open("w", encoding="utf-8").write(svg)
    
    print(i)
