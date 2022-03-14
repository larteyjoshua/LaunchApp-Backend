from asyncio.windows_events import NULL
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from utils.hashing import Hash
from models import models
from utils import schemas

def create(request: schemas.Admin, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        return{"info": f"User with the email {request.email} already exist"}
    else: 
        new_manager = models.User(fullName=request.fullName,
                                     email=request.email, 
                                     password= Hash.bcrypt(request.password))
        db.add(new_manager)
        db.commit()
        db.refresh(new_manager)
        return{"success": f"Manager with the email {request.email} created"}


def show(id: int, db: Session):
    admin = db.query(models.User).filter(models.User.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the id {id} is not available")
    return admin

def get_all(db: Session):
    # admins =db.query(
    # models.User, 
    # models.UserRole, 
    # models.Role).filter(
    # models.User.id ==  models.UserRole.user_id).filter(
    # models.UserRole.role_id == models.Role.id).filter(models.Role.name == "ADMIN").all()
    admins = db.query(models.User).join(models.UserRole, models.User.id == models.UserRole.user_id).all()
    #roles = db.query(models.Role, models.UserRole).all()

    return admins

def destroy(id: int, db: Session):
    admin = db.query(models.User).filter(models.User.id == id)
    if not admin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id {id} not found")
    admin.delete(synchronize_session=False)
    db.commit()
    return{"success": f"Admin with the email {admin.email} Deleted"}

def update(id: int, request: schemas.ShowUser, db: Session):
    admin = db.query(models.User).filter(models.User.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id {id} not found")
    
    admin.password = Hash.bcrypt(request.password) 
    admin.email = request.email
    admin.fullName = request.fullName
    admin.isActive = request.isActive
    admin.isSuper = request.isSuper
    admin.roleId = request.roleId
    db.commit()
    db.refresh(admin)
    return admin


def is_active(admin: schemas.ShowAdmin) -> bool:
        return admin.is_active

def is_superuser(admin: schemas.ShowAdmin) -> bool:
        return admin.is_superuser
    
def get_by_email(db: Session, request):
    admin = db.query(models.Manager).filter(
        models.User.email == request.username).first()
    return admin

def showAdmin(db: Session, email: str ):
    #admin = db.query(models.Manager).filter(models.Manager.email == email).first()
    admin = db.query(models.User).join(models.Role).filter(models.User.email == email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with the id {email} is not available")
    #role =db.query(models.Role).filter(models.Role.id == admin.roleId).first()
    return admin