from sqlmodel import Session, SQLModel, create_engine

# 数据库连接配置
DATABASE_URL = "mysql+pymysql://root:111222@localhost/g_p"

# 创建引擎
engine = create_engine(DATABASE_URL, echo=True)

# 初始化数据库
def init_db():
    SQLModel.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db_session():
    with Session(engine) as session:
        yield session
