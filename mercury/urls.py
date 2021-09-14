"""mercury URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from mercuryapi.views.product import ProductView
from mercuryapi.models.employeeSchedule import EmployeeSchedule
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from mercuryapi.views import register_user, login_user
from mercuryapi.views import MonthlyFinanceView, EmployeeView, EmployeeScheduleView, ProductView
from mercuryapi.views.employee import EmployeeView



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'monthlyfinances', MonthlyFinanceView, 'monthlyfinance')
router.register(r'employees', EmployeeView, 'employee')
router.register(r'employeeSchedules', EmployeeScheduleView, 'employeeschedule')
router.register(r'products', ProductView, 'product')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
