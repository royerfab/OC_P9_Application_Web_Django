"""
URL configuration for LITRevu project.

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
from django.contrib import admin
from django.urls import path, include, re_path
import authentication.views
import critical.views
from django.views.static import serve
from LITRevu import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path('', authentication.views.login_page, name='login'),
    path('home/', critical.views.home, name='home'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('register/', authentication.views.sign_up, name='register'),
    path('follow/', critical.views.follow, name='follow'),
    path('add_ticket/', critical.views.add_ticket, name='add-ticket'),
    path('<int:ticket_id>/add_review/', critical.views.add_review, name='add-review'),
    path('add_ticket_and_review/', critical.views.add_ticket_and_review, name='add-ticket-and-review'),
    path('posts/', critical.views.ticket_list, name='posts'),
    path('<int:id>/update_ticket/', critical.views.update_ticket, name='update-ticket'),
    path('<int:id>/update_review/', critical.views.update_review, name='update-review'),
    path('<int:id>/delete_ticket/', critical.views.delete_ticket, name='delete-ticket'),
    path('<int:id>/delete_review/', critical.views.delete_review, name='delete-review'),
]

