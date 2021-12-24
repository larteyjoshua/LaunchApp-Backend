from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from utils.hashing import Hash
from models import models
from utils import schemas
from fastapi.encoders import jsonable_encoder


def create(request: schemas.Role, db: Session):
    role = db.query(models.Role).filter(models.Role.name == request.name).first()
    if role:
        return{"info": f"Role with the name {request.name} already exist"}
    else: 
        new_role = models.Role(name=request.name)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return{"success": f"Role with the name {request.name} created"}


def show(id: int, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with the id {id} is not available")
    return role

def get_all(db: Session):
    roles = db.query(models.Role).all()
    return roles

def destroy(id: int, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id)
    if not role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    role.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id: int, request: schemas.ShowUser, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
     
    role.name = request.name
    db.commit()
    db.refresh(role)
    return role