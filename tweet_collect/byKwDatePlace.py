#
import requests
import os
import json

bearer_token='<bearer_token_heare>'

def create_headers(bearer_token):
    
    headers = {"Authorization":"Bearer {}".format(bearer_token)}
    
    return headers

search_url = "https://api.twitter.com/2/tweets/search/all"


def make_query(query,end_time=None,start_time=None,tweet_fields=None, max_results=None,next_token=None):

    query_params = {'query':query}
    
    if end_time is not None:
        
        query_params['end_time'] = end_time

    if start_time is not None:

        query_params['start_time'] = start_time
    
    if tweet_fields is not None:

        query_params['tweet.fields'] = tweet_fields 

    if max_results is not None:

        query_params['max_results'] = max_results
    
    if next_token is not None:

        query_params['next_token'] = next_token

    return query_params


def connect_to_endpoint(search_url,headers,params):

    response = requests.request("GET",search_url, headers=headers, params=params)
    
    print(response.status_code)
    
    if response.status_code != 200:
    
        raise Exception(response.status_code,response.text)
    
    return response.json()


def main(query,end_time=None,start_time=None,tweet_fields=None,max_results=None,next_token=None):
    
    query_params = make_query(query,start_time,end_time,tweet_fields,max_results,next_token)
    
    headers = create_headers(bearer_token)
    
    json_response = connect_to_endpoint(search_url, headers, query_params)
    
    print(json.dumps(json_response, indent=4, sort_keys=True))
    
    return json.dumps(json_response, indent=4, sort_keys=True)

  
#### example of use
# data y meta
results_query = []

# firts query results
r = json.loads(main('(vandalos vándalos) OR (VANDALISMO VANDALIZAR) -is:retweet place_country:CO',
              end_time='2021-04-28T23:59:00.00Z',
              start_time='2020-04-28T00:00:00.00Z',
              tweet_fields='created_at',
              max_results=500))

# compare if data is not empty
var_cont = True

if r['data']:

    # store data
    results_query.extend(r['data'])
    
    while var_cont:
        
        time.sleep(1.2)
        
        if r['meta']['next_token']:
            
            r = json.loads(main('(vandalos vándalos) OR (VANDALISMO VANDALIZAR) -is:retweet place_country:CO',
              end_time='2021-04-28T23:59:00.00Z',
              start_time='2020-04-28T00:00:00.00Z',
              tweet_fields='created_at',
              max_results=500,
              next_token=r['meta']['next_token']))
            
            if r['data']:
                # store data
                for i in r['data']:
                    
                    if i['created_at'].split('-')[-1][:2] >= '28':
                        # enhance this logic
                        
                        results_query+=[i]
                        
                    else:
                        # out of date
                        
                        print('out of date')
                        
                        var_cont = False

        else:
            # no more results
            print('no more results')
            break
print(len(results_query))
