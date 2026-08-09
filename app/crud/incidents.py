
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentPartialUpdate, IncidentUpdate


# ----SQL FUNCTION -- ENDPOINT CHECK INCS - ALL INC - QUERY PARAMS - GET METHOD
def get_incidentsb_by_id(
    inc_priority: str | None = None,
    inc_state: str | None = None,
    inc_assignee: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):

    query = db.query(Incident)

    if inc_priority:
        query = query.filter(
            Incident.inc_priority == inc_priority  # Add a filter to the query to only return incidents with the specified priority
        )

    if inc_state:
        query = query.filter(
            Incident.inc_state == inc_state  # Add a filter to the query to only return incidents with the specified state
        )

    if inc_assignee:
        query = query.filter(
            Incident.inc_assignee == inc_assignee  # Add a filter to the query to only return incidents with the specified assignee
        )

    query = query.offset(offset).limit(limit)  # Aply limit and offset for pagination
    incidents = query.all()

    return incidents


# ---SQL FUNCTION -- ENDPOINT CHECK 1 SPECIFIC INC ---- GET METHOD
def get_incident(db: Session, incident_id: int):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if db_incident is None:  # If not exist inc whit current id return none
        return None

    return db_incident


# ----SQL FUNCTION -- ENDPOINT CREATE INC --- POST METHOD
def create_incident(db: Session, incident: IncidentCreate):

    db_incident = Incident(
        inc_title=incident.inc_title,
        inc_description=incident.inc_description,
        inc_state=incident.inc_state,
        inc_priority=incident.inc_priority,
        inc_assignee=incident.inc_assignee,
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


# ----SQL FUNCTION -- ENDPOINT UPDATE INC -- PUT METHOD
def update_incident(incident_id: int, incident: IncidentUpdate, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if db_incident is None:  # If not exist inc whit current id return none
        return None

    db_incident.inc_title = incident.inc_title
    db_incident.inc_description = incident.inc_description
    db_incident.inc_state = incident.inc_state
    db_incident.inc_priority = incident.inc_priority
    db_incident.inc_assignee = incident.inc_assignee

    db.commit()

    db.refresh(db_incident)

    return db_incident


# ----SQL FUNCTION -- ENDPOINT PARTIAL UPDATE INC ---- PATCH METHOD
def patch_incident(incident_id: int, incident: IncidentPartialUpdate, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if db_incident is None:  # If not exist inc whit current id return none
        return None

    update_data = incident.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)

    return db_incident


# ----SQL FUNCTION -- ENDPOINT DELETE INC ---- DELETE METHOD
def delete_incident(incident_id: int, db: Session = Depends(get_db)):

    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if db_incident is None:  # If not exist inc whit current id return none
        return None

    db.delete(db_incident)

    db.commit()

    return {"message": "Incident deleted successfully"}
