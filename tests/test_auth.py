# TEST EXISTING USER - OK LOGIN
def test_login_known_user(client, test_user):

    response = client.post(
        "/auth/login",
        json={
            "user_login": "admin",  # comes from test_user
            "password": "admin123",  # comes from test_user
        },
    )

    # TEST OK - USER LOGGED -- ELSE 200 FAILED LOGIN
    assert response.status_code == 200

    print()  # Just visual Format prints
    print(f".TEST : test_login_known_user --> PASSED ------ Status code: {response.status_code}")


# TEST IF BAD LOGIN - WRONG PASS
def test_login_wrong_password(client, test_user):

    response = client.post("/auth/login", json={"user_login": "admin", "password": "wrong_password"})

    assert response.status_code == 401

    print(f"TEST : test_login_wrong_password --> PASSED ------ Status code: {response.status_code}")


# TEST IF BAD LOGIN - WRONG USER
def test_login_wrong_user(client, test_user):

    response = client.post("/auth/login", json={"user_login": "wrong_user", "password": "admin123"})

    assert response.status_code == 401

    print(f"TEST : test_login_wrong_user --> PASSED ------ Status code: {response.status_code}")


# TEST CHECK IF JWT TOKEN IS VALID
def test_login_returns_jwt(client, test_user):

    response = client.post("/auth/login", json={"user_login": "admin", "password": "admin123"})

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "token_type" in body
    assert body["token_type"] == "bearer"

    print(f"TEST : test_login_returns_jwt --> PASSED ------ Status code: {response.status_code}")


# TEST ACCESS INCIDENTS ENDPOINT WHIT TOKEN
def test_access_protected_incidents_endpoint_token(client, auth_headers):

    response = client.get("/incidents", headers=auth_headers)

    assert response.status_code == 200

    print(f"TEST : test_access_protected_incidents_endpoint_token --> PASSED ------ Status code: {response.status_code}")


# TEST ACCESS INCIDENTS ENDPOINT WHITOUT TOKEN
def test_access_protected_incidents_endpoint_NOtoken(client):

    response = client.get("/incidents")

    assert response.status_code == 401

    print(f"TEST : test_access_protected_incidents_endpoint_NOtoken --> PASSED ------ Status code: {response.status_code}")


# TEST ACCESS INCIDENTS ENDPOINT WHIT WRONG TOKEN
def test_access_protected_endpoint_invalid_token(client):

    response = client.get("/incidents", headers={"Authorization": "Bearer wrong_token"})

    assert response.status_code == 401

    print(f"TEST : test_access_protected_endpoint_invalid_token --> PASSED ------ Status code: {response.status_code}")
