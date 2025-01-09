from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import bcrypt
from jose import JWTError, jwt

SECRET_KEY = "123"  # 从环境变量读取以增强安全性
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码加密
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 密码验证
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# 创建 JWT token
def create_access_token(data: Dict[str, Union[str, int]], expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 验证 JWT token
def verify_token(token: str) -> Optional[Dict[str, Union[str, int]]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise JWTError("Token payload missing 'sub'")
        return payload
    except JWTError as e:
        print(f"Token verification failed: {e}")
        return None
