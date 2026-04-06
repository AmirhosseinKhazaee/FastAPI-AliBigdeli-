
from fastapi import status

def test_public(annon_client):
    response = annon_client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "this is public endpoint"}
    
    
def test_user_auth_register(annon_client):
    payload = {
        "username" : "amir",
        "email" : "amirh@gmail.com",
        "password" : "12321"
    }
    response = annon_client.post("/auth/register" , json=payload)
    assert response.status_code == status.HTTP_200_OK
        
def test_user_auth(annon_client):
    payload = {
        "email" : "amirh@gmail.com",
        "password" : "12321"
    }
    response = annon_client.post("/auth/login" , json=payload)
    assert response.status_code == status.HTTP_200_OK
    