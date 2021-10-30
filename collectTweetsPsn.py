from tools import *

lp =[
    'AlvaroUribeVel',
    'petrogustavo',
    'GustavoBolivar',
    'IvanDuque',
    'MariaFdaCabal',
    'PaolaHolguin',
    'PalomaValenciaL',
    'Margaritarosadf',
    'JulianRoman',
    'juanpisrules',
    'VickyDavilaH',
    'lcvelez',
    'AdrianaLucia',
    'Santialarconu',
    'HOLLMANMORRIS',
    'tobonsanin',
    'QuinteroCalle',
    'JorgeIvanOspina',
    'joaltejada',
    'JuanManSantos',
    'JERobledo',
    'ClaudiaLopez',
    'diegomolanovega',
    'matador',
    'polo_polo',
    'saludhernandezm',
    'LevyRincon',
    'sergio_fajardo',
    'piedadcordoba',
    'fdbedout',
    'IvanCepedaCast',
    'PizarroMariaJo',
    'intiasprilla',
    'DanielSamperO',
    'wilsonariasc',
    'mluciaramirez',
    'RoyBarreras',
    'DanielPalam',
    'velezfutbol'
    ]

for i in lp:
    time.sleep(3)
    print('from:%s (vandalos OR vándalos OR VANDALISMO OR VANDALIZAR OR vandalico OR vandálico) -is:retweet' % i)
    collect_tweets('from:%s (vandalos OR vándalos OR VANDALISMO OR VANDALIZAR OR vandalico OR vandálico) -is:retweet' % i,
            start_time='2021-04-28T23:58:00.00Z',
            end_time='2021-05-28T23:58:00.00Z',
            tweet_fields='author_id,created_at,public_metrics',name_file=i)
    
    
# Generate all_df with all csv
all_df = pd.DataFrame()
for _root,_dirs,_files in os.walk(os.path.abspath('./data/')):
    for _file in _files:
        if _file.endswith('.csv'):
            #read
            df = pd.read_csv(os.path.abspath('./data')+'/'+_file)
            #clean
            df=df[[x for x in df.columns if x != 'Unnamed: 0']]
            #add_column
            df['author_name'] = _file.split('.')[0]
            #avoid int to float
            try:
                df['id'] = df['id'].astype(int).astype(str)
                df['author_id'] = df['author_id'].astype(int).astype(str)
            except KeyError:
                pass
            #generate all df
            all_df=pd.concat([all_df,df])
            
# Get replies for a tweets in all_df
allrep = []
for i in all_df.index:
    print(all_df.loc[i,'id'])
    time.sleep(1.2)
    r = collect_tweets('conversation_id:%s' % all_df.loc[i,'id'],start_time=all_df.loc[i,'created_at'],repls=True)
    trep = []
    for rep in r:
        #print(rep['text'])
        trep.append(rep['text'])
    allrep.append(trep)
all_df['reps'] = allrep

# store 
all_df.to_csv('tweets_personajes_with_replies_28_04_2021_28_04_2021.csv')
