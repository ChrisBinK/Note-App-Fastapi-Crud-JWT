import requests
import json
HOST = 'http://127.0.0.1:8000/'

user_data = {
        'id':0,
        'first_name': 'Christelle',
        'last_name': 'Kalanda',
        'gender': 'Female',
        'email': 'christelle@mynotes.com',
        'password': 'securepassword'
    }

phantomas_user = {
        'id':985,
        'first_name': 'Christelle',
        'last_name': 'Kalanda',
        'gender': 'Female',
        'email': 'christelle@mynotes.com',
        'password': 'securepassword'
    }
def test_create_new_user():
    '''This Function ensures that a user is created when the email is unique.'''
    url = HOST + 'api/users'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    response= requests.post(url, data = json.dumps(user_data), headers=headers)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["password"] != "securepassword"

def test_create_user_existing_user_email():
    #This function ensures that the user email is unique and prevents the creation of a new user with existing email
    url = HOST + 'api/users'
   
    response= requests.post(url, data = json.dumps(user_data))
    assert response.status_code == 406
    assert response.json()["detail"] == "User already exists."

def test_update_user_existing_user():
    '''This Function update an existing user.'''
    url = HOST + 'api/users'
    user_data['last_name'] = 'Marcello'
    response= requests.post(url, data = json.dumps(user_data))
    assert response.status_code == 200

def test_update_user_with_no_record():
    '''This function ensures if the user information provided is not stored, return an error. '''
    url = HOST + 'api/users'
    response= requests.post(url, data = json.dumps(phantomas_user))
    assert response.status_code == 404

def test_delete_user():
    url = HOST + 'api/users/2'
    response= requests.post(url)
    assert response.status_code == 200

def test_delete_non_existing_user():
    url = HOST + 'api/users/2985'
    response= requests.post(url)
    assert response.status_code == 404


