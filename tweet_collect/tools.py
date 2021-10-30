# %load collector.py
#!/usr/bin/python3
import re
import os
import json
import time
import pandas as pd
import requests

from pysentimiento import SentimentAnalyzer
# Auth app
bearer_token='AAAAAAAAAAAAAAAAAAAAAGP%2FQAEAAAAAMsVOXfioKuGkju6iyWBDLMf3Ojs%3DFP7whmTYYWIJznLYT3eA79iGlg23xbE8b9olJx6gzXOgZrzKCs'


# EndPoint
api_end_point = "https://api.twitter.com/2/tweets/search/all"

def create_headers(bearer_token):
    '''headers for auth application'''
    return {"Authorization":"Bearer {}".format(bearer_token)}

# Query params Headers
def build_query_params(query,start_time=None,end_time=None,tweet_fields=None,max_results=None,next_token=None):
    '''
    PUBLIC PARAMS:
        query: query string
        start_time
        end_time
        tweet_fields
        max_results
    PRIVATE PARAMS:
        next_token
    '''
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

# end point connection
def connect_to_end_point(api_end_point,headers,params):
    
    # handling internet connection; see: https://stackoverflow.com/questions/21407147/python-requests-exception-type-connectionerror-try-except-does-not-work
    var_cont = True

    while var_cont:
        
        try:
            response = requests.request("GET",api_end_point, headers=headers, params=params)
            var_cont = False
        except requests.exceptions.ConnectionError as e:
            print('internet connection fail wait for a moment')
            time.sleep(60)
            
    print(response.status_code)

    if response.status_code != 200 and response.status_code != 503:
        raise Exception(response.status_code,response.text)
    
    # handling rate-limit-handling; see: https://developer.twitter.com/en/docs/twitter-api/rate-limits
    rtl = int(response.headers['x-rate-limit-remaining'])

    if rtl <= 5:
        print('waiting for a moment for avoid rate-limit request')
        time.sleep(15*60)

    # handling servers are up with many work
    if response.status_code == 503:   # the Twitter servers are up, but overloaded with requests. 
        time.sleep(3*60)             # Try again later.
        print('sleeping for a moment')

        # handling internet connection II
        var_cont = True
    
        while var_cont:
            try:
                response = requests.request("GET",api_end_point, headers=headers, params=params)
                var_cont = False
            except requests.exceptions.ConnectionError as e:
                print('internet connection failm wait for a moment')
                time.sleep(60)

        return response.json()
    
    return response.json()

def make_query(query,start_time=None,end_time=None,tweet_fields=None,max_results=None,next_token=None):
    
    '''Basic query without pagination.'''
    
    # Retrieve a basic amount of tweets (max_results between 10 or 500)
    query_params = build_query_params(query,start_time,end_time,tweet_fields,max_results,next_token)
    headers = create_headers(bearer_token)
    json_response = connect_to_end_point(api_end_point, headers, query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    #print(json_response)
    return json_response

def collect_tweets(query,start_time=None,end_time=None,tweet_fields=None,name_file=None,repls = None):
    '''Query with pagination'''

    # store results in list of json
    results_query = []

    # firts query results tweets
    r = make_query(query,
             start_time,
             end_time,
             tweet_fields=tweet_fields,
             max_results=500)

    # handle pagination for retrieve all results
    var_cont = True
    
    try:
        if r['data']:
            # store data
            results_query.extend(r['data'])

            while var_cont:
                time.sleep(1.2)
                try:
                    if r['meta']['next_token']:
                        next_token = r['meta']['next_token'] # private param
                        r = make_query(query,
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
        print('no results for thist query %s' % query)

    print(len(results_query))
    
    if not repls:
    # make directory for store data
        path = "./data/"
        if os.path.exists("./data/"):
            pass
        else:
            os.makedirs(path)

        # make data frame 
        df = pd.DataFrame(results_query)

        print(df.shape)

        df.to_csv(path + name_file +'.csv')
    else:
        return results_query

    return 'ok'    
