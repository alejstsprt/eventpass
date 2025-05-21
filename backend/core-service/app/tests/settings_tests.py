# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from ..models.models import Base


# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def get_test_db():
#     # Создаем все таблицы заново для каждого теста
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)