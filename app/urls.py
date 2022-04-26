from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('operations/', views.operations, name='operations'),
    path('proof/', views.proof, name='proof'),
    path('/employee', views.employee, name='employee'),
    path('/department', views.department, name='department'),
    path('/position', views.position, name='position'),
    path('/discount', views.discount, name='discount'),
    path('/client', views.client, name='client'),
    path('/service', views.service, name='service'),
    path('/service/<int:pk>', views.service_doc, name='service-doc'),
    path('/appoinments', views.appoinments, name='appoinments'),
    path('/operation/add', views.add_operation, name='add_operation'),
    path('/employee/add', views.add_employee, name='add-employee'),
    path('/department/add', views.add_department, name='add-department'),
    path('/position/add', views.add_position, name='add-position'),
    path('/discount/add', views.add_discount, name='add-discount'),
    path('/client/add', views.add_client, name='add-client'),
    path('/service/add', views.add_service, name='add-service'),
    path('employee/update/<int:emp_id>', views.update_employee),
    path('department/update/<int:id>', views.update_department),
    path('position/update/<int:id>', views.update_position),
    path('discount/update/<int:id>', views.update_discount),
    path('client/update/<int:id>', views.update_client),
    path('service/update/<int:id>', views.update_service),

    path('employee/delete/<int:emp_id>', views.delete_employee),
    path('department/delete/<int:id>', views.delete_department),
    path('position/delete/<int:id>', views.delete_position),
    path('discount/delete/<int:id>', views.delete_discount),
    path('client/delete/<int:id>', views.delete_client, name='client-delete'),
    path('service/delete/<int:id>', views.delete_service),
    path('appoinments/delete/<int:id>', views.delete_app),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
