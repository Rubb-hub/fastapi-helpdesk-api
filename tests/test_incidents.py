
# --------------POST--------------------POST------------------ POST ---------------------------
# TEST INCIDENTS POST -- INCIDENT CREATION
def test_create_incident(client, auth_headers, valid_incident):

    response = client.post("/incidents", headers=auth_headers, json=valid_incident)

    assert response.status_code == 201  # 201 Created: resource successfully created (REST convention)

    body = response.json()

    assert body["inc_title"] == valid_incident["inc_title"]
    assert body["inc_priority"] == valid_incident["inc_priority"]
    assert body["inc_state"] == valid_incident["inc_state"]
    assert body["inc_assignee"] == valid_incident["inc_assignee"]

    assert "id" in body
    assert "inc_create_date" in body

    print()
    print(f".TEST : test_create_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS POST -- INVALID PRIORITY !=LOW, MEDIUM or HIGH --> schemas.py -> class Priority
def test_create_incident_invalid_priority(client, auth_headers, valid_incident):

    valid_incident["inc_priority"] = "super_high"  # Override inc_priority in the valid incident

    response = client.post("/incidents", headers=auth_headers, json=valid_incident)

    assert response.status_code == 422

    print(f"TEST : test_create_incident_invalid_priority --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS POST -- INVALID STATE !=Assigned, in_progress, Closed --> schemas.py -> class State
def test_create_incident_invalid_state(client, auth_headers, valid_incident):

    valid_incident["inc_state"] = "opened"  # Override inc_state in the valid incident

    response = client.post("/incidents", headers=auth_headers, json=valid_incident)

    assert response.status_code == 422

    print(f"TEST : test_create_incident_invalid_state --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS POST -- INVALID TITLE - cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_title
def test_create_incident_empty_title(client, auth_headers, valid_incident):

    valid_incident["inc_title"] = "      "  # Override inc_title in the valid incident

    response = client.post("/incidents", headers=auth_headers, json=valid_incident)

    assert response.status_code == 422

    print(f"TEST : test_create_incident_empty_title --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS POST -- INVALID ASSIGNEE - cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_assignee
def test_create_incident_empty_assignee(client, auth_headers, valid_incident):

    valid_incident["inc_assignee"] = "     "

    response = client.post("/incidents", headers=auth_headers, json=valid_incident)

    assert response.status_code == 422

    print(f"TEST : test_create_incident_empty_assignee --> PASSED ------ Status code: {response.status_code}")


# -------------------GET--------------------------------GET--------------------GET--------------
# TEST INCIDENTS GET -- GET BY ID
def test_get_incident_by_id(client, auth_headers, test_incident):

    response = client.get(f"/incidents/{test_incident.id}", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == test_incident.id
    assert body["inc_title"] == test_incident.inc_title
    assert body["inc_priority"] == test_incident.inc_priority

    print(f"TEST : test_get_incident_by_id --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS GET -- GET BY ID - NON EXISTING ID
def test_get_non_existing_incident(client, auth_headers):

    response = client.get("/incidents/9999", headers=auth_headers)

    assert response.status_code == 404

    assert response.json()["detail"] == "Cant find incident - there is no incident with that ID"
    print(f"TEST : test_get_non_existing_incident --> PASSED ------ Status code: {response.status_code}")


# -----------------PUT---------------------PUT--------------------PUT-----------
# TEST INCIDENTS PUT -- UPDATE BY ID
def test_update_incident(client, auth_headers, test_incident, db_session):

    updated_incident = {
        "inc_title": "Cant Acces TS_bbdd_ux43",
        "inc_description": "Message said not valid user.",
        "inc_state": "closed",
        "inc_priority": "low",
        "inc_assignee": "shopie",
    }

    response = client.put(f"/incidents/{test_incident.id}", headers=auth_headers, json=updated_incident)

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == test_incident.id
    assert body["inc_title"] == updated_incident["inc_title"]
    assert body["inc_description"] == updated_incident["inc_description"]
    assert body["inc_state"] == updated_incident["inc_state"]
    assert body["inc_priority"] == updated_incident["inc_priority"]
    assert body["inc_assignee"] == updated_incident["inc_assignee"]

    updated = db_session.get(type(test_incident), test_incident.id)  # check database

    assert updated.inc_title == updated_incident["inc_title"]
    assert updated.inc_description == updated_incident["inc_description"]
    assert updated.inc_state == updated_incident["inc_state"]
    assert updated.inc_priority == updated_incident["inc_priority"]
    assert updated.inc_assignee == updated_incident["inc_assignee"]

    print(f"TEST : test_update_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PUT -- UPDATE BY ID - NON EXISTING ID
def test_update_non_existing_incident(client, auth_headers, valid_incident):

    response = client.put("/incidents/9999", headers=auth_headers, json=valid_incident)

    assert response.status_code == 404
    assert response.json()["detail"] == "Cant update incident - there is no incident with that ID"
    print(f"TEST : test_update_non_existing_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PUT -- UPDATE BY ID -- INVALID PRIORITY !=LOW, MEDIUM or HIGH --> schemas.py -> class Priority
def test_update_incident_invalid_priority(client, auth_headers, test_incident):

    updated_incident = {
        "inc_title": "Cant Acces TS_bbdd_ux43",
        "inc_description": "Message said not valid user.",
        "inc_state": "closed",
        "inc_priority": "outrage",
        "inc_assignee": "shopie",
    }

    response = client.put(f"/incidents/{test_incident.id}", headers=auth_headers, json=updated_incident)

    assert response.status_code == 422

    print(f"TEST : test_update_incident_invalid_priority --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PUT -- UPDATE BY ID -- INVALID STATE !=Assigned, in_progress, Closed --> schemas.py -> class State
def test_update_incident_invalid_state(client, auth_headers, test_incident):

    updated_incident = {
        "inc_title": "Cant Acces TS_bbdd_ux43",
        "inc_description": "Message said not valid user.",
        "inc_state": "confirmed",
        "inc_priority": "low",
        "inc_assignee": "shopie",
    }

    response = client.put(f"/incidents/{test_incident.id}", headers=auth_headers, json=updated_incident)

    assert response.status_code == 422

    print(f"TEST : test_update_incident_invalid_state --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PUT -- UPDATE BY ID -- cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_title
def test_update_incident_invalid_title(client, auth_headers, test_incident):

    updated_incident = {
        "inc_title": "",
        "inc_description": "Message said not valid user.",
        "inc_state": "closed",
        "inc_priority": "low",
        "inc_assignee": "shopie",
    }

    response = client.put(f"/incidents/{test_incident.id}", headers=auth_headers, json=updated_incident)

    assert response.status_code == 422

    print(f"TEST : test_update_incident_invalid_title --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PUT -- UPDATE BY ID -- cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_assignee
def test_update_incident_invalid_assignee(client, auth_headers, test_incident):

    updated_incident = {
        "inc_title": "Cant Acces TS_bbdd_ux43",
        "inc_description": "Message said not valid user.",
        "inc_state": "closed",
        "inc_priority": "low",
        "inc_assignee": "     ",
    }

    response = client.put(f"/incidents/{test_incident.id}", headers=auth_headers, json=updated_incident)

    assert response.status_code == 422

    print(f"TEST : test_update_incident_invalid_assignee --> PASSED ------ Status code: {response.status_code}")


# --------PATCH---------------------PATCH-----------------PATCH--------------
# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID
def test_partial_update_incident(client, auth_headers, test_incident, db_session):

    patch_data = {"inc_priority": "low"}

    response = client.patch(f"/incidents/{test_incident.id}", headers=auth_headers, json=patch_data)

    assert response.status_code == 200

    body = response.json()

    # Updated field
    assert body["inc_priority"] == "low"

    # Unchanged fields
    assert body["inc_title"] == test_incident.inc_title
    assert body["inc_description"] == test_incident.inc_description
    assert body["inc_state"] == test_incident.inc_state
    assert body["inc_assignee"] == test_incident.inc_assignee

    # Verify database
    updated = db_session.get(type(test_incident), test_incident.id)

    assert updated.inc_priority == "low"
    assert updated.inc_title == test_incident.inc_title
    assert updated.inc_description == test_incident.inc_description
    assert updated.inc_state == test_incident.inc_state
    assert updated.inc_assignee == test_incident.inc_assignee

    print(f"TEST : test_partial_update_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID --- NON EXISTING ID
def test_partial_update_non_existing_incident(client, auth_headers):

    response = client.patch("/incidents/9999", headers=auth_headers, json={"inc_priority": "low"})

    assert response.status_code == 404

    assert response.json()["detail"] == "Cant update incident - there is no incident with that ID"
    print(f"TEST : test_partial_update_non_existing_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID -- INVALID PRIORITY !=LOW, MEDIUM or HIGH --> schemas.py -> class Priority
def test_partial_update_invalid_priority(client, auth_headers, test_incident):

    response = client.patch(f"/incidents/{test_incident.id}", headers=auth_headers, json={"inc_priority": "super_high"})

    assert response.status_code == 422

    print(f"TEST : test_partial_update_invalid_priority --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID -- cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_title
def test_partial_update_invalid_title(client, auth_headers, test_incident):

    response = client.patch(f"/incidents/{test_incident.id}", headers=auth_headers, json={"inc_title": "   "})

    assert response.status_code == 422

    print(f"TEST : test_partial_update_invalid_title --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID -- cannot be empty (“”) or contain only spaces("   ") --> schemas.py -> def not_empty_assignee
def test_partial_update_invalid_assignee(client, auth_headers, test_incident):

    response = client.patch(f"/incidents/{test_incident.id}", headers=auth_headers, json={"inc_assignee": ""})

    assert response.status_code == 422

    print(f"TEST : test_partial_update_invalid_assignee --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS PATCH -- PARTIAL UPDATE BY ID -- INVALID STATE !=Assigned, in_progress, Closed --> schemas.py -> class State
def test_partial_update_invalid_state(client, auth_headers, test_incident):

    response = client.patch(f"/incidents/{test_incident.id}", headers=auth_headers, json={"inc_state": "Rejected"})

    assert response.status_code == 422

    print(f"TEST : test_partial_update_invalid_state --> PASSED ------ Status code: {response.status_code}")


# --------------DELETE-----------------------DELETE------------------DELETE------------
# TEST INCIDENTS DELETE --- DELETE BY ID --
def test_delete_incident(client, auth_headers, test_incident, db_session):

    response = client.delete(f"/incidents/{test_incident.id}", headers=auth_headers)

    assert response.status_code == 200

    deleted = db_session.get(type(test_incident), test_incident.id)

    assert deleted is None

    assert response.json()["message"] == "Incident deleted successfully"
    print(f"TEST : test_delete_incident --> PASSED ------ Status code: {response.status_code}")


# TEST INCIDENTS DELETE --- DELETE BY ID -- NON EXISTING ID
def test_delete_non_existing_incident(client, auth_headers):

    response = client.delete("/incidents/9999", headers=auth_headers)

    assert response.status_code == 404

    assert response.json()["detail"] == "Cant delete incident - there is no incident with that ID"
    print(f"TEST : test_delete_non_existing_incident --> PASSED ------ Status code: {response.status_code}")
