import requests
import json

class RestApiComms():

    def post(self, url, data, bearer_token=None):

        headers = self.build_headers(bearer_token)
        print("Posting to URL:: "+str(url))
        print("W headers:: "+str(headers))
        response = requests.post(url, json.dumps(data), headers=headers)
        print("REST API response:: "+str(response.content))
        response = response.json()
        if 'status_code' in response and response['status_code']>=400:
            print("REST API error:: "+str(response))
            return None

        return response
    
    def put(self, url, data, bearer_token=None):
        headers = self.build_headers(bearer_token)
        response = requests.put(url, json.dumps(data), headers=headers)
        #print("REST API response:: "+str(response.content))
        response = response.json()
        if 'status_code' in response and response['status_code']>=400:
            print("REST API error:: "+str(response))
            return None

        return response
    
    def get(self, url, query_params_map, bearer_token=None, api_dev_key=None):

        query_params = []
        if query_params_map:
            for param_key in query_params_map.keys():
                query_params.append(str(param_key)+"="+str(query_params_map[param_key]))

        query_params_str = ""
        if len(query_params)>0:
            query_params_str = "?"+"&".join(query_params)
        
        headers = self.build_headers(bearer_token, api_dev_key)

        print("Invoking url:: "+str(url))
        print("W Query string:: "+str(query_params))
        print("And headers:: "+str(headers))
        response = requests.get(url+query_params_str, headers=headers)
        
        response = response.json()

        return response
    
    def build_headers(self, bearer_token=None, api_dev_key=None):
        headers = {'Content-type': 'application/json'}
        if bearer_token:
            headers['Authorization']='Bearer '+bearer_token
        if api_dev_key:
            headers['api_dev_key']=api_dev_key

        return headers
