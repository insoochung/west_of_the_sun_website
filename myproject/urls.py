"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, re_path
from django.contrib import admin # ,include (Corey Schafer Tutorial Recommendation)
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from books import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('about/company/', views.about_company, name='about_company'),    
    path('book_detail/<int:id>', views.book_detail, name='book_detail'), # For rendering book views (according to original tutorials)

    # Cory Schafer Tutorial Recommendation (For later versions of Django): path('books/', include('book.urls'))
    # According to Cory Schafer: If you use an "include" function here like above, you do not need to add anything to the project URLs module
    # Because once someone goes to a specific book route, the "include" function will chop off the part already matched and process the next string (has to create an additional book.url file)

    
    # re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),

    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

]
