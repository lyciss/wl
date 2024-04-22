from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import *
from . import appbuilder, db
from flask import render_template
from flask import request, session, current_app, g, jsonify,redirect
from flask_appbuilder import BaseView, expose
from flask_appbuilder.actions import action
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import redirect
import flask_excel as excel
import pandas as pd
from flask import make_response
import time
class MyModelView(ModelView):
    datamodel = SQLAInterface(MyModel)
    list_columns = ['id', 'name']
    @expose("/index", methods=["GET"])
    def index(self):
        # 获取会话
        session = db.session  # db = SQLA(app)
        #m_obj = session.query(MyModel).filter_by(id=1).one_or_none() # all()获取所有对象
        m_obj = session.query(MyModel).all() # all()获取所有对象
        print("result:", len(m_obj), type(m_obj))
        return jsonify({
            "status": 200,
            "id": m_obj[0].id,
            "name": m_obj[0].name
        })
    @action(
        "myaction", "Do something on this record", "Do you really want to?", "fa-rocket"
    )
    
    def myaction(self, items):
        if isinstance(items, list):
            print(len(items))
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        
        data = {'Column1': [1, 2, 3], 'Column2': [4, 5, 6]}
        df = pd.DataFrame(data)

        # 将数据集转换为 xls 文件
        file_name = time.strftime('%Y%m%d', time.localtime(time.time())) + '.xlsx'
        df.to_excel(file_name, index=False)

        # 读取 xls 文件并将其作为响应返回
        with open(file_name, 'rb') as f:
            content = f.read()

        response = make_response(content)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename={file_name}'

        return response
        



        
        return redirect(self.get_redirect())

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())
    
#appbuilder.add_view( MyModelView,  "MyModel",  icon="fa-folder-open-o", category="MyModel",  category_icon='fa-envelope' )





# 车主信息视图
class CarOwnerModelView(ModelView):
    datamodel = SQLAInterface(CarOwner)
    label_columns = {'name':'姓名','gender':"性别",'birth_date':'出生日期','phone':'电话号码', 'address':'地址', 'id_card':'电话号码', 'bank_account':'银行账户', 'photo':'照片'}
    list_columns = ['name', 'gender', 'birth_date', 'phone', 'address', 'id_card', 'bank_account', 'photo']
    
# 车辆类型视图
class VehicleTypeModelView(ModelView):
    datamodel = SQLAInterface(VehicleType)
    label_columns = {'type':'车辆类型'}
    list_columns = ['type']
    

# 集装箱视图
class ContainerModelView(ModelView):
    datamodel = SQLAInterface(Container)
    label_columns = {'number':'集装箱号码'}
    list_columns = ['number']
    
# 车辆信息视图
class VehicleModelView(ModelView):
    datamodel = SQLAInterface(Vehicle)

    label_columns = {'vehicle_type.type':'车辆类型','owner.name':"所有人",
                     'license_plate':'车牌号码','transport_certificate_number':'道路运输证号码', 
                     'brand_model':'厂牌型号', 'load_capacity':'载重', 
                     'purchase_date':'购买日期', 'photo':'照片','national_transport_certificate_number':'国际运输证号'}


    list_columns = ['vehicle_type.type', 'owner.name', 
                    'license_plate', 'transport_certificate_number', 
                    'brand_model', 'load_capacity', 
                    'purchase_date', 'photo', 'national_transport_certificate_number']
    
    
# 单位信息视图
class CompanyModelView(ModelView):
    datamodel = SQLAInterface(Company)
    label_columns = {'name':'姓名','legal_representative':"法人代表", 'address':'地址', 'bank':'开户行', 'bank_account':'银行账户'}
    list_columns = ['name', 'legal_representative', 'address', 'bank', 'bank_account']
    

# 货物信息视图
class GoodsModelView(ModelView):
    datamodel = SQLAInterface(Goods)
    label_columns = {'name':'货物名称'}
    list_columns = ['name']
    

# 物流信息视图
class LogisticsModelView(ModelView):
    datamodel = SQLAInterface(Logistics)

    label_columns = {'license_plate':'车牌号码',
                     'goods.name':'货物', 'gross_weight':'毛重kg', 
                    'tare_weight':'皮重kg', 'net_weight':'净重kg', 'date':'打印日期','time':'打印时间', 
                    'shipping.name':'发货单位', 'receiving.name':'收货单位', 'customs.name':'报关单位', 
                    'serial_number':'流水号', 'waybill_photo':'底单照片'
                     }

    list_columns = ['license_plate', 
                    'goods.name', 'gross_weight', 
                    'tare_weight', 'net_weight', 'date','time', 
                    'shipping.name', 'receiving.name', 'customs.name', 
                    'serial_number', 'waybill_photo'
                    ]
    
    show_template = 'appbuilder/general/model/show_cascade.html'
    @expose("/index", methods=["GET"])
    def index(self):
        # 获取会话
        session = db.session  # db = SQLA(app)
        #m_obj = session.query(MyModel).filter_by(id=1).one_or_none() # all()获取所有对象
        m_obj = session.query(MyModel).all() # all()获取所有对象
        print("result:", len(m_obj), type(m_obj))
        return jsonify({
            "status": 200,
            "id": m_obj[0].id,
            "name": m_obj[0].name
        })
    @action(
        "导出", "导出xlsx文件", None, "fa-file-excel"
    )
    
    def myaction(self, items):


        if isinstance(items, list):
            print(len(items))
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        df = pd.DataFrame()


        

        for item in items:
            
            
            new_row = {'车牌': [str(item.license_plate)],
                       '所有者': [str(item.vehicle.owner)],
                                    '货物': [str(item.goods_name)],
                                    '发货单位': [str(item.shipping_company)],
                                    '接收单位': [str(item.receiving_company)],
                                   '报关单位': [str(item.customs_company)],
                                   '集装箱号': [str(item.containers)],
                                   '毛重(KG)': [str(item.tare_weight)],
                                   '皮重(KG)': [str(item.net_weight)],
                                   '净重': [str(item.net_weight)],
                                   '打印日期': [str(item.date)],
                                   '打印时间': [str(item.time)],
                                   '流水号': [str(item.serial_number)]
            }

        
        


        #df = df.append(new_row, ignore_index=True)
        df = pd.concat([df ,pd.DataFrame(new_row)])

        # 将数据集转换为 xls 文件
        file_name = 'output.xlsx'
        df.to_excel(file_name, index=False)

        # 读取 xls 文件并将其作为响应返回
        with open(file_name, 'rb') as f:
            content = f.read()

        response = make_response(content)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename={file_name}'

        

        return response
        


        #return redirect(self.get_redirect())

    @action("muldelete", "Delete", "Delete all Really?", "fa-delete-left")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

# 添加到菜单
appbuilder.add_view(CarOwnerModelView, "车主信息", icon="fa-address-card", category="基本信息维护")
appbuilder.add_view(VehicleTypeModelView, "车辆类型", icon="fa-car", category="基本信息维护")
appbuilder.add_view(ContainerModelView, "集装箱", icon="fa-cube", category="基本信息维护")
appbuilder.add_view(VehicleModelView, "车辆信息", icon="fa-truck", category="基本信息维护")
appbuilder.add_view(CompanyModelView, "单位信息", icon="fa-building", category="基本信息维护")
appbuilder.add_view(GoodsModelView, "货物信息", icon="fa-box", category="基本信息维护")
appbuilder.add_view(LogisticsModelView, "物流信息", icon="fa-shipping-fast", category="物流管理与统计")



@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )




from .models import Employee,Department, Function, Benefit
from app import appbuilder,app


class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)
    list_columns = ['full_name', 'department', 'employee_number']

    show_template = 'appbuilder/general/model/show_cascade.html'
    @expose("/index", methods=["GET"])
    def index(self):
        # 获取会话
        session = db.session  # db = SQLA(app)
        #m_obj = session.query(MyModel).filter_by(id=1).one_or_none() # all()获取所有对象
        m_obj = session.query(MyModel).all() # all()获取所有对象
        print("result:", len(m_obj), type(m_obj))
        return jsonify({
            "status": 200,
            "id": m_obj[0].id,
            "name": m_obj[0].name
        })
    @action(
        "myaction", "Do something on this record", "Do you really want to?", "fa-rocket"
    )
    
    def myaction(self, items):
        if isinstance(items, list):
            print(len(items))
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())


class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]


class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [EmployeeView]

class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    related_views = [EmployeeView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']


# appbuilder.add_view(EmployeeView, "Employees", icon="fa-folder-open-o", category="Company")
# appbuilder.add_separator("Company")
# appbuilder.add_view(DepartmentView, "Departments", icon="fa-folder-open-o", category="Company")
# appbuilder.add_view(FunctionView, "Functions", icon="fa-folder-open-o", category="Company")
# appbuilder.add_view(BenefitView, "Benefits", icon="fa-folder-open-o", category="Company")


class EmployeeHistoryView(ModelView):
    datamodel = SQLAInterface(EmployeeHistory)
    list_columns = ['department', 'begin_date', 'end_date']




# appbuilder.add_view(EmployeeHistoryView, "EmployeeHistoryView", icon="fa-folder-open-o", category="Company")

db.create_all()

excel.init_excel(app)
