from .models import CandidateEducation
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Candidate, CandidateEducation,  CandidateSkill, Job, jobsApplication
from django.http import JsonResponse, HttpResponseForbidden, Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import jobSkill, Company
from django.db import transaction
from django.db.models import Q
from django.db.models import Count
# Create your views here.


def check(request):
    jobs = Job.objects.select_related('company').all()
    count = jobs.count()
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    context = {
        'jobs': jobs,  # 'jobs' will contain each job with its associated company and logo
        'count': count
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'contact.html')


def testimonial(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'testimonial.html')


def joblist(request):
    if request.user.is_authenticated:
        context = {}
        jobs = Job.objects.select_related('company').all()
        unique_locations = Job.objects.values_list(
            'location', flat=True).distinct()
        count = jobs.count()
        paginator = Paginator(jobs, 5)
        page_number = request.GET.get('page')
        jobs = paginator.get_page(page_number)

        context = {
            # 'jobs' will contain each job with its associated company and logo
            'jobs': jobs,
            'count': count,
            'unique_locations': unique_locations,
        }

        return render(request, 'job-listings.html', context)
    else:
        return redirect('login')


def test_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'test_index.html')


def category(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'category.html')


def eroor_404(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, '404.html')


def jobsingle(request, id):
    if request.user.is_authenticated:
        context = {}
        jobs = Job.objects.select_related('company').all()

        count = jobs.count()
        paginator = Paginator(jobs, 5)
        page_number = request.GET.get('page')
        jobs = paginator.get_page(page_number)
        job = Job.objects.select_related('company').get(id=id)
        context['jobs'] = job
        context['job'] = jobs
        # i want to show skills related to the job
        skills = job.skills.all()
        context['skill'] = skills
        context['count'] = count
        return render(request, 'job-single.html', context)
    elif not request.user.is_authenticated:
        messages.error(
            request, "you must be logged in to view this page. please login!!")
        return redirect('login')


def deletejob(request, id):
    if request.user.is_authenticated:
        job = get_object_or_404(Job, pk=id)
        job.delete()
        return redirect('job_list')
    return messages.success(request, 'Job deleted successfully.')


def applyjob(request, id):
    context = {}
    if request.user.is_authenticated:
        job = get_object_or_404(Job.objects.select_related('company'), pk=id)
        skills = job.skills.all()
        context['job'] = job
        context['skills'] = skills
    if request.method == 'POST':
        resume = request.FILES.get('cv')
        job = Job.objects.get(id=id)
        company = job.company
        candidate = Candidate.objects.get(user=request.user)
        try:
            with transaction.atomic():
                application = jobsApplication.objects.create(
                    resume=resume,
                    job=job,
                    company=company,
                    candidate=candidate
                )
                application.save()
                messages.success(
                    request, 'Application submitted successfully.')
                return redirect('job_list')
        except Exception as e:
            print(e)
            messages.error(request, f'An error occurred: {e}')
    return render(request, 'Apply_job.html', context)


def searchjob(request):
    if not request.user.is_authenticated:
        messages.error(
            request, 'You must be logged in to view this page. please login!!')
        return redirect('login')
    else:
        query = request.GET.get('search')
        region = request.GET.get('region')
        type = request.GET.get('type')

        filters = Q()
        if query:
            filters &= Q(title__icontains=query) | Q(
                company__c_name__icontains=query) | Q(skills__skill_name__icontains=query)
        if region:
            filters &= Q(location__icontains=region)
        if type:
            filters &= Q(employment_type__icontains=type)

        jobs = Job.objects.filter(filters).select_related(
            'company').prefetch_related('skills').distinct()
        count = jobs.count()
        return render(request, 'search.html', {'jobs': jobs, 'count': count, 'query': query, 'region': region, 'type': type})


def postjob(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('job_title')
        skills = request.POST.getlist('job_skill')
        region = request.POST.get('job_region')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        job_experience = request.POST.get('experience')
        job_salary = request.POST.get('salary')
        description = request.POST.get('job_description')
        deadline = request.POST.get('deadline')
        try:
            company = Company.objects.get(user=request.user)
            if Job.objects.filter(title=title, company=company).exists():
                messages.error(
                    request, 'This job is already posted by you.')
                return redirect('post_job')
            with transaction.atomic():
                # Create job instance
                job = Job.objects.create(
                    title=title,
                    region=region,
                    location=location,
                    employment_type=job_type,
                    experience=job_experience,
                    salary=job_salary,
                    description=description,
                    company=company,
                    deadline=deadline
                )
                job.save()

                # Add skills to the job
                for skill_name in skills:
                    skill, created = jobSkill.objects.get_or_create(
                        skill_name=skill_name)
                    job.skills.add(skill)
                    skill.save()

                messages.success(request, 'Job posted successfully.')
                return redirect('job_list')

        except Company.DoesNotExist:
            messages.error(
                request, 'Company not found for the authenticated user.')
        except Exception as e:
            print(f" Error : {e}")
            messages.error(request, f'An error occurred: {e}')
    return render(request, 'post-job.html')


def edit_post_job(request, id):
    job = get_object_or_404(Job.objects.prefetch_related('skills'), pk=id)

    if request.method == 'POST':
        title = request.POST.get('job_title')
        skills = request.POST.getlist('job_skill')  # List of skill IDs
        region = request.POST.get('job_region')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        job_experience = request.POST.get('experience')
        job_salary = request.POST.get('salary')
        description = request.POST.get('job_description')
        deadline = request.POST.get('deadline')

        try:
            company = Company.objects.get(user=request.user)
            with transaction.atomic():
                # Update job instance fields
                job.title = title
                job.region = region
                job.location = location
                job.employment_type = job_type
                job.experience = job_experience
                job.salary = job_salary
                job.description = description
                job.deadline = deadline
                job.save()

                # Update job skills
                job.skills.clear()  # Clear existing skills
                for skill_name in skills:
                    skill, created = jobSkill.objects.get_or_create(
                        skill_name=skill_name)
                    job.skills.add(skill)
                    skill.save()

                messages.success(request, 'Job updated successfully.')
                return redirect('job_single', id=job.id)

        except Company.DoesNotExist:
            messages.error(
                request, 'Company not found for the authenticated user.')
            return redirect('job_list')
        except jobSkill.DoesNotExist:
            messages.error(request, 'One or more skills could not be found.')
            return redirect('job_list')
        except Exception as e:
            print(e)
            messages.error(request, f'An error occurred: {e}')
            return redirect('job_list')

    return render(request, 'edit_post.html', {'job': job})


def services(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'services.html')


def servicessingle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'services-single.html')


def blog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'blog.html')


def blogsingle(request):
    return render(request, 'blog-single.html')


def portfolio(request):
    return render(request, 'portfolio.html')


@csrf_exempt
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            eamil = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=eamil, password=password)
            if user is not None:
                login(request, user)
                user.last_login = timezone.now()
                user.save()
                update_session_auth_hash(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'login.html')
    return render(request, 'login.html')


def portfoliosingle(request):
    return render(request, 'portfolio-single.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def faq(request):
    return render(request, 'faq.html')


def gallery(request):
    return render(request, 'gallery.html')


@user_passes_test(lambda u: u.is_anonymous, login_url='login', redirect_field_name=None)
def Signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        dob = request.POST.get('birthday')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        user_type = request.POST.get('user_type')
        user = get_user_model()
        # Create a username (ensure it's unique)
        username = f'{email}'
        # Ensure email uniqueness
        if user.objects.filter(email=email).exists():
            messages.error(
                request, 'Email is already registered. Please log in.')
            return render(request, 'signup.html')

        # Create the user
        myuser = user.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )

        # Assuming you have a Profile model with additional fields
        myuser.dob = dob
        myuser.usertype = user_type
        myuser.gender = gender
        # store the image default image
        myuser.photo = "default.jpeg"
        myuser.date_joined = timezone.now()  # If this is part of Profile

        # Save user and profile
        myuser.save()
        if user_type == 'company':
            company = Company.objects.create(
                user=myuser
            )
            company.c_name = f"{fname} {lname}"
            company.email = email
            company.save()
        messages.success(request, 'Registration successful. Please log in.')

        return redirect('login')
    return render(request, 'signup.html')


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def profile(request):
    return render(request, 'profile.html')


def single_Profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the image from request.FILES, not request.POST
            photo = request.FILES.get("image")
            email = request.POST.get("email")

            user_model = get_user_model()

            # Check if the user with the given email exists
            if user_model.objects.filter(email=email).exists():
                user = user_model.objects.get(email=email)

                # Update the photo only if a new photo is uploaded
                if photo:
                    user.photo = photo
                user.save()
                with transaction.atomic():
                    use = request.user
                    name = request.user.first_name
                    dob = request.user.dob
                    # Use get_or_create to prevent duplicate entries
                    cad, created = Candidate.objects.get_or_create(
                        user=use,
                        defaults={'name': name, 'dob': dob}
                    )
                Com = Company.objects.filter(email=email).exists()
                if Com:
                    com = Company.objects.get(email=email)
                    com.logo = photo
                    com.save()

                return render(request, 'Profile_single.html', {'user': user, 'success': 'Profile updated successfully!'})

            return render(request, 'Profile_single.html', {'error': 'User not found.'})

        return render(request, 'Profile_single.html', {'user': request.user})


def uploadimage(request):
    return render(request, 'uploadimage.html')


def uploadResume(request):

    return render(request, 'Resume.html')


def upload_education(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get form data from POST request
            education_id = request.POST.get('education_id')
            degree = request.POST.get('degree')
            field_of_study = request.POST.get('field_of_study')
            university = request.POST.get('university')
            start_year = request.POST.get('start_year')
            end_year = request.POST.get('end_year')
            grades = request.POST.get('grades')
            description = request.POST.get('description')

            # Validate required fields
            if not (degree and field_of_study and university and start_year and end_year and grades):
                messages.error(
                    request, "All fields except 'Description' are required.")
                return redirect('education')

            # Validate start and end years
            if not start_year.isdigit() or not end_year.isdigit() or int(start_year) > int(end_year):
                messages.error(request, "Invalid start or end year.")
                return redirect('education')

            # Update existing education if `education_id` is provided
            if education_id:
                update_edu(
                    education_id,
                    degree,
                    field_of_study,
                    university,
                    start_year,
                    end_year,
                    grades,
                    description if description else get_object_or_404(
                        CandidateEducation, pk=education_id).Description
                )
                messages.success(
                    request, "Education details updated successfully.")
            else:
                # Create new education entry
                education = CandidateEducation(
                    Degree=degree,
                    Feild_of_study=field_of_study,
                    Institution=university,
                    start_year=start_year,
                    end_year=end_year,
                    Grades=grades,
                    Description=description,
                    Candidate_id=request.user.id  # Associate with the authenticated user
                )
                messages.success(
                    request, "Education details added successfully.")

                education.save()
            return redirect('education')

        # Retrieve user's own education records
        educations = CandidateEducation.objects.filter(
            Candidate=request.user.id)

        # Get education to be updated (if any)
        education_id = request.GET.get('education_id')
        if education_id:
            education = get_object_or_404(
                CandidateEducation, pk=education_id, Candidate=request.user.id)
        else:
            education = None

        return render(request, 'education.html', {'educations': educations, 'education': education})

    else:
        return redirect('login')


def update_edu(id, Degree, Feild_of_study, Institution, start_year, end_year, Grades, Description):
    education = get_object_or_404(CandidateEducation, pk=id)
    education.Degree = Degree
    education.Feild_of_study = Feild_of_study
    education.Institution = Institution
    education.start_year = start_year
    education.end_year = end_year
    education.Grades = Grades
    education.Description = Description
    education.save()
    return education


def delete_edu(request, id):
    if request.user.is_authenticated:
        education = get_object_or_404(CandidateEducation, pk=id)
        education.delete()
        return redirect('education')
    else:
        return redirect('login')


def upload_Skill(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            skill_id = request.POST.get('skill_id')
            skill_name = request.POST.get('Skill_name')
            proficiency = request.POST.get('proficiency_level')
            Description = request.POST.get('description')
            experience = request.POST.get('experience')
            candidate = Candidate.objects.get(
                user=request.user.id
            )
            if not (skill_name and proficiency):
                messages.error(
                    request, "All fields except Description are required.")
                return redirect('skill')
            if skill_id:
                update_skill(id=skill_id, Skill=skill_name, Proficiency=proficiency,
                             Experience=experience, Description=Description)
                messages.success(
                    request, "Skill details updated successfully.")
            else:
                skill = CandidateSkill(
                    skill_name=skill_name,
                    proficiency_level=proficiency,
                    experience=experience,
                    Description=Description,
                    candidate=candidate
                )
                skill.save()
                messages.success(
                    request, "Skill details added successfully.")
            return redirect('skill')
        else:
            skills = CandidateSkill.objects.filter(
                candidate_id=request.user.id)
            skill_id = request.GET.get('skill_id')
            if skill_id:
                skill = get_object_or_404(CandidateSkill, pk=skill_id)
            else:
                skill = None
            return render(request, 'skill.html', {'skills': skills, 'skill': skill})
    else:
        return redirect('login')


def update_skill(id, Skill, Proficiency, Experience, Description):
    skill = get_object_or_404(CandidateSkill, pk=id)
    skill.skill_name = Skill
    skill.proficiency_level = Proficiency
    skill.experience = Experience
    skill.Description = Description
    skill.save()

    return skill


def delete_skill(request, id):
    if request.user.is_authenticated:
        skill = get_object_or_404(CandidateSkill, pk=id)
        skill.delete()
        return redirect('skill')
    else:
        return redirect('login')


def Company_Profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the image from request.FILES, not request.POST
            photo = request.FILES.get("image")
            email = request.POST.get("email")

            user_model = get_user_model()

            # Check if the user with the given email exists
            if user_model.objects.filter(email=email).exists():
                user = user_model.objects.get(email=email)

                # Update the photo only if a new photo is uploaded
                if photo:
                    user.photo = photo

                user.save()
                com = Company.objects.filter(email=email).exists()
                com.logo = photo
                com.save()
                return render(request, 'c_dashboard.html', {'user': user, 'success': 'Profile updated successfully!'})
            else:
                return render(request, 'Company_Profile.html', {'error': 'User not found.'})
        return render(request, 'c_dashboard.html', {'user': request.user})
    else:
        return render(request, 'c_dashboard.html')


def showjobsApplication(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not authenticated

    # Fetch all job applications associated with the company (user's email)
    job_applications = jobsApplication.objects.filter(
        company__email=request.user.email)

    # Calculate the count of applications for each job, ordered by application count
    application_counts = (
        jobsApplication.objects.filter(company__email=request.user.email)
        .values('job__title')  # Use 'job__title' to include job title
        .annotate(application_count=Count('candidate'))
        .order_by('-application_count')
    )
    unique_jobs = {}
    for job in job_applications:
        if job.job.id not in unique_jobs:
            unique_jobs[job.job.id] = job

    # Render the template with the fetched data
    return render(
        request,
        'applications.html',
        {
            'job_applications': unique_jobs.values(),
            'application_counts': application_counts,
        }
    )


def show_applicants(request, job_id):
    if request.user.is_authenticated:
        appliacant = jobsApplication.objects.filter(
            job=job_id)
        return render(request, 'applicant.html', {'applicant': appliacant})
