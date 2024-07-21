from home.views import person, login, PersonApi, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')

urlpatterns = [
    path('person/', person),
    # path('login/', login),
    path('persons/', PersonApi.as_view()),
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view())
]