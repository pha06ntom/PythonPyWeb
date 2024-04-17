from django.urls import path
from .views import AuthorAPIView
from .views import AuthorGenericAPIView

urlpatterns = [
    path('authors/', AuthorAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorAPIView.as_view(), name='author-detail'),
    path('authors_generic/', AuthorGenericAPIView.as_view(), name='author-generic-list'),
    path('authors_generic/<int:pk>/', AuthorGenericAPIView.as_view(), name='author-generic-detail'),
]

