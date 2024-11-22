from django.urls import path
from jobwebsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home/", views.check, name='home'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("testimonial/", views.testimonial, name='testimonial'),
    path("job_list/", views.joblist, name='job_list'),
    path("test_index/", views.test_index, name='test_index'),
    path("category/", views.category, name='category'),
    path("404/", views.eroor_404, name='404'),
    path("job_single/<int:id>", views.jobsingle, name='job_single'),
    path("post_job/", views.postjob, name='post_job'),
    path("services/", views.services, name='services'),
    path("service_single/", views.servicessingle, name='service_single'),
    path("blog/", views.blog, name='blog'),
    path("blog_single/", views.blogsingle, name='blog_single'),
    path("login/", views.signin, name='login'),
    path("portfolio/", views.portfolio, name='portfolio'),
    path("portfolio_single/", views.portfoliosingle, name='portfolio_single'),
    path('testimonials/', views.testimonial, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path("gallery/", views.gallery, name='gallery'),
    path("register/", views.Signup, name='register',),
    path("logout/", views.signout, name='logout'),
    path("dashboard/", views.profile, name='dashboard'),
    path('profile', views.single_Profile, name='profile'),
    path('upload_resume/', views.uploadResume, name='upload_resume'),
    path('education/', views.upload_education, name='education'),
    path('delete/<int:id>/', views.delete_edu, name='delete'),
    path('skill/', views.upload_Skill, name='skill'),
    path('delete_skill/<int:id>/', views.delete_skill, name='delete_skill'),
    path('companyProfile/', views.Company_Profile, name='companyProfile'),
    path('delete_job/<int:id>/', views.deletejob, name='delete_job'),
    path("ApplyJob/<int:id>", views.applyjob, name='ApplyJob'),
    path("edit/<int:id>/", views.edit_post_job, name='edit'),
    path("search/", views.searchjob, name='search'),
    path("applications/", views.showjobsApplication, name='applications'),
    path("applicants/<int:job_id>/",
         views.show_applicants, name='applicants'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
