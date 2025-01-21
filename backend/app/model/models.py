from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from .config import Base


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_location = Column(String(255), nullable=False)
    address_location = Column(String(255), nullable=False)

class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_camera = Column(String(255), nullable=False)
    type_camera = Column(String(255), nullable=False)
  
    location = relationship('Location', back_populates='camera', uselist=False)  
    status = Column(Enum('ON', 'OFF'), nullable=True)
    ip_address = Column(String(255), nullable=False)
    id_location = Column(Integer, ForeignKey('location.id'), nullable=True)

    location_ref = relationship('Location', back_populates='camera')
    recordings = relationship('Recording', back_populates='camera')

class Recording(Base):
    __tablename__ = 'recording'
    id = Column(Integer, primary_key=True, autoincrement=True)
    encode_type = Column(Enum('SHA-256'), nullable=True)
    status = Column(Enum('Success', 'Failed'), nullable=True)
    id_camera = Column(Integer, ForeignKey('camera.id'), nullable=True)

    camera = relationship('Camera', back_populates='recording')

class CameraConfiguration(Base):
    __tablename__ = 'camera_configuration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    ip = Column(String(255), nullable=True)
    line_point_left = Column(JSON, nullable=False)
    line_point_right = Column(JSON, nullable=False)
    id_camera = Column(Integer, ForeignKey('camera.id'), nullable=True)

    camera = relationship('Camera', back_populates='configurations')
