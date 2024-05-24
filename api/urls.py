from django.urls import path
from . import views




urlpatterns = [
path('products/<int:pk>', views.ProductsOperations.as_view()),
path('products/', views.ProductsOperations.as_view()),
path('stocks/<int:pk>', views.StockOperations.as_view()),
path('stocks/', views.StockOperations.as_view()),
path('stocksedited/<int:pk>', views.StockUpdatedHandles.as_view()),
path('stocksedited/', views.StockUpdatedHandles.as_view()),
path('salesrecord/<int:pk>', views.SalesOperations.as_view()),
path('salesrecord/', views.SalesOperations.as_view()),
path('expense/<int:pk>', views.ExpensesOperations.as_view()),
path('expense/', views.ExpensesOperations.as_view()),
]