"""OAPC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from OAPC_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    ######## LOGIN & REGISTER START ###########
    url(r'^$', display_login),
    url(r'^show_register', show_register, name="show_register"),
    url(r'^register', register, name="register"),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^check_login', check_login, name="check_login"),
    ########### LOGIN & REGISTER END ############

    # ADMIN START
    url(r'^a_home_admin', a_home_admin, name="a_home_admin"),
    url(r'^c_view_users_admin', c_view_users_admin, name="c_view_users_admin"),
    url(r'^users', users, name="users"),
    url(r'^delete', delete, name="delete"),
    url(r'^m_add_subjects_admin',m_add_subjects_admin,name="m_add_subjects_admin"),
    url(r'^add_subjects',add_subjects,name="add_subjects"),
    url(r'^n_manage_subjects_admin',n_manage_subjects_admin,name="n_manage_subjects_admin"),
    url(r'^subjects',subjects,name="subjects"),
    url(r'^subject_edit',subject_edit,name="subject_edit"),
    url(r'^subject_delete',subject_delete,name="subject_delete"),
    url(r'^o_add_assignment_topic_admin',o_add_assignment_topic_admin,name="o_add_assignment_topic_admin"),
    url(r'^add_assignment_topic',add_assignment_topic,name="add_assignment_topic"),
    url(r'^p_manage_assignment_topic_admin',p_manage_assignment_topic_admin,name="p_manage_assignment_topic_admin"),
    url(r'^topics',topics,name="topics"),
    url(r'^topic_edit',topic_edit,name="topic_edit"),
    url(r'^topic_delete',topic_delete,name="topic_delete"),
    url(r'^e_view_assignments_admin', e_view_assignments_admin,
        name="e_view_assignments_admin"),
    url(r'^assignments', assignments, name="assignments"),
    url(r'^f_check_plagiarism_admin', f_check_plagiarism_admin,
        name="f_check_plagiarism_admin"),
    url(r'^take_status',take_status,name="take_status"),
    # url(r'^check_plagiarism', check_plagiarism, name="check_plagiarism"),
    url(r'^admin_check_plagiarism', admin_check_plagiarism,
        name="admin_check_plagiarism"),
    url(r'^show_grade',show_grade,name="show_grade"),
    url(r'^generate_report_admin', generate_report_admin,
        name="generate_report_admin"),
    url(r'^report_generation', report_generation, name="report_generation"),
    url(r'^match_table_delete', match_table_delete, name="match_table_delete"),
    # ADMIN END

    # STUDENT START
    url(r'^b_home_student', b_home_student, name="b_home_student"),
    url(r'^d_upload_assignment_student', d_upload_assignment_student,
        name="d_upload_assignment_student"),
    url(r'^show_topic_on_subject',show_topic_on_subject,name="show_topic_on_subject"),
    url(r'^last_date_on_topic',last_date_on_topic,name="last_date_on_topic"),
    url(r'^upload_assignment', upload_assignment, name="upload_assignment"),
    url(r'^g_check_plagiarism_student', g_check_plagiarism_student,
        name="g_check_plagiarism_student"),
    url(r'^my_plagiarism', my_plagiarism, name="my_plagiarism"),
    url(r'^store', store, name="store"),
    url(r'^retrieve', retrieve, name="retrieve"),
    url(r'^table_delete', table_delete, name="table_delete"),
    # STUDENT END
]
