from django.urls import path
from .views import AdvertisementList, Ad, AdCreate, AdUpdate, AdDelete, like_ad, dislike_ad, approve_comment,\
    CommentList, reject_comment, create_comment

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<int:pk>', Ad.as_view(), name='Ad'),
    path('create', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('<int:pk>/ad_like/', like_ad, name='like_ad'),
    path('<int:pk>/ad_dislike/', dislike_ad, name='dislike_ad'),
    path('<comment', CommentList.as_view(), name='comment_list'),
    path('<int:pk>/approve/', approve_comment, name='approve_comment'),
    path('<int:pk>/reject/', reject_comment, name='reject_comment'),
    path('ad/<int:pk>/create_comment/', create_comment, name='create_comment'),
]
