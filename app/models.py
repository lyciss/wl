from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Date,Time,DateTime, Table
from sqlalchemy.orm import relationship
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from datetime import datetime
# 定义车主信息表
import datetime
class MyModel(Model):
# 表名
    __tablename__ = "my_model_t"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # print info when print this obj
    def __repr__(self):
        return self.name




class CarOwner(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    gender = Column(String(10), unique=True, nullable=False)
    birth_date = Column(Date)
    phone = Column(String(50))
    address = Column(String(255))
    id_card = Column(String(50))
    bank_account = Column(String(100))
    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))
    def __repr__(self):
        return self.name

# 定义车辆类型表
class VehicleType(Model):
    id = Column(Integer, primary_key=True)
    type = Column(String(50), unique=True, nullable=False)
    def __repr__(self):
        return self.type

# 定义集装箱表
class Container(Model):
    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True, nullable=False)
    def __repr__(self):
        return self.number

# 定义车辆信息表
class Vehicle(Model):
    id = Column(Integer, primary_key=True)
    vehicle_type_id = Column(Integer, ForeignKey('vehicle_type.id'), nullable=False)
    owner_name = Column(String(150), ForeignKey('car_owner.name'), nullable=False)
    license_plate = Column(String(50), unique=True, nullable=False)
    transport_certificate_number = Column(String(50), unique=True, nullable=False)
    brand_model = Column(String(100), unique=True, nullable=False)
    load_capacity = Column(Integer, unique=True, nullable=False)
    purchase_date = Column(Date)
    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))
    national_transport_certificate_number = Column(String(50))
    vehicle_type = relationship("VehicleType")
    owner = relationship("CarOwner")
    def __repr__(self):
        return self.license_plate

# 定义单位信息表
class Company(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    legal_representative = Column(String(150))
    address = Column(String(255))
    bank = Column(String(100))
    bank_account = Column(String(100))
    def __repr__(self):
        return self.name

# 定义货物信息表
class Goods(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name

# 定义物流信息表
# 创建一个关联表来定义物流信息和集装箱之间的多对多关系
logistics_container_association_table = Table('logistics_container_association', Model.metadata,
    Column('logistics_id', Integer, ForeignKey('logistics.id'), primary_key=True),
    Column('container_id', Integer, ForeignKey('container.id'), primary_key=True)
)

# 修改物流信息表，添加多对多关系
class Logistics(Model):
    id = Column(Integer, primary_key=True)
    license_plate = Column(String(50), ForeignKey('vehicle.license_plate'), nullable=False)
    goods_name = Column(String(150), ForeignKey('goods.name'), nullable=False)
    gross_weight = Column(Integer, unique=False, nullable=False)
    tare_weight = Column(Integer, unique=False, nullable=False)
    net_weight = Column(Integer, unique=False, nullable=False)
    date = Column(Date,unique=False, nullable=False)
    time = Column(String(9),default='00:00:00',unique=False, nullable=False)
    
    shipping_company = Column(String(150), ForeignKey('company.name'),unique=False, nullable=False)
    receiving_company = Column(String(150), ForeignKey('company.name'),unique=False, nullable=False)
    customs_company = Column(String(150), ForeignKey('company.name'),unique=False, nullable=False)
    container_number = Column(String(50), ForeignKey('container.number'),unique=False, nullable=False)
    serial_number = Column(String(50), unique=True, nullable=False)
    waybill_photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))
    vehicle = relationship("Vehicle")
    goods = relationship("Goods")
    shipping = relationship("Company", foreign_keys=[shipping_company])
    receiving = relationship("Company", foreign_keys=[receiving_company])
    customs = relationship("Company", foreign_keys=[customs_company])
    containers = relationship('Container', secondary=logistics_container_association_table, backref='logistics')
    def __repr__(self):
        return self.serial_number




class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

class Benefit(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_benefits_employee = Table('benefits_employee', Model.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('benefit_id', Integer, ForeignKey('benefit.id')),
                                      Column('employee_id', Integer, ForeignKey('employee.id'))
)


class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    address = Column(String(250), nullable=False)
    fiscal_number = Column(Integer, nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=False)
    function = relationship("Function")
    benefits = relationship('Benefit', secondary=assoc_benefits_employee, backref='employee')

    begin_date = Column(Date, default=today, nullable=False)
    end_date = Column(Date, nullable=True)

    def __repr__(self):
        return self.full_name
    
class EmployeeHistory(Model):
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee")
    begin_date = Column(Date, default=today)
    end_date = Column(Date)
