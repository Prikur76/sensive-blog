from django.contrib import admin
from blog import views
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from blog import views as blog_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/<int:page>', views.index, name='index'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_title>', views.tag_filter, name='tag_filter'),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
