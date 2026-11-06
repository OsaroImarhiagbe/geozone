from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import ( AuthSessionLocal,AnonSessionLocal)
from collections.abc import AsyncGenerator
from app.middleware.dependencies import get_authenticated_user







# Protected — all authenticated routes
async def get_auth_db() -> AsyncGenerator[AsyncSession,None]:
     async with AuthSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    # await db.execute(text("SET LOCAL ROLE authenticated"))
    # await db.execute(
    #     text("SET LOCAL app.current_user_id = :user_id"),
    #     {"user_id": user_id}
    # )
# user_id:get_current_user_id_dependency

## Public routes, temporay access
async def get_anon_db() -> AsyncGenerator[AsyncSession,None]:
      async with AnonSessionLocal() as session:
             try:
                 yield session
             except Exception:
                 await session.rollback()
                 raise
             finally:
                 await session.close()

async def get_db(current_user = Depends(get_authenticated_user)) -> AsyncGenerator[AsyncSession, None]:
     session_factory = AuthSessionLocal if current_user else AnonSessionLocal

     async with session_factory as session:
          yield session

    # async with AsyncSessionLocal() as session:
    #     try:
    #         yield session
    #     except Exception:
    #         await session.rollback()
    #         raise
    #     finally:
    #         await session.close()
     