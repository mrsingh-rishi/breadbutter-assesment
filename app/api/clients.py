from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import client
from app.schemas.schemas import ClientResponse, ClientCreate

router = APIRouter()


@router.post("/", response_model=ClientResponse)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db)
):
    """Create a new client."""
    db_client = client.get_by_email(db, email=client_in.email)
    if db_client:
        raise HTTPException(
            status_code=400,
            detail="Client with this email already exists"
        )
    
    return client.create(db, client_in)


@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Get all clients with pagination."""
    return client.get_multi(db, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific client by ID."""
    db_client = client.get(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: str,
    client_update: dict,
    db: Session = Depends(get_db)
):
    """Update a client profile."""
    db_client = client.get(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client.update(db, db_client, client_update)


@router.delete("/{client_id}")
def delete_client(
    client_id: str,
    db: Session = Depends(get_db)
):
    """Delete a client."""
    db_client = client.delete(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}
