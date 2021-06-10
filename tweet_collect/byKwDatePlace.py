#!/usr/bin/python3

import os
import json
import time
import pandas as pd
import requests

# Auth app
bearer_token=''

# EndPoint
search_url = "https://api.twitter.com/2/tweets/search/all"

# Headers for auth
def create_headers(bearer_token):
    
    headers = {"Authorization":"Bearer {}".format(bearer_token)}
    
    return headers

# Build query
def make_query(query,start_time=None,end_time=None,tweet_fields=None,max_results=None,next_token=None):

    query_params = {'query':query}

    if start_time is not None:

        query_params['start_time'] = start_time
    
    if end_time is not None:
        
        query_params['end_time'] = end_time
    
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
    
    if response.status_code != 200 and response.status_code != 503:
    
        raise Exception(response.status_code,response.text)

    if response.status_code == 503:   # the Twitter servers are up, but overloaded with requests. 

        time.sleep(3*60)             # Try again later.

        print('sleeping for a moment')

        response = requests.request("GET",search_url, headers=headers, params=params)

        return response.json()
    
    return response.json()

# Main
def main(query,start_time=None,end_time=None,tweet_fields=None,max_results=None,next_token=None):
    
    query_params = make_query(query,start_time,end_time,tweet_fields,max_results,next_token)
    
    headers = create_headers(bearer_token)
    
    json_response = connect_to_endpoint(search_url, headers, query_params)
    
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    print(json_response)

    # return json.dumps(json_response, indent=4, sort_keys=True)
    return json_response

def collect_tweets(query,start_time=None,end_time=None,tweet_fields=None):
    '''collect tweets by query and params between start_date and end date'''

    # data y meta
    results_query = []

    # firts query results
    r = main(query,
             start_time,
             end_time,
             tweet_fields=tweet_fields,
             max_results=500)

    # compare if data is not empty
    var_cont = True
    
    try:

        if r['data']:

            # store data
            results_query.extend(r['data'])
            
            while var_cont:
                
                time.sleep(1.2)

                try:
                    
                    if r['meta']['next_token']:

                        next_token = r['meta']['next_token'] # private
                        
                        r = main(query,
                                start_time=start_time,
                                end_time=end_time,
                                tweet_fields=tweet_fields,
                                max_results=500,
                                next_token=next_token)

                        print(r)

                        results_query.extend(r['data'])

                except KeyError:

                    var_cont=False

    except KeyError:

        print('no results')

    print(len(results_query))

    df = pd.DataFrame(results_query)

    print(df.shape)

    df.to_csv('tweets_Revista_semana_28_05_k.csv')

    return 'ok'

#print(len(results_query))

#<<<<<<< HEAD
collect_tweets('(vandalos OR vándalos) OR (VANDALISMO OR VANDALIZAR) -is:retweet place_country:CO''(vandalos OR vándalos) OR (VANDALISMO OR VANDALIZAR) -is:retweet place_country:CO',
                end_time='2021-05-28T23:59:00.00Z',
                start_time='2021-05-28T00:00:00.00Z',
                tweet_fields='created_at')
#=======

