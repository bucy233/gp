from app.core.db import get_db_session
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

router = APIRouter()

@router.get("/test-db-connection")
async def test_db_connection(session: Session = Depends(get_db_session)):
    try:
        # 尝试查询数据库中的一行数据
        result = session.execute(select(User).limit(1)).fetchone()
        if result:
            return {"message": "数据库连接成功", "user": result[0].dict()}  # 返回一个用户数据
        else:
            raise HTTPException(status_code=404, detail="数据库中没有用户")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {str(e)}")
