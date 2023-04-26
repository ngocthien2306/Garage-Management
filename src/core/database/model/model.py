from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from core.database.connectionmssql import Base

class Track(Base):
    __tablename__ = "tblTrack"
    trackId = Column(Integer, primary_key=True, index=True)
    vehicleId = Column(Integer)
    startTime = Column(String(20))
    endTime = Column(String(20), default=False)
    fee = Column(String(20), default=False)
    siteId= Column(Integer, default=False)
    #items = relationship("Item", back_populates="owner")
class Vehicle(Base):
    __tablename__ = "tblVehicle"
    id = Column(Integer, primary_key=True, index=True)
    plateNum =Column(String(20), default=True)
    location = Column(String(100), default=False)
class Guest(Base):
    __tablename__ = "tblGuest"
    driverId = Column(Integer, primary_key=True, index=True)
    vehicleId = Column(Integer,default=True)
    originPathFace =Column(String(100), default=True)
    detectPathFace =Column(String(100), default=False)

class VehicleExtend(Base):
    __tablename__ = "tblVehicleExtend"
    #vehicle_id = Column(ForeignKey("tblVehicle.id"))
    VehicleExtendId = Column(Integer, primary_key=True)
    vehicleId = Column(Integer)
    status =Column(String(10), default=True)
    typeTransport = Column(String(10), default=True)
    typePlate = Column(String(10), default=True)
    vehicleId.server_default = None
