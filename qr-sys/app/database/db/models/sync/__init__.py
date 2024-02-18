from sqlalchemy.orm import Session
from sqlalchemy import (insert, select,
                        update, and_, text, func, delete)

from ...Meta.engine_sync import engine
from ...TablesParse import tables_names

from .....settings import logger


class sync_db:

    def err(self, msg) -> ValueError:
        logger.error(f'{msg} is not instance of sqlalchemy.sql.schema.Table')
        raise ValueError(f'{msg} is not instance of sqlalchemy.sql.schema.Table')


    def _check_obj_instance(self, instance: object) -> object | ValueError:
        try:
            return instance.name in tables_names
        except Exception:
            self.err(instance)


    def cursor(self) -> Session:
        return Session(engine)
            

    def insert_data(self, instance: object, get_data: bool = True, **kwargs):
        if self._check_obj_instance(instance):
            query = insert(instance).values(**kwargs)

            session = self.cursor()
            session.begin()
            session.execute(query)
            session.commit()

            logger.info(f'insert {kwargs.keys()} into {instance}')

            if get_data is True:
                query = text(''.join([f'{instance.name}.{k} == "{v}" AND ' for k, v in kwargs.items() if v])[:-5])

                return self.get_where(instance, exp=query, all_=False, session=session)
            
            session.close()
        else:
            self.err(instance)


    def count_items(self, executor: Session, esteintment, *args) -> int:
        return executor.query(func.count()).filter(esteintment(*args) if args else esteintment).scalar()


    def get_where(self, instance: object, 
                  and__ = None, exp = None, 
                  all_: bool = True, count: bool = False,
                  offset: int = None, limit: int = None, to_dict: bool = False, session: Session = None):
        
        query = select(instance)

        if and__:
            query = query.where(and_(*and__))
        else:
            query = query.where(exp)

        if session is None:
            session = self.cursor()
            session.begin()

        count_items = self.count_items(session, exp) if (count and exp is not None) else self.count_items(session, and_, and__) if (count and and__ is not None) else None

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)


        result = session.execute(query)

        if all_:
            result = result.fetchall()
        else:
            result = result.fetchone()

        session.close()

        if to_dict:
            if isinstance(result, list):
                result = [i._asdict() for i in result]
            else:
                result = result._asdict() if result else None

        return result if not count_items else [result, count_items]


    def update_data(self, instance: object,
                    and__ = None, exp = None, **kwargs):
        if self._check_obj_instance(instance):
            if and__:
                query = update(instance).where(and_(*and__)).values(**kwargs)
            else:
                query = update(instance).where(exp).values(**kwargs)


            session = self.cursor()
            session.begin()
            session.execute(query)
            session.commit()

            logger.info(f"update {kwargs.keys()} in {instance}")
            return self.get_where(instance, and__, exp, all_=False, session=session)
        else:
            self.err(instance)


    def delete_data(self, instance: object,
                    and__ = None, exp = None):
        if self._check_obj_instance(instance):
            if and__:
                query = delete(instance).filter(and_(*and__))
            else:
                query = delete(instance).filter(exp)

            session = self.cursor()
            session.begin()
            session.execute(query)
            session.commit()
            session.close()

            logger.info(f"delete data in {instance}")

        else:
            self.err(instance)