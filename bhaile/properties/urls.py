from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchResultListView,
    BookingListView,
    BookingDetailView,
    BookingUpdateView,
    BookingDeleteView,

)

urlpatterns = [
    # to access the home page from views
    # url path mapped to home function in views
    path('', PostListView.as_view(), name='properties-home'),
    path('bookings/', BookingListView.as_view(template_name='properties/bookings.html'), name='booking'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/update', BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete', BookingDeleteView.as_view(), name='booking-delete'),
    #
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    # detail view for the properties
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<category>/', PostDetailView.as_view(), name='post-detail'),
    # shares template with update view
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='properties-about'),
    path('search/', SearchResultListView.as_view(), name='properties-search'),
]
