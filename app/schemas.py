from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict


# ---------------------------Check fullfillment of the requirements for the fields in the Incident model using Pydantic validators ----------------------------------
# CUSTOM VALIDATOR -- #inc_title are not empty or only whitespace
def not_empty_title(v: str) -> str:
    if not v.strip():
        raise ValueError("inc_title can not be empty or contain only spaces")
    return v.strip()  # Clean whitespace from the title


AllowedTitle = Annotated[str, AfterValidator(not_empty_title)]


# CUSTOM VALIDATOR -- #inc_Assignee (case insensitive) transforming the value to lowercase and stripping whitespace
def not_empty_assignee(v: str) -> str:
    if not v.strip().lower():
        raise ValueError("inc_assignee cann ot be empty or contain only spaces")
    return v.strip().lower()  # Clean whitespace


AllowedAssignee = Annotated[str, AfterValidator(not_empty_assignee)]


# CUSTOM VALIDATOR -- inc_priority must be either "high", "medium" or "low" (case insensitive) transforming the value to lowercase and stripping whitespace
class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


def validate_priority(value: str) -> str:
    return value.strip().lower()


PriorityType = Annotated[Priority, BeforeValidator(validate_priority)]


# CUSTOM VALIDATOR -- inc_state must be either "closed" , "in_progress" o "assigned" (case insensitive) transforming the value to lowercase and stripping whitespace
class State(str, Enum):
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    ASSIGNED = "assigned"


def validate_state(value: str) -> str:
    return value.strip().lower()


StateType = Annotated[State, BeforeValidator(validate_state)]


# ---------------------------------------CLASSES FOR THE SCHEMAS OF THE INCIDENT MODEL-----------------------------------


# ---- Class BaseModel
class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- VIEW INCIDENT - IncidentResponse
class IncidentResponse(Base):
    id: int
    inc_title: str
    inc_description: str | None  # None means that can be a string or can be none -- filling as null
    inc_state: str
    inc_priority: str
    inc_assignee: str
    inc_create_date: datetime


# --- CREATE NEW INCIDENT - IncidentCreate
class IncidentCreate(Base):
    inc_title: AllowedTitle  # = Field(..., min_length=5, max_length=255) #Field(...)
    inc_description: str | None  # None means that can be a string or can be none -- filling as null
    inc_state: StateType
    inc_priority: PriorityType
    inc_assignee: AllowedAssignee


# --- UPDATE ALL FIELDS OF THE INCIDENT - IncidentUpdate  --- COULD BE USED FOR POST METHOD TOO BUT I WILL CREATE A SEPARATE CLASS
class IncidentUpdate(Base):
    inc_title: AllowedTitle
    inc_description: str | None
    inc_state: StateType
    inc_priority: PriorityType
    inc_assignee: AllowedAssignee


# --- UPDATE SOME FIELDS OF THE INCIDENT - IncidentPartialUpdate
class IncidentPartialUpdate(Base):
    inc_title: AllowedTitle | None = None
    inc_description: str | None = None
    inc_state: StateType | None = None
    inc_priority: PriorityType | None = None
    inc_assignee: AllowedAssignee | None = None


# ---------------------------------------CLASSES FOR THE SCHEMAS OF THE USER MODEL-----------------------------------
# --- LOGIN USER AUTH - LoginRequest
class LoginRequest(BaseModel):
    user_login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
