from app.core.db import get_db_session
from app.models.user import User, UserCreate, UserUpdate
from fastapi import Depends, HTTPException
from sqlmodel import Session


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self) -> list[User]:
        return self.session.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def create_user(self, user_to_create: UserCreate) -> User:
        user = User.from_orm(user_to_create)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        db_user = self.get_user_by_id(user_id)
        if user_update.name:
            db_user.name = user_update.name
        if user_update.role:
            db_user.role = user_update.role
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.password = user_update.password
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> User:
        db_user = self.get_user_by_id(user_id)
        self.session.delete(db_user)
        self.session.commit()
        return db_user

# 获取服务实例
def get_user_service(session: Session = Depends(get_db_session)):
    return UserService(session)
