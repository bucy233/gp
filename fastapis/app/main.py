from fastapi import FastAPI

from app.routers import company, user, vessel  # 引入路由

app = FastAPI()


# 注册路由
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(company.router, prefix="/api", tags=["companies"])
app.include_router(vessel.router, prefix="/api", tags=["vessel"])

#uvicorn app.main:app --reload