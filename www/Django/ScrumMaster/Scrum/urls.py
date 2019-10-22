from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

app_name = "Scrum"

def_router = DefaultRouter()
def_router.register('scrumusers', views.ScrumUserViewSet)
def_router.register('scrumgoals', views.ScrumGoalViewSet)
def_router.register('scrumprojects', views.ScrumProjectViewSet)
def_router.register('scrumprojectroles', views.ScrumProjectRoleViewSet)
def_router.register(r'scrumsprint', views.SprintViewSet, base_name='scrumsprint')

'''
    path('create-user/', views.create_user, name="create_user"),
    path('init-user/', views.init_user, name="init_user"),
    path('scrum-login/', views.scrum_login, name="scrum_login"),
    path('profile/', views.profile, name="profile"),
    path('scrum-logout/', views.scrum_logout, name="scrum_logout"),
    path('add-goal/', views.add_goal, name="add_goal"),
    path('remove-goal/<int:goal_id>/', views.remove_goal, name="remove_goal"),
    path('move-goal/<int:goal_id>/<int:to_id>/', views.move_goal, name="move_goal"),
'''
    
urlpatterns = [
    url(r'api/', include(def_router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    path(r'create-demo/', views.createDemoUser)
]