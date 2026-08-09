from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import IncidentCreate, IncidentPartialUpdate, IncidentResponse, IncidentUpdate, PriorityType, StateType

router = APIRouter()  # ALL ENDPOINTS START FOR /INCIDENTS


# ----ENDPOINT CHECK INCS - ALL INC - QUERY PARAMS ------ GET METHOD --
@router.get("/incidents", response_model=list[IncidentResponse])
def get_incidentsb_by_id(
    inc_priority: PriorityType | None = None,
    inc_state: StateType | None = None,
    inc_assignee: str | None = None,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,  # Limit the number of incidents returned min 1, max 1000, default 100
    offset: Annotated[int, Query(ge=0)] = 0,  # Limit the offset for pagination, min 0, default 0
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incidents = crud.incidents.get_incidentsb_by_id(inc_priority=inc_priority, inc_state=inc_state, inc_assignee=inc_assignee, limit=limit, offset=offset, db=db)

    return incidents


# ----ENDPOINT CHECK 1 SPECIFIC INC - FILTER BY ID ------ GET METHOD
@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_incident = crud.incidents.get_incident(db, incident_id)

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Cant find incident - there is no incident with that ID")

    return db_incident


# ----ENDPOINT CREATE INC ------- POST METHOD
@router.post("/incidents", response_model=IncidentResponse, status_code=201)  # 201 Created: resource successfully created (REST convention)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_incident = crud.incidents.create_incident(db, incident)

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Cant update incident - there is no incident with that ID")

    return db_incident


# ----ENDPOINT UPDATE INC ------- PUT METHOD
@router.put("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, incident: IncidentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_incident = crud.incidents.update_incident(incident_id, incident, db)

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Cant update incident - there is no incident with that ID")

    return db_incident


# ----ENDPOINT PARTIAL UPDATE INC ------- PATCH METHOD
@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
def patch_incident(incident_id: int, incident: IncidentPartialUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_incident = crud.incidents.patch_incident(incident_id, incident, db)

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Cant update incident - there is no incident with that ID")

    return db_incident


# ----ENDPOINT DELETE INC ------- DELETE METHOD
@router.delete("/incidents/{incident_id}")  # Return 200 because method return answer json
def delete_incident(incident_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_incident = crud.incidents.delete_incident(incident_id, db)

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Cant delete incident - there is no incident with that ID")

    return db_incident
