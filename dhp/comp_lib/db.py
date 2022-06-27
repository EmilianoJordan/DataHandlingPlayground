from uuid import UUID

from sqlalchemy.orm import Session

from dhp.models import Data, engine
from dhp.models._base import Base
from dhp.typing import _SENTINEL


def load_data_object_from_database(uuid: UUID) -> Base:
    with Session(engine) as session:
        with session.begin():
            result = session.query(Data).filter(id=uuid).one()

    return result


def persist_object_to_database(obj):
    with Session(engine) as session:
        with session.begin():
            session.add(obj)


def _load_data_from_uuid(uuid: UUID) -> Base:
    if not isinstance(uuid, UUID):
        # User can naively pass object in that may not be a UUID but a Data object
        # or data
        return uuid

    return load_data_object_from_database(uuid)


def handle_db_object(output_class):
    def decorator(f):
        def wrapper(*args, **kwargs):

            if len(args) == 0:
                data_arg = kwargs.get("data_obj", _SENTINEL)

                if data_arg is _SENTINEL:
                    # The data_obj arg wasn't passed. Rather than raise our own
                    # exception just call the function and let the python
                    # TypeError bubble up.
                    return f(*args, **kwargs)

            else:
                data_arg = args[0]

            if not isinstance(data_arg, UUID):
                return f(*args, **kwargs)

            args = list(args)
            db_object = _load_data_from_uuid(data_arg)

            if len(args) == 0:
                kwargs["data_obj"] = db_object.data

            else:
                args[0] = db_object.data

            result = f(*args, **kwargs)

            return output_class(data=result)

        return wrapper

    return decorator
