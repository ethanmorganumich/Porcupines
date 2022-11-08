from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', views.notes, name='notes'),
    path('notes/<str:note_id>', views.notes_update),
]