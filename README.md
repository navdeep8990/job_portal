# **JobPortal Project**

A feature-rich job portal built with **Python Django** to connect job seekers and employers.

---

## **Features**
1. **User Management**:
   - Separate profiles for Candidates and Companies.
   - Secure authentication with role-based access.

2. **Job Listings**:
   - Companies can post, edit, and delete jobs.
   - Jobs categorized by skills, location, and salary range.

3. **Job Applications**:
   - Candidates can apply for jobs and upload resumes.
   - Employers can view, track, and filter applications.

4. **Search and Filters**:
   - Job seekers can search and filter jobs by keywords, skills, and location.

5. **Interview Scheduling**:
   - Manage interview processes and track completed interviews.

6. **Admin Dashboard**:
   - Monitor user activity, jobs, and applications with analytics.

---

## **Installation**

### 1. Clone the repository:
   ```bash
   git clone https://github.com/navdeep8990/jobportal.git
   cd jobportal
 ```
### 2. Set up a virtual environment
Create a virtual environment to manage dependencies:

 ```bash
python -m venv venv
```
### Activate the virtual environment:
#### On Windows:
 ```bash
venv\Scripts\activate
 ```
#### On macOS/Linux:bash
 ```bash
source venv/bin/activate
```
## 3. Install dependencies
#### Install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```
## 4. Apply migrations
#### Make and apply migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
## 5. Create a superuser
#### Create a superuser for admin access:
```bash
python manage.py createsuperuser
```
# Follow the prompts to set up the admin credentials.
## 6. Run the development server
### Start the Django development server:
```bash
python manage.py runserver
```
## 7. Access the app
Job Portal: Open your browser and navigate to ` http://127.0.0.1:8000/` to access the Job Portal

# Technologies Used
#### Backend: Python, Django
#### Frontend: HTML, CSS, Bootstrap
#### Database:MySQL 


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

