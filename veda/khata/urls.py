
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView, heroimg,openbankaccount,deposite,ApplyLoan,newbankaccdetail,newdeposite,LendLoan,heroImages,ResetPasswordView,GeneratedOtpView,VerifyOTPView,ForgotPasswordView,VerifyAccountView
from . import views

urlpatterns = [
  path('register/',RegisterView.as_view(),name="register"),
  path('login/',LoginView.as_view(),name="login"),
  path('user/',UserView.as_view(),name="user"),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('openacc/',openbankaccount.as_view(),name="openacount"),
  path('deposit/',deposite.as_view(),name="Deposite"),
  path('loan/',ApplyLoan.as_view(),name="Apply Loan"),
  path('bankaccount/',newbankaccdetail.as_view(),name="New bank acc details"),
  path('depositer/',newdeposite.as_view(),name="New Depositer"),
  path('loanapply/',LendLoan.as_view(),name="Apply for loan"),
  path('getimp/',heroimg.as_view(),name="Hero Images"),
  path('upload/',views.uploadimg,name="Uplaod Images"),
  path('delete/<int:pk>/',views.deleteimg,name="Delete img"),
  path('auth/users/reset_password/',ResetPasswordView.as_view()),
  path('generateotp/',GeneratedOtpView.as_view()),
  path('verifyotp/',VerifyOTPView.as_view()),
  path('forgotpassword/',ForgotPasswordView.as_view()),
  path('verify/<uuid:token>/', VerifyAccountView.as_view(), name='verify_account'),
]
