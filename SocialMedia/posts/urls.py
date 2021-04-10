from django.urls import path, re_path
from .views import all_posts, post_detail, new_post, post_delete, post_edit, add_comment, add_reply, like_post

app_name = 'posts'
urlpatterns = [
    re_path(r'(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/(?P<slug>[-\w]+)/', post_detail, name='post_detail'),
    path('', all_posts, name='all_posts'),
    path('new/<int:user_id>/', new_post, name='new_post'),
    path('post_delete/<int:user_id>/<int:post_id>/', post_delete, name='post_delete'),
    path('post_edit/<int:user_id>/<int:post_id>/', post_edit, name='post_edit'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('add_reply/<int:post_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('like/', like_post, name='like_post')
]
