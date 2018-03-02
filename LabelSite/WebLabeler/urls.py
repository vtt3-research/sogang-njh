from django.conf.urls import url
from django.contrib import admin

from WebLabeler import views
from WebLabeler import uploader

urlpatterns = [
    url(r'^test/', views.test, name='test'),


    # login logout
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),

    # media list
    url(r'^list/page/(?P<media_page>\d+)/$', views.list_page, name='list_page'),

    # media browse
    url(r'^view/(?P<media_id>\d+)/$', views.browse_media, name='media_browse'),

    # media labeling
    url(r'^edit/sbd_manual/(?P<media_id>\d+)/$', views.edit_media_sbd_manual, name='media_sbd_manual'),
    url(r'^edit/sbd_manual/addshots/$', views.edit_media_sbd_add_shots, name='media_sbd_add_shots'),
    url(r'^edit/person/(?P<media_id>\d+)/$', views.edit_media_person, name='media_edit_person'),
    url(r'^edit/person/(?P<media_id>\d+)/shot/(?P<shot_num>\d+)/$', views.edit_media_person_page, name='media_edit_person_page'),

    # media upload
    url(r'^upload/$', uploader.MediaCreateView.as_view(), name='upload'),
    url(r'^upload/view/$', uploader.MediaListView.as_view(), name='upload_view'),
    url(r'^upload/delete/(?P<pk>\d+)$', uploader.MediaDeleteView.as_view(), name='upload-delete'),

    # utility
    url(r'^utils/image/$', views.util_image_ajax, name='util_media_image'),

    url(r'^', views.front, name='front'),
]