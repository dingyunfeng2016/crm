from django.conf.urls import url, include
from django.contrib import admin

from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^test/$', views.test),
    url(r'^book', views.book),
    url(r'^reg', views.reg),
    url(r'^logout/$', views.logout),

    url(r'^customers/$', views.CustomersView.as_view(), name='all_customers'),
    url(r'^my_customers/$', views.CustomersView.as_view(), name='my_customers'),
    url(r'^add_customer/$', views.AddAndEditCustomersView.as_view(), name='add_ustomer'),
    url(r'^add_consult_record/$', views.AddAndEditConsultRecordView.as_view(), name='add_consult_record'),
    url(r'^edit_customer/(\d+)$', views.AddAndEditCustomersView.as_view(), name='edit_customers'),
    url(r'^edit_consult_record/(\d+)$', views.AddAndEditConsultRecordView.as_view(), name='edit_consult_record'),
    url(r'^add_edit_customer/(\d+)$', views.AddAndEditCustomersView.as_view(), name='add_edit_customer'),

    url(r'^public_customers/$', views.CustomersView.as_view(), name='public_customers'),

    url(r'^consult_record/$', views.ConsultRecordView.as_view(), name='consult_record'),

    url(r'^class_record/$', views.class_record),
    url(r'^study_record/$', views.study_record),
    url(r'^stuff_management/$', views.stuff_management),
    url(r'^class_study_record_list/$', views.class_study_record_list),
    url(r'^all_student_study_record_list/$', views.all_student_study_record_list),
    url(r'^record_score/(\d+)', views.RecordScoreView.as_view(), name='record_score'),
    url(r'^tongji', views.TongJiView.as_view(), name='tongji'),
    # url(r'^room/', include('app02_room_boooking.urls')),


]