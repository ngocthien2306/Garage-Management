from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from core.database.connectionmssql import Base

class Track(Base):
    __tablename__ = "tblTrack"
    trackId = Column(Integer, primary_key=True, index=True)
    vehicleId = Column(Integer)
    startTime = Column(DateTime)
    endTime = Column(DateTime, default=False)
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
    detectPathPlate =Column(String(100), default=False)
class VehicleExtend(Base):
    __tablename__ = "tblVehicleExtend"
    vehicleId = Column(Integer, primary_key=True, index=True)
    status =Column(String(10), default=True)
    typeTransport = Column(String(10), default=True)
    typePlate = Column(String(10), default=True)
