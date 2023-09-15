
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,openbankaccount,deposite,ApplyLoan

urlpatterns = [
  path('register/',RegisterView.as_view(),name="register"),
  path('login/',LoginView.as_view(),name="login"),
  path('user/',UserView.as_view(),name="user"),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('openacc/',openbankaccount.as_view(),name="openacount"),
  path('deposit/',deposite.as_view(),name="Deposite"),
  path('loan/',ApplyLoan.as_view(),name="Apply Loan"),
]
