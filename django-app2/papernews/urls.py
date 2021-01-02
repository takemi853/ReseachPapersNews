from django.contrib import admin
from django.urls import path,include
from .views import PnList,PnDetail,PnCreate,PnDelete,PnTest
# from .views import PnList,PnDetail,PnCreate,PnDelete,PnUpdate

urlpatterns = [
    path('', PnList.as_view(),name='list'),
    path('detail/<int:pk>',PnDetail.as_view(),name='detail'),
    path('create/',PnCreate.as_view(),name='create'),
    path('delete/<int:pk>',PnDelete.as_view(),name='delete'),
    path('test/',PnTest.as_view(),name='test')
    # path('update/<int:pk>',PnUpdate.as_view(),name='update'),
]