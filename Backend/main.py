from fastapi import FastAPI
from models import  models
from utils.database import SessionLocal, engine
from routers import users, admin, roles, company, riders, foods, orders, feedbacks, account

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
async def home():
    return {"message": "Hello World"}

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(roles.router)
app.include_router(company.router)
app.include_router(riders.router)
app.include_router(foods.router)
app.include_router(orders.router)
app.include_router(feedbacks.router)
app.include_router(account.router)