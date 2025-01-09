import bcrypt


# 验证用户输入的密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt 会自动提取哈希值中的盐并重新计算哈希值进行比对
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# 假设数据库中的哈希值为
hashed_password_from_db = "$2b$12$1CFL6UXpoOBJhVwo9ITobORJZzOAB1wR6uLAQY8XQaeSj1pgvRx2e"

# 用户输入的密码
plain_password = "123"

# 验证密码
if verify_password(plain_password, hashed_password_from_db):
    print("密码正确")
else:
    print("密码错误")

