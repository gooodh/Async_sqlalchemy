from sqlalchemy.ext.asyncio import AsyncSession
from database import connection
from asyncio import run
from models import Profile, User
from sql_enums import GenderEnum, ProfessionEnum


@connection
async def create_user_example_1(
    username: str, email: str, password: str, session: AsyncSession
) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - username: str - имя пользователя
    - email: str - адрес электронной почты
    - password: str - пароль пользователя
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - int - идентификатор созданного пользователя
    """

    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id

# new_user_id = run(create_user_example_1(username="nikulin",
#                                         email="nikulin@example.com",
#                                         password="asdasd"))

# print(f"Новый пользователь с идентификатором {new_user_id} создан")
@connection
async def get_user_by_id_example_2(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()

    profile = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        profession=profession,
        interests=interests,
        contacts=contacts)

    session.add(profile)
    await session.commit()
    print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
    return {'user_id': user.id, 'profile_id': profile.id}


@connection
async def get_user_by_id_example_3(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        user = User(username=username, email=email, password=password)
        session.add(user)
        await session.flush()  # Промежуточный шаг для получения user.id без коммита

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            interests=interests,
            contacts=contacts
        )
        session.add(profile)

        # Один коммит для обоих действий
        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()  # Откатываем транзакцию при ошибке
        raise e


user_profile = run(get_user_by_id_example_3(
    username="dao",
    email="dao@example.com",
    password="password7123",
    first_name="dao",
    last_name="Dao",
    age=28,
    gender=GenderEnum.MALE,
    profession=ProfessionEnum.ENGINEER,
    interests=["hiking", "photography", "coding"],
    contacts={"phone": "+723456789", "email": "dao@example.com"},
))
