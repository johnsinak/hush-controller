from django.urls import path
from assignments import views

app_name = "assignments"
urlpatterns = [
    path("getnew", views.AssignmentView.as_view(), name="assignment"),
    path("postupdate", views.ProxyUpdateView.as_view(), name="postupdate")
]
