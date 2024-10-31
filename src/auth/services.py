from src.auth.schemes import UserCreateSchema
from .models import User
from .utils import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc



class UserService:

    async def get_all_users(self, session: AsyncSession):
        query = select(User).order_by(desc(User.created_at))
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_email(
        self, session: AsyncSession, email: str, as_dict: bool = True
    ) -> User | dict | None:
        """Get a user by their email address."""
        
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        
        if user is None:
            return None

        if as_dict:
            return user.model_dump()
        return user

    
    async def user_exists(self, session: AsyncSession, user_email: str) -> bool:
        """ Check if a user exists by their email address. """
        user = await self.get_user_by_email(session, user_email, as_dict=False)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> User | dict:
        user_data_dict = user_data.model_dump()
        user_data_dict['password'] = generate_password_hash(user_data_dict['password'])
        new_user = User(**user_data_dict)
        session.add(new_user)
        await session.commit()

        return new_user.model_dump()

        
