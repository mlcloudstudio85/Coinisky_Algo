import json
# import requests
from bs4 import BeautifulSoup as bs
from bs4 import Comment
from UseSupersetApi import UseSupersetApi

superUsername = 'coinisky'
superUserPassword = 'A_GHw$eSXq@QlT$J'

def lambda_handler(event, context):
    
    first_name = event['first_name']
    last_name = event['last_name']
    username = event['username']
    email = event['email']
    active = True
    password = event['password']
    conf_password = event['conf_password']
    
    try:
        superset = UseSupersetApi(superUsername, superUserPassword)
        payload = {'first_name': first_name,
               'last_name': last_name,
               'username': username,
               'email': email,
               'active': True,
               'password': password,
               'conf_password': conf_password,
               'roles':['4', '8', '9']
          }
        
        response = superset.post(url_path='users/add', json=payload)
        if response.status_code != 200:
            raise Exception("Error while creating user") 
        return {
            'statusCode': 200,
            'message': "Successfully created user"
        }
        
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'message': str(e)
        }
        
