from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreate, PostUpdate, PostDelete


urlpatterns = [
   path('', NewsList.as_view(), name='posts_list'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),

   path('search', NewsSearch.as_view(), name='posts_search'),

   path('<str:post_type>/create', PostCreate.as_view(), name='post_create', ),
   path('<str:post_type>/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('<str:post_type>/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

]