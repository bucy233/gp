from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserCreate, UserLogin, UserUpdate
from app.sercices.user import UserService, get_user_service
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

# 创建新用户
@router.post("/users", response_model=User)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    if service.get_user_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册")

    user.password = hash_password(user.password)
    return service.create_user(user)

# 用户登录
@router.post("/login")
async def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    db_user = service.get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邮箱未注册")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"message": "登录成功", "access_token": access_token, "token_type": "bearer"}

# 更新用户信息
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(user_id, user)

# 删除用户
@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)

# 获取所有用户
@router.get("/users", response_model=list[User])
async def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

# 获取单个用户
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)
