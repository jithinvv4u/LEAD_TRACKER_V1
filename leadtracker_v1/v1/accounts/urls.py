"""URLs of the app accounts."""

from django.urls import path

from .views import user as user_views
from .views import auth as auth_views

urlpatterns = [
    # Auth views
    path("validate/username/", auth_views.ValidateUsername.as_view()),
    path("validate/password/", auth_views.ValidatePassword.as_view()),
    path("validator/", auth_views.ManageValidator.as_view()),
    path("password/forgot/", auth_views.ResetPassword.as_view()),
    path("password/set/", auth_views.SetPassword.as_view()),
    path("device/", auth_views.CreateUserDevice.as_view()),
    path("signup/", auth_views.Signup.as_view()),
    path("login/", auth_views.Login.as_view()),
    path("login/magic/", auth_views.MagicLogin.as_view()),
    path("magic/generate/", auth_views.MagicLink.as_view()),
    path("logout/", auth_views.Logout.as_view()),
    path("verify-email/resend/", auth_views.VerificationEmail.as_view()),
    # User Views
    path("user/search/", user_views.UserList.as_view()),
    path("user/<idencode:pk>/", user_views.UserDetails.as_view()),
    path("user/", user_views.UserDetails.as_view()),
    path("terms/", user_views.TermsAndConditionsDetails.as_view()),
]
