from django.urls import path

from . import views

app_name = 'bazar'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('eventdetail/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('eventcreate', views.CreateEventView.as_view(), name='event_create'),
    path('event/<int:event_id>/add-item/', views.AddItemView.as_view(), name='add_item'),
    path('reserveditems/', views.ReservedItemsView.as_view(), name='reserved_items'),
    path('reserveitems/<int:item_id>/', views.ReserveItemsView.as_view(), name='reserve_items'),
]