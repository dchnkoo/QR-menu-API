from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (insert, select,
                        update, and_, text, func, delete)

from ...Meta.engine_async import engine
from ...TablesParse import tables_names

from .....settings import logger
from typing import Any, Tuple


class async_db:

    def __init__(self) -> None:
        self._session = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False
            )


    def err(self, msg) -> ValueError:
        logger.error(f'{msg} is not instance of sqlalchemy.sql.schema.Table')
        raise ValueError(f'{msg} is not instance of sqlalchemy.sql.schema.Table')


    def _check_obj_instance(self, instance: object) -> object | ValueError:
        try:
            return instance.name in tables_names
        except Exception:
            self.err(instance)


    async def get_async_session(self) -> AsyncSession:
        return self._session()


    async def async_insert_data(self, instance: object, get_data: bool = True, **kwargs):
        if self._check_obj_instance(instance):
            
            session = await self.get_async_session()
            data_insert = insert(instance).values(**kwargs)
            
            async with session.begin() as transaction:
                await transaction.session.execute(data_insert)
                await transaction.commit()
            
            logger.info(f'insert {kwargs.keys()} into {instance}')
            query = text(''.join([f"{instance.name}.{k}='{v}' AND " 
                                  for k, v in kwargs.items() if v and isinstance(v, list) is False])[:-5])    

            return await self.async_get_where(instance, exp=query, all_=False) 
            
        else:
            self.err(instance)


    async def async_get_where(self, instance: object, 
                  and__ = None, exp = None, 
                  all_: bool = True, count: bool = False,
                  offset: int = None, limit: int = None, to_dict: bool = False):

        query = select(instance)

        if and__:
            query = query.where(and_(*and__))
        else:
            query = query.where(exp)

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        
        session = await self.get_async_session()
        async with session.begin() as transaction:
            count_items = await self.count_items(transaction, exp, instance) if (count and exp is not None) else self.count_items(transaction, and_, instance, and__) if (count and and__ is not None) else None
            result = await transaction.session.execute(query)

        if all_:
            result = result.fetchall()
        else:
            result = result.fetchone()

        if to_dict:
            if isinstance(result, list):
                result = [i._asdict() for i in result]
            else:
                result = result._asdict() if result else None
        
        return result if not count_items else [result, count_items]


    async def count_items(self, executor: AsyncSession, esteintment, instance: object = None, *args) -> int:
        stmt = select(func.count()).select_from(instance).where(esteintment(*args) if args else esteintment)
        result = await executor.session.execute(stmt)
        return result.scalar()


    async def async_update_data(self, instance: object,
                    and__ = None, exp = None, **kwargs):
        if self._check_obj_instance(instance):
            if and__:
                query = update(instance).where(and_(*and__)).values(**kwargs)
            else:
                query = update(instance).where(exp).values(**kwargs)

            session = await self.get_async_session()

            async with session.begin() as transaction:
                await transaction.session.execute(query)
                await transaction.commit()

            logger.info(f"update {kwargs.keys()} in {instance}")
            return await self.async_get_where(instance, and__, exp, all_=False)

        else:
            self.err(instance)


    async def async_delete_data(self, instance: object,
                                 and__ = None, exp=None):
        if self._check_obj_instance(instance):
            if and__:
                query = delete(instance).filter(and_(*and__))
            else:
                query = delete(instance).filter(exp)

            session = await self.get_async_session()

            async with session.begin() as transaction:
                await transaction.session.execute(query)
                await transaction.commit()

        else:
            self.err(instance)


    async def async_join_data(self, table_1: object, table_2: object, 
                              table_2exp: Any = None, table_2and: Tuple[object] = None, 
                              exp = None, and__ = None):
        
        if table_2exp is not None:
            query = select(table_1, table_2).join(table_2, table_2exp)
        elif table_2and is not None:
            query = select(table_1, table_2).join(table_2, and_(*table_2and))


        if exp is not None:
            query = query.where(exp)
        elif and__ is not None:
            query = query.where(and_(*and__))

        if query is None:
            raise ValueError("Check instances and expression")

        session = await self.get_async_session()

        async with session.begin() as transaction:
            result = await transaction.session.execute(query)

        one = table_1.columns.keys()
        two = table_2.columns.keys()
        oneLen = len(one)
        twoLen = len(two)

        result = result.fetchone()

        from .....framework import t 

        return {table_1.name: t.parse_user_data(dict(zip(one, result[0:oneLen]))), table_2.name: t.parse_user_data(dict(zip(two, result[oneLen:oneLen+twoLen])))} if result else {}