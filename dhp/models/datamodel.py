import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from dhp.models._base import Base
from dhp.models._data_readers import DATA_READERS


class DataEdge(Base):
    __tablename__ = "data_edge"
    source_data_id = Column(UUID, ForeignKey("data.id"), primary_key=True)
    derived_data_id = Column(UUID, ForeignKey("data.id"), primary_key=True)
    extra_data = Column(String(50))
    source_data = relationship("source_data", back_populates="derived_data")
    derived_data = relationship("derived_data", back_populates="source_data")


# data_meta_data_association_table = Table(
#     'data_meta_data_association_table',
#     Base.metadata,
#     Column("left_id", UUID, ForeignKey("left.id"), primary_key=True),
#     Column("right_id", UUID, ForeignKey("right.id"), primary_key=True),
# )
#
# data_edge_meta_data_association_table = Table(
#     'data_edge_meta_data_association_table',
#     Base.metadata,
#     Column("left_id", UUID, ForeignKey("left.id"), primary_key=True),
#     Column("right_id", UUID, ForeignKey("right.id"), primary_key=True),
# )


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
    # Data IO
    # #################### #

    # Windows max length which is 260 characters which is the shortest of linux,
    # windows and AWS S3
    _data_file = Column(String(260))

    # _data_io = Column(Enum(DataIO))

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
    time_deleted = Column(DateTime(timezone=True))

    # ################### #
    # Relationships
    # ################### #
    source_data = relationship("DataEdge", back_populates="derived_data")
    derived_data = relationship("DataEdge", back_populates="source_data")


# class MetaData(Base):
#     __tablename__ = "meta_data"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#
#     key = Column(String(260), nullable=False)
#     value = Column(PickleType, nullable=False)


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
