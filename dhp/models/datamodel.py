import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from dhp.models._base import Base
from dhp.models._data_readers import DATA_READERS, DataIO

data_edge = Table(
    "data_edge",
    Base.metadata,
    Column("source_data", UUID, ForeignKey("data.id"), primary_key=True),
    Column("derived_data", UUID, ForeignKey("data.id"), primary_key=True),
)


class Data(Base):
    __tablename__ = "data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # #################### #
    # Polymorphism
    # #################### #
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "base_data",
        "polymorphic_on": type,
        "with_polymorphic": "*",  # Eager load subclass attributes by default.
    }

    # #################### #
    # Data IO columns
    # #################### #

    # Windows max length which is 260 characters which is the shortest of linux,
    # windows and AWS S3
    _data_file = Column(String(260))

    _data_io = Column(Enum(DataIO))

    _data = None  # Cache the expensive data loading operation.

    @property
    def data(self):
        if self._data is None:
            self._data = DATA_READERS[self._data_io](self._data_file)
        return self._data

    # ################### #
    # Immutability
    # ################### #
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # ################### #
    # Relationships
    # ################### #
    source_data = relationship(
        "DirectedEdge",
        secondary=data_edge,
        primaryjoin=id == data_edge.c.derived_data,
        secondaryjoin=id == data_edge.c.source_data,
        backref="derived_data",
    )


class TestData(Data):
    __mapper_args__ = {
        "polymorphic_identity": "test_data",
    }


class TimeHistory(Data):
    __mapper_args__ = {
        "polymorphic_identity": "time_history",
    }


class PSD(Data):
    __mapper_args__ = {
        "polymorphic_identity": "random_vibe_psd",
    }
