from fastapi import FastAPI

from app.core.db import init_db
from app.routers.user import router as user_router

app = FastAPI()

# 初始化数据库
init_db()

# 注册用户路由
app.include_router(user_router, prefix="/api", tags=["users"])
