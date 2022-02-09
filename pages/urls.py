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
                  path('<str:lang>/', views.start, name='frontend-start-lang'),
                  path('start', views.start, name='frontend-start'),
                  path('home', views.home, name='frontend-home'),
                  path('dashboard', views.dashboard, name='backend-dashboard'),
                  path('pair/<str:pk>/', views.pair, name='backend-pair'),
                  path('rankings', views.rankings, name='backend-rankings'),
                  path('create_pair', views.create_pair, name='backend-create_pair'),
                  path('update_pair/<str:pk>/', views.update_pair, name='backend-update_pair'),
                  path('preview_pair/<str:pk>/', views.preview_pair, name='backend-preview_pair'),
                  path('delete_pair/<str:pk>/', views.delete_pair, name='backend-delete_pair'),
                  path('options', views.options, name='backend-options'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if DEBUG:
#     urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
#     urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)
