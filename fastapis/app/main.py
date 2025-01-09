from fastapi import FastAPI

from app.routers import company, user  # 引入company路由

app = FastAPI()


# 注册路由
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(company.router, prefix="/api", tags=["companies"])


#uvicorn app.main:app --reload