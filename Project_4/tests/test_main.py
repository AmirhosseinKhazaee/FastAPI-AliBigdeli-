from .conftest import client
from fastapi import status

def test_public():
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "this is public endpoint"}
    
    
def test_user_auth_register():
    payload = {
        "username" : "amir",
        "email" : "amirh@gmail.com",
        "password" : "12321"
    }
    response = client.post("/auth/register" , json=payload)
    assert response.status_code == status.HTTP_200_OK
        
def test_user_auth():
    payload = {
        "email" : "amirh@gmail.com",
        "password" : "12321"
    }
    response = client.post("/auth/login" , json=payload)
    assert response.status_code == status.HTTP_200_OK
    