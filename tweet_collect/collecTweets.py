import time

import tools

medios = [  'NoticiasRCN',
            'NoticiasCaracol',
            'NoticiasUno',
            'BluRadioCo',
            'lafm',
            'WRadioColombia',
            'RevistaSemana',
            'elespectador',
            'Teleantioquia',
            'CanalCapital',
            'TelepacificoTV',
            'elcolombiano',
            'Telemedellin',
            'elpaiscali'
        ]

for m in medios:

    query = 'from:%s' % m 

    time.sleep(1.5)

    tools.collect_tweets(query,
                         end_time='2021-05-28T23:59:00.00Z',
                         start_time='2021-05-28T23:50:00.00Z',
                         tweet_fields='created_at',name_file=query)