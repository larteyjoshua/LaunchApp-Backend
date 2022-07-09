
from fastapi import HTTPException, status, BackgroundTasks
from app.models import  models
from app.utils import schemas
from sqlalchemy.orm import Session
 
def create(request: schemas.UserRoleBase, db: Session):
        print('request', request)
        new_role = models.UserRole(user_id=request.user_id, role_id = request.role_id)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role


def show(id: int, db: Session):
    role = db.query(models.UserRole).filter(models.UserRole.role_id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Role with the id {id} is not available")
    return role

def get_all(db: Session):
    roles = db.query(models.UserRole).all()
    return roles

def destroy(id: int, db: Session):
    role = db.query(models.UserRole).filter(models.UserRole.role_id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Role with id {id} not found")
    db.delete(role)
    db.commit()
    return role


def update(id: int, request: schemas.UserRoleBase, db: Session):
    role = db.query(models.UserRole).filter(models.UserRole.role_id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" User Role with id {id} not found")
     
    role.role_id = request.role_id
    role.user_id = request.user_id
    db.commit()
    db.refresh(role)
    return role