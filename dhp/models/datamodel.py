import uuid

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from dhp.models._base import Base
from dhp.models._data_readers import DATA_READERS, DataIO


class BaseData(Base):
    __tablename__ = "base_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Windows max length which is 260 characters which is the shortest of linux,
    # windows and AWS S3
    _data_file = Column(String(260))

    _data_io = Column(Enum(DataIO))

    @property
    def data(self):
        return DATA_READERS[self._data_io](self._data_file)
