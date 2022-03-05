from django.urls import path
from pages import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path("", auth_views.LoginView.as_view(template_name="registration/login.html"),
                       name='registration-login'),
                  path("logout/", auth_views.LogoutView.as_view(), name='registration-logout'),
                  # path('<str:lang>/', views.start, name='frontend-start-lang'),
                  path('start', views.start, name='frontend-start'),
                  path('home', views.home, name='frontend-home'),
                  path('brake', views.brake, name='frontend-brake'),
                  path('section', views.section, name='backend-section'),
                  path('dashboard', views.dashboard, name='backend-dashboard'),
                  path('details/<str:pk>/', views.details, name='backend-details'),
                  # path('rankings', views.rankings, name='backend-rankings'),
                  path('create', views.create, name='backend-create'),
                  path('update/<str:pk>/', views.update, name='backend-update'),
                  path('preview/<str:pk>/', views.preview, name='backend-preview'),
                  path('delete/<str:pk>/', views.delete, name='backend-delete'),
                  path('options', views.options, name='backend-options'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if DEBUG:
#     urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
#     urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)
