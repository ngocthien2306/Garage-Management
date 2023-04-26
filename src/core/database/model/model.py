from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from core.database.connectionmssql import Base

class Track(Base):
    __tablename__ = "tblTrackNew"
    trackId = Column(Integer, primary_key=True, index=True)
    vehicleId = Column(Integer, ForeignKey('tblVehicleNew.id'))
    driverId = Column(Integer)
    startTime = Column(String(20))
    endTime = Column(String(20), default=False)
    fee = Column(String(20), default=False)
    siteId= Column(Integer, default=False)
    locationX = Column(String(20), default=False)
    locationY = Column(String(20), default=False)
    vehicle = relationship("Vehicle", back_populates="tracks")
    #items = relationship("Item", back_populates="owner")
class Vehicle(Base):
    __tablename__ = "tblVehicleNew"
    id = Column(Integer, primary_key=True, index=True)
    plateNum =Column(String(20), default=True)
    status =Column(String(10), default=True)
    typeTransport = Column(String(10), default=True)
    typePlate = Column(String(10), default=True)
    tracks = relationship("Track", back_populates="vehicle") # tạo quan hệ
class Guest(Base):
    __tablename__ = "tblGuestNew"
    driverId = Column(Integer, primary_key=True, index=True)
    originPathFace =Column(String(100), default=True)
    detectPathFace =Column(String(100), default=False)
    status = Column(String(10), default=True)

class VehicleExtend(Base):
    __tablename__ = "tblVehicleExtend"
    #vehicle_id = Column(ForeignKey("tblVehicle.id"))
    VehicleExtendId = Column(Integer, primary_key=True)
    vehicleId = Column(Integer)
    status =Column(String(10), default=True)
    typeTransport = Column(String(10), default=True)
    typePlate = Column(String(10), default=True)
    vehicleId.server_default = None
