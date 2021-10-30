from tools import *

collect_tweets('place_country:CO (vandalos OR vándalos) OR (VANDALISMO OR VANDALIZAR) -is:retweet',
               start_time='2021-04-28T00:00:00.00Z',
               end_time='2021-05-28T23:59:00.00Z',        
               tweet_fields='author_id,created_at,public_metrics',name_file='name_file_here')
