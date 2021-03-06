import uuid

from sqlalchemy import Column, DateTime, ForeignKey, PickleType, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from dhp.models._base import Base


class DataEdge(Base):
    __tablename__ = "data_edge"
    source_data_id = Column(ForeignKey("data.id"), primary_key=True)
    derived_data_id = Column(ForeignKey("data.id"), primary_key=True)
    meta_data = Column(String(50))


class Data(Base):
    __tablename__ = "data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # #################### #
    # Polymorphism
    # #################### #
    _type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "base_data",
        "polymorphic_on": _type,
    }

    # #################### #
    # Data IO
    # #################### #
    data = Column(PickleType, nullable=False)

    # ################### #
    # Relationships
    # ################### #
    source_data = relationship(
        "Data",
        secondary="data_edge",
        primaryjoin="Data.id==DataEdge.derived_data_id",
        secondaryjoin="Data.id==DataEdge.source_data_id",
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


class FRF(Data):
    __mapper_args__ = {
        "polymorphic_identity": "frf",
    }
