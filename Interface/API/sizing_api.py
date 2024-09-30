"""
@author: marc-antoine goulet, 2022
"""
import os

import requests
from datetime import datetime, timedelta
from .crypt_key import get_secret_id_key


class API_Connection:
    def __init__(self, client='pathogen_api', side="local", grant_type="client_credentials", username=None, password=None):
        """
        Initialize the data from the Sanuvox API
        :param db: the database object
        :param db_conn: the database class object
        :param client: which client to use
        """
        self.username = username
        self.password = password
        self.grant_type = grant_type

        api_key = get_secret_id_key(client=client)

        self.token_data = {
            'grant_type':    grant_type,
            'client_id':     api_key['client_id'],
            'client_secret': api_key['client_secret'],
        }
        if grant_type == "password":
            self.token_data["username"] = username
            self.token_data["password"] = password

        if side == "staging":
            self.api_url = 'https://staging.sanuvox.com'
        elif side == "local":
            self.api_url = 'http://web:8000' # used with local external network
        else:
            self.api_url = 'http://127.0.0.1:8000' # used with local external network

        self.get_token()
    
    def get_token(self):
        """
        Refresh the authentification token
        :return: None
        """
        self.created = datetime.now()
        if "refresh_token" not in self.token_data:
            req = requests.post(self.api_url+'/oauth2/token/', data=self.token_data).json()
            self.token_data['scope'] = req['scope']
            if "refresh_token" in self.token_data:
                self.token_data['refresh_token'] = req['refresh_token']
            self.expires = self.created + timedelta(seconds=req['expires_in'])
            self.headers = {
                'Authorization': '{} {}'.format(req['token_type'], req['access_token']),
                'content_type': 'json/application',
            }
        else:
            pass
    
    def token_has_expire(self):
        """
        Check if the token has expired
        :param req_json: the json from te API get request
        :return: Boolean
        """
        return not((self.expires - datetime.now()) > timedelta(seconds=1))
    
    def request(self, path, data=None, mode='get'):
        """
        Make a request to the API
        :param path: the path of the url of the API
        :param data: the data to send to the API
        :param mode: the mode of the request
        :return: the json map from the API response
        """
        url = self.api_url + self.root + path
        
        if self.token_has_expire():
            self.get_token()
        if mode == 'get':
            response = requests.get(url, json=data, headers=self.headers)
        elif mode == 'post':
            response = requests.post(url, json=data, headers=self.headers)
        elif mode == 'put':
            response = requests.put(url, json=data, headers=self.headers)
        elif mode == 'patch':
            response = requests.patch(url, json=data, headers=self.headers)
        elif mode == 'delete':
            response = requests.delete(url, json=data, headers=self.headers)
        
        try:
            response = response.json()
        except:
            pass

        return response

class Sizing_API(API_Connection):
    def __init__(self, side="local", username=None, password=None):
        """
        Initialize the API connection to the Sizing Pathogen API
        :param client: which client to use
        """
        self.root = "/sizing/"
        client = "sizing_ressource_api"
        super().__init__(
            client=client, grant_type="password",
            side=side, username=username, password=password
        )

    def convert_unit(self, data):
        return self.request(
            "unit/convert/", mode="post", data=data)

    def get_odor_list(self, cas_rn=None):
        data = None
        if cas_rn:
            data = {'cas_rn': cas_rn}
        return self.request(
            "odor/", data=data)
        
    def get_molecule(self, name=None, sequence=None, cas_rn=None):
        data = {}
        if name:
            data["name"] = name
        elif sequence:
            data["sequence"] = sequence
        elif cas_rn:
            data["cas_rn"] = cas_rn
        return self.request(
            "odor/molecule/", mode="post", data=data)
    
    def post_odor_wall(self, data=None):
        return self.request(
            "odorwall/", data=data, mode='post')
    
    def post_coil_clean(self, data=None):
        return self.request(
            "coilclean/", data=data, mode='post')


USERNAME = "user@sanuvox.com"
PASSWORD = "password"
if __name__ == "__main__":
    api = Sizing_API(side="local", username=USERNAME, password=PASSWORD)
    # resp = api.convert_unit(data={"input": "12000 CFM", "to_unit": "CMH"})
    resp = api.get_molecule(sequence="H2S").json()
    print(f"resp: {resp}")
    if resp["molecule"]["sizeable"]:
        resp = api.post_odor_wall(data={
            "cas_rn": resp["molecule"]["cas_rn"],
            "air_flow": "25000 cfm",
            "height": "62 inch",
            "width": "93.5 inch",
            "odor_concentration": "13 ppm",
            "air_temperature": "20 degC",
            "humidity": 40,
        })
    else:
        print("This molecule is not sizeable")
    try:
        print(f"resp: {resp.json()}")
    except:
        print(f"resp: {resp}")
