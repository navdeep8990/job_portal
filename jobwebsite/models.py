from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class AuthUser(AbstractUser):
    dob = models.CharField(max_length=255)
    usertype = models.CharField(max_length=50, default="candidate", choices=[
                                ("candidate", "candidate"), ("company", "comapny")])
    gender = models.CharField(max_length=10, default="male", choices=[
                              ("male", "male"), ("female", "female"), ("other", "other")])
    photo = models.ImageField(upload_to="photo/", default='photo/default.png')

    def __str__(self):
        return self.username

# create class candidate


class Candidate(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    resume = models.FileField(upload_to="resume/", default='resume/resume.pdf')
    dob = models.DateField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    education = models.CharField(max_length=50, default='Graduate', choices=[('Graduate', 'Graduate'),
                                                                             ('Post Graduate',
                                                                              'Post Graduate'),
                                                                             ('Doctorate',
                                                                              'Doctorate'),
                                                                             ('Diploma',
                                                                              'Diploma'),
                                                                             ('Others', 'Others')])
    experience = models.CharField(max_length=50, default='Fresher', choices=[('Fresher', 'Fresher'),
                                                                             ('1-2 Years',
                                                                              '1-2 Years'),
                                                                             ('2-5 Years',
                                                                              '2-5 Years'),
                                                                             ('5-10 Years',
                                                                              '5-10 Years'),
                                                                             ('10+ Years', '10+ Years')])

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, primary_key=True)
    c_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="logo/", default='logo/logo.png')
    address = models.CharField(max_length=100)
    website = models.URLField(max_length=50)
    industry = models.CharField(max_length=50, default='IT-services', choices=[("Service-Based", "Service-Based"),
                                                                               ("Product-Based",
                                                                                "Product-Based"),
                                                                               ("IT-services",
                                                                                "IT-services"),
                                                                               ("Others", "Others")])
    company_type = models.CharField(max_length=50, default='Startup', choices=[('Startup', 'Startup'),
                                                                               ('Small Scale',
                                                                                'Small Scale'),
                                                                               ('Medium Scale',
                                                                                'Medium Scale'),
                                                                               ('Large Scale',
                                                                                'Large Scale')])

    def __str__(self):
        return self.c_name


class jobSkill(models.Model):
    skill_id = models.AutoField(primary_key=True, auto_created=True)
    skill_name = models.CharField(max_length=255)


class Job(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    region = models.CharField(max_length=50, default='India')
    description = models.TextField()
    employment_type = models.CharField(max_length=50, default='Full-Time', choices=[('Full-Time', 'Full-Time'),
                                                                                    ('Part-Time',
                                                                                     'Part-Time'),
                                                                                    ('Contract',
                                                                                     'Contract'),
                                                                                    ('Internship', 'Internship')])
    experience = models.CharField(max_length=50, default='Fresher', choices=[('Fresher', 'Fresher'),
                                                                             ('1-2 Years',
                                                                              '1-2 Years'),
                                                                             ('2-5 Years',
                                                                              '2-5 Years'),
                                                                             ('5-10 Years',
                                                                              '5-10 Years'),
                                                                             ('10+ Years', '10+ Years')])
    salary = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    skills = models.ManyToManyField(jobSkill, related_name='jobs')
    published_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


class jobsApplication(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to="resume/", default='resume/resume.pdf')
    status = models.CharField(max_length=50, default='Applied', choices=[('Applied', 'Applied'),
                                                                         ('Shortlisted',
                                                                          'Shortlisted'),
                                                                         ('Rejected',
                                                                          'Rejected'),
                                                                         ('Hired', 'Hired')])

    def __str__(self):
        return f"{self.candidate.name} applied for {self.job.title}"


class interviews(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interview_type = models.CharField(max_length=50,
                                      default='HR Interview', choices=[('HR Interview', 'HR Interview'),
                                                                       ('Technical', 'Technical'),])
    interview_mode = models.CharField(max_length=50, default='Scheduled', choices=[(
        'Telephonic', 'Telephonic'), ('video call', 'video call'), ('Face To Face', 'Face To Face')])
    interview_date = models.DateTimeField(auto_now_add=True)
    interview_time = models.TimeField(auto_now_add=True)
    interviewer_panel = models.ForeignKey(
        'InterviewsPanel', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Scheduled', choices=[('Scheduled', 'Scheduled'),
                                                                           ('Completed',
                                                                            'Completed'),
                                                                           ('Cancelled',
                                                                            'Cancelled'),
                                                                           ('Rescheduled', 'Rescheduled')])

    def __str__(self):
        return f"Interview for {self.candidate.name} on {self.interview_date}"


class InterviewReservation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate_name = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interview_id = models.ForeignKey(interviews, on_delete=models.CASCADE)
    interview_date = models.DateTimeField(auto_now_add=True)
    interviewr_panel = models.ForeignKey(
        'InterviewsPanel', on_delete=models.CASCADE)
    ReservationDate = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Scheduled', choices=[('Pending', 'Pending'),
                                                                           ('Confirmed',
                                                                            'Confirmed'),
                                                                           ('Cancelled',
                                                                            'Cancelled')])

    def __str__(self):
        return f"Reservation for {self.candidate_name.name} on {self.ReservationDate} for  {self.job.title }"


class CandidateSkill(models.Model):
    choices = [("Communication Skills", "Communication Skills"),
               ("Management Skills", "Management Skills"),
               ("Backend Developer", "Backend Developer"),
               ("Frontend Developer", "Frontend Developer"),
               (".DotNet Developer", ".DotNet Developer"),
               ("MERN-Stack Developer", "MERN-Stack Developer"),
               ("Full-stack Developer", "Full-Stack Developer"),
               ("Java Developer", "Java Developer"),
               ("Python Developer", "Python Developer"),
               ("Python-Full-Stack Developer", "Python-Full-Stack Developer"),
               (" c/c++", "c/c++"),
               ("AI/ML Developer", "AI/ML Developer"),
               ("Data Science", "Data Science"),
               ("Data Analyst", "Data Analyst"),
               ("Data Engineer", "Data Engineer"),
               ("Data Architect", "Data Architect"),
               ("Data Administrator", "Data Administrator"),
               ("Data Security Analyst", "Data Security Analyst"),
               ("Data Warehousing Specialist", "Data Warehousing Specialist"),
               ("Database Manager", "Database Manager"),
               ("Database Developer", "Database Developer"),
               ("Database Administrator", "Database Administrator"),
               ("Database Analyst", "Database Analyst"),
               ("Database Designer", "Database Designer"),
               ("Database Security Specialist", "Database Security Specialist"),
               ("Database Architect", "Database Architect"),
               ("Database Coordinator", "Database Coordinator"),
               ("Database Programmer", "Database Programmer"),
               ("Database Modeller", "Database Modeller"),
               ("Database Tuner", "Database Tuner"),
               ("Database Consultant", "Database Consultant"),
               ("Database Vendor", "Database Vendor"),
               ("Database Specialist", "Database Specialist"),
               ("Database Operator", "Database Operator"),
               ("Database Administrator", "Database Administrator"),
               ("Database Manager", "Database Manager"),
               ("Database Developer", "Database Developer"),
               ("Database Analyst", "Database Analyst"),
               ("Database Designer", "Database Designer"),
               ("Database Security Specialist", "Database Security Specialist"),
               ("Database Architect", "Database Architect"),
               ("Database Coordinator", "Database Coordinator"),
               ("Database Programmer", "Database Programmer"),
               ("Database Modeller", "Database Modeller"),
               ("Database Tuner", "Database Tuner"),
               ("Database Consultant", "Database Consultant"),
               ("Database Vendor", "Database Vendor"),
               ("Database Specialist", "Database Specialist"),
               ("Database Operator", "Database Operator"),
               ("Database Administrator", "Database Administrator"),
               ("Database Manager", "Database Manager"),
               ("Database Developer", "Database Developer"),
               ("Database Analyst", "Database Analyst"),
               ("Database Designer", "Database Designer"),
               ("Database Security Specialist", "Database Security Specialist"),
               ("Database Architect", "Database Architect"),
               ("Database Coordinator", "Database Coordinator"),
               ("Database Programmer", "Database Programmer"),
               ("Database Modeller", "Database Modeller"),
               ("Database Tuner", "Database Tuner"),
               ("Database Consultant", "Database Consultant"),
               ("Database Vendor", "Database Vendor"),
               ("Database Specialist", "Database Specialist"),
               ("Database Operator", "Database Operator"),
               ("Database Administrator", "Database Administrator ")]
    CandidateSkill_id = models.AutoField(primary_key=True, auto_created=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill_name = models.CharField(
        max_length=255, default='Communication Skill', choices=choices)
    proficiency_level = models.CharField(max_length=255, default='Beginner ', choices=[('Beginner', 'Beginner'),
                                                                                       ('Intermediate',
                                                                                        'Intermediate'),
                                                                                       ('Expert', 'Expert')])
    experience = models.CharField(max_length=50, default='Fresher', choices=[('Fresher', 'Fresher'),
                                                                             ('1-2 Years',
                                                                              '1-2 Years'),
                                                                             ('2-5 Years',
                                                                              '2-5 Years'),
                                                                             ('5-10 Years',
                                                                              '5-10 Years'),
                                                                             ('10+ Years', '10+ Years')])
    Description = models.TextField(default='Good')


class InterviewsPanel(models.Model):
    panel_id = models.AutoField(primary_key=True, auto_created=True)
    interviews_id = models.ForeignKey(interviews, on_delete=models.CASCADE)
    InterviewReservation_id = models.ForeignKey(
        InterviewReservation, on_delete=models.CASCADE)
    interviewer_name = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(max_length=10)
    location = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50, default='Scheduled', choices=[('Scheduled', 'Scheduled'),
                                                     ('Completed', 'Completed'),
                                                     ('Cancelled', 'Cancelled'),
                                                     ('Rescheduled', 'Rescheduled')])


class CandidateEducation(models.Model):
    CandidateEducation_id = models.AutoField(
        primary_key=True, auto_created=True)
    Candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    Degree = models.CharField(max_length=50)
    Institution = models.CharField(max_length=50)
    Feild_of_study = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    Grades = models.CharField(max_length=50)
    Description = models.TextField()


class UserCompany(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Active', choices=[
                              ('Active', 'Active'), ('InActive', 'InActive')])
