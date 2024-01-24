from sqlalchemy.orm import Session
from sqlalchemy import (insert, select,
                        update, delete, and_, text)

from .. import engine
from ..__models__ import tables_names

from ...settings import logger


class DB:

    def __init__(self) -> None:
        self._session = Session(engine)


    def err(self, msg) -> ValueError:
        logger.error(f'{msg} is not instance of sqlalchemy.sql.schema.Table')
        raise ValueError(f'{msg} is not instance of sqlalchemy.sql.schema.Table')


    def _check_obj_instance(self, instance: object) -> object | ValueError:
        try:
            return instance.name in tables_names
        except Exception:
            self.err(instance)


    def cursor(self) -> Session:
        return self._session


    def insert_data(self, instance: object, **kwargs):
        if self._check_obj_instance(instance):
            query = insert(instance).values(**kwargs)
            self.cursor().execute(query).connection.commit()
            
            logger.info(f'insert {kwargs.keys()} into {instance}')
            query = text(''.join([f'{instance.name}.{k} == "{v}" AND ' for k, v in kwargs.items() if v])[:-5])

            return self.get_where(instance, exp=query, all_=False)
        else:
            self.err(instance)


    def get_all(self, instance: object):
        if self._check_obj_instance(instance):
            query = select(instance)
            result = self.cursor().execute(query)
            
            for i in result.fetchall():
                yield i
        else:
            self.err(instance)


    def get_where(self, instance: object, 
                  and__ = None, exp = None, 
                  all_: bool = True):
        if and__:
            query = select(instance).where(and_(*and__))
        else:
            query = select(instance).where(exp)

        ex = self.cursor().execute(query)
        if all_:
            return ex.all()
        else: return ex.fetchone()


    def update_data(self, instance: object,
                    and__ = None, exp = None, **kwargs):
        if self._check_obj_instance(instance):
            if and__:
                query = update(instance).where(and_(*and__)).values(**kwargs)
            else:
                query = update(instance).where(exp).values(**kwargs)

            changes = self.cursor().execute(query)
            changes.connection.commit()

            logger.info(f"update {kwargs.keys()} in {instance}")
            return self.get_where(instance, and__, exp, all_=False)
        else:
            self.err(instance)


    def delete_data(self, instance: object,
                    and__ = None, exp = None):
        if self._check_obj_instance(instance):
            if and__:
                query = delete(instance).where(and_(*and__))
            else:
                query = delete(instance).where(exp)

            self.cursor().execute(query).connection.commit()
            logger.info(f"delete data in {instance}")

        else:
            self.err(instance)