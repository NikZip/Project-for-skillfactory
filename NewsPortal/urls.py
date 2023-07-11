from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
   path('', cache_page(5)(NewsList.as_view()), name='posts_list'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),

   path('search', NewsSearch.as_view(), name='posts_search'),

   path('<str:post_type>/create', PostCreate.as_view(), name='post_create', ),
   path('<str:post_type>/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('<str:post_type>/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

   path('upgrade/', make_author, name='upgrade'),
   path('profile/', ProfileView.as_view(), name='user_profile'),

   path('subscribe/<int:pk>/', subscribe, name='subscribe'),
   path('unsubscribe/<int:pk>/', unsubscribe, name='unsubscribe'),

   # debugging
   path('debug/', DebugView.as_view(), name='debug'),
   path('debug/sub', debug_send_sub_email, name='debug_sub'),
   path('debug/welcome', debug_send_welcome_notification, name='debug_welcome'),
   path('debug/weekly',debug_send_best_weekly_posts, name='debug_send_weekly'),
]
