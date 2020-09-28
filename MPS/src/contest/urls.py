"""contest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from .views import (
    contest_post_create_view,
    contest_post_delete_view,
    contest_post_detail_view,
    contest_post_list_view,
    contest_post_update_view,
    team_list_post_view,
    team_crud_post_view,
    team_post_detail_view,
    team_post_delete_view,
    category_crud_post_view,
    category_post_list_view,
    member_list_view,
    member_crud_view,
    contest_start_view,
    round_list_view,
    round_detail_view,
    grade_crud_view,
    grade_round_list_view,
    elimination_button,
    winner_button,
    logout_request,
)


urlpatterns = [
	path('', contest_post_list_view),
    path('admin/', admin.site.urls),
    path('logout/', logout_request),
# ============================================== Contest =================================================

    path('contest-list/', contest_post_list_view),
    path('contest-new/', contest_post_create_view),

    path('contest/<str:slug>/', contest_post_detail_view),
    path('contest/<str:slug>/update/', contest_post_update_view),
    path('contest/<str:slug>/delete/', contest_post_delete_view),
    path('contest/<str:slug>/start/', contest_start_view),

# ============================================== Category ==============================================

    path('contest/<str:slug>/category-new/', category_crud_post_view),
    path('contest/<str:slug>/category-list/', category_post_list_view),

# ============================================== Team ==================================================
    
    path('contest/<str:slug>/team-list/', team_list_post_view),
    path('contest/<str:slug>/team-new/', team_crud_post_view),
    path('contest/<str:slug>/team/<int:pk>/', team_post_detail_view),
    path('contest/<str:slug>/team/<int:pk>/delete/', team_post_delete_view),

# ============================================== Member ==================================================

    path('contest/<str:slug>/team/<int:pk>/member-list/', member_list_view),
    path('contest/<str:slug>/team/<int:pk>/member-new/', member_crud_view),

# ==============================================  Round ===================================================

    path('contest/<str:slug>/round-list/', round_list_view),
    path('contest/<str:slug>/round/<int:no>/', round_detail_view),
    # TODO integrate series if needed then check the grading view
    # path('contest/<str:slug>/round-list/', round_list_view),

# ==============================================  Grade ===================================================

    path('contest/<str:slug>/round/<int:no>/team/<int:pk>/', grade_crud_view),
    path('contest/<str:slug>/round/<int:no>/grades', grade_round_list_view),
    path('contest/<str:slug>/magic', elimination_button),
    path('contest/<str:slug>/winner', winner_button),
    
# ==============================================  ?? ===================================================

]
