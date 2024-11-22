from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser, Candidate, Company,  CandidateEducation, CandidateSkill, UserCompany, interviews, InterviewReservation, InterviewsPanel, Job, jobsApplication, jobSkill


class AuthUserAdmin(UserAdmin):
    model = AuthUser
    # Customize the admin panel if needed
    fieldsets = UserAdmin.fieldsets + (
        ("DOB and UserType and gender and photo", {
         'fields': ('dob', 'usertype', 'gender', 'photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("DOB and UserType and gender and photo", {
         'fields': ('dob', 'usertype', 'gender', 'photo')}),
    )


admin.site.register(AuthUser, AuthUserAdmin)


# Register your models here.

admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(CandidateEducation)
admin.site.register(CandidateSkill)
admin.site.register(UserCompany)
admin.site.register(interviews)
admin.site.register(InterviewReservation)
admin.site.register(InterviewsPanel)
admin.site.register(Job)
admin.site.register(jobsApplication)
admin.site.register(jobSkill)
