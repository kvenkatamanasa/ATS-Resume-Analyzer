# ATS Resume Analyzer — Technical Documentation

## 1. Introduction

ATS Resume Analyzer is a Django-based web application that helps users analyze resumes for Applicant Tracking System (ATS) compatibility and create ATS-friendly resumes.

The application supports two primary workflows:

1. Analyze an existing PDF or DOCX resume.
2. Build a new ATS-friendly resume using predefined templates.

The application also supports optional Job Description analysis to identify matched and missing keywords.

---

# 2. Objectives

The main objectives of the application are:

* Analyze resume structure and content.
* Generate an ATS compatibility score.
* Detect technical skills.
* Identify important resume sections.
* Compare a resume with a target Job Description.
* Identify matched and missing keywords.
* Provide resume improvement recommendations.
* Allow users to build ATS-friendly resumes.
* Preview generated resumes.
* Download resumes in PDF and DOCX formats.
* Maintain user-specific resume and analysis history.

---

# 3. Technology Stack

## Backend

* Python
* Django
* Django Authentication

## Resume Processing

* PyMuPDF
* python-docx

## Analysis

* Python-based text processing
* Keyword matching
* Resume section detection
* Skill detection
* Custom ATS scoring

## Document Generation

* ReportLab
* python-docx

## Frontend

* HTML5
* CSS3
* Django Templates
* Custom responsive CSS

## Database

Development:

* SQLite

Production:

* PostgreSQL

## Deployment

* Gunicorn
* WhiteNoise
* Render

---

# 4. System Architecture

The application follows a Django MVC-style architecture.

```text
                        USER
                         |
                         v
                 Django Web Interface
                         |
          +--------------+--------------+
          |                             |
          v                             v
   Resume Analyzer                 Resume Builder
          |                             |
          v                             v
   File Extraction                Template Selection
          |                             |
          v                             v
   Text Processing                 Resume Form
          |                             |
          v                             v
   ATS Analysis                    BuiltResume
          |                             |
          v                             v
   Score + Keywords               Resume Preview
          |                       /            \
          v                      v              v
   Analysis Result             PDF            DOCX
          |
          v
   Analysis History
```

---

# 5. Project Structure

```text
ATS-Resume-Analyzer/
│
├── README.md
├── DOCUMENTATION.md
├── requirements.txt
├── manage.py
├── build.sh
├── render.yaml
│
├── ai/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── parser.py
│   ├── keywords.py
│   ├── sections.py
│   └── skills.py
│
├── analyzer/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── documents.py
│   │
│   └── migrations/
│
├── ats_analyzer/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   │
│   ├── analyzer/
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   ├── result.html
│   │   ├── templates.html
│   │   ├── builder.html
│   │   └── builder_preview.html
│   │
│   └── registration/
│       ├── login.html
│       └── register.html
│
├── static/
│   └── css/
│       └── style.css
│
└── media/
```

---

# 6. Django Applications

## `ats_analyzer`

This is the main Django project configuration.

Important files:

### `settings.py`

Contains:

* Installed applications
* Middleware
* Templates configuration
* Database configuration
* Static files configuration
* Media configuration
* Authentication configuration

### `urls.py`

Connects the project-level URL configuration with the `analyzer` application.

### `wsgi.py`

Provides the WSGI application for production servers such as Gunicorn.

### `asgi.py`

Provides the ASGI application for asynchronous deployments.

---

# 7. Analyzer Application

The `analyzer` application contains the main business logic.

## `models.py`

Defines the application's database models.

## `forms.py`

Contains:

* Registration form
* Resume upload form
* Resume builder form

## `views.py`

Handles:

* Home page
* Registration
* Dashboard
* Resume upload
* ATS analysis
* Results
* Template selection
* Resume builder
* Resume preview
* PDF download
* DOCX download

## `documents.py`

Responsible for generating downloadable:

* PDF resumes
* DOCX resumes

---

# 8. AI / Analysis Modules

The `ai` package contains resume-analysis logic.

## `parser.py`

Responsible for extracting readable text from uploaded resume files.

The application supports:

```text
PDF
DOCX
```

The extracted text is stored with the uploaded resume.

---

## `analyzer.py`

Coordinates the ATS analysis.

Typical processing flow:

```text
Extracted Text
      |
      v
Keyword Analysis
      |
      +----> Skill Analysis
      |
      +----> Section Analysis
      |
      +----> Experience Analysis
      |
      +----> Formatting Analysis
      |
      v
ATS Score
```

---

## `keywords.py`

Used to process keyword information.

For Job Description analysis, the application compares relevant terms between:

```text
Resume
   +
Job Description
```

and produces:

```text
Matched Keywords
Missing Keywords
```

---

## `sections.py`

Detects common resume sections such as:

* Summary
* Skills
* Experience
* Education
* Projects
* Certifications
* Achievements

---

## `skills.py`

Identifies technical and professional skills from resume text.

Example skills:

```text
Python
SQL
MySQL
Power BI
Excel
Pandas
NumPy
Tableau
Git
GitHub
Machine Learning
```

---

# 9. Database Models

## Resume

The `Resume` model stores uploaded resumes.

Main fields:

```text
id
user
file
original_filename
extracted_text
uploaded_at
```

### Purpose

Stores the uploaded resume and the extracted text used for analysis.

---

## JobDescription

Stores optional Job Description information.

Fields:

```text
id
user
title
description
created_at
```

### Purpose

Allows job-specific resume analysis.

---

## ResumeAnalysis

Stores the results of resume analysis.

Important fields:

```text
id
resume
job_description
ats_score
keyword_score
skills_score
section_score
experience_score
formatting_score
skills
sections
matched_keywords
missing_keywords
recommendations
created_at
```

### Purpose

Stores a historical record of each analysis.

---

## BuiltResume

Stores resumes created using the Resume Builder.

Fields include:

```text
id
user
template
full_name
professional_title
email
phone
location
linkedin
github
summary
skills
experience
projects
education
certifications
achievements
created_at
updated_at
```

---

# 10. User Authentication

The application uses Django's authentication system.

The authentication flow is:

```text
Register
   |
   v
Create User
   |
   v
Login
   |
   v
Dashboard
```

Authenticated views use Django's `login_required` decorator.

User-specific filtering ensures that a user only accesses their own resume and analysis records.

---

# 11. Resume Analysis Workflow

## Step 1 — Upload Resume

The user uploads a PDF or DOCX file.

The application validates:

* File presence
* File extension
* File size

---

## Step 2 — Extract Text

The parser extracts readable text from the document.

Example:

```text
PDF/DOCX
   |
   v
Text Extraction
   |
   v
Resume Text
```

---

## Step 3 — Analyze Resume

The extracted text is passed to the ATS analysis engine.

The engine evaluates multiple areas.

---

## Step 4 — Calculate Scores

The application calculates:

```text
Keyword Score
Skills Score
Section Score
Experience Score
Formatting Score
```

These values contribute to the overall ATS score.

---

## Step 5 — Generate Recommendations

The application generates suggestions based on detected weaknesses.

Examples:

```text
Improve experience bullet points.

Add measurable achievements where truthful.

Increase relevant keyword coverage.

Add missing resume sections.

Improve formatting consistency.
```

---

## Step 6 — Save Analysis

The analysis is saved to the database.

---

## Step 7 — Display Result

The user receives:

* Overall ATS score
* Score breakdown
* Detected skills
* Missing keywords
* Matched keywords
* Resume section status
* Recommendations
* Extracted text

---

# 12. Job Description Matching

Job Description analysis is optional.

### Without Job Description

The system performs:

```text
General ATS Analysis
```

### With Job Description

The system performs:

```text
Resume
   +
Job Description
   |
   v
Keyword Comparison
   |
   +----> Matched Keywords
   |
   +----> Missing Keywords
   |
   +----> Similarity / Match Information
   |
   v
Job-Specific Recommendations
```

---

# 13. ATS Scoring

The application uses a custom scoring framework.

The current score categories are:

| Category          | Purpose                                   |
| ----------------- | ----------------------------------------- |
| Keyword Score     | Measures keyword alignment                |
| Skills Score      | Measures detected skills                  |
| Section Score     | Measures important resume sections        |
| Experience Score  | Evaluates experience-related signals      |
| Formatting Score  | Evaluates basic readability and structure |
| Overall ATS Score | Combines the category scores              |

The score is an application-specific indicator.

It is **not an official score from any particular ATS vendor** and does not guarantee interview selection.

---

# 14. Dashboard

The dashboard displays:

```text
Total Analyses
Average ATS Score
Latest ATS Score
Analysis History
Built Resumes
```

The analysis history includes:

* Resume name
* Job title
* ATS score
* Analysis date
* View action

---

# 15. Resume Templates

The application currently supports:

```text
Classic ATS
Modern ATS
Student / Fresher ATS
Professional ATS
Executive ATS
Minimal ATS
```

Each template is designed around simple text-based content so the resulting resume remains easy for document parsers to read.

---

# 16. Resume Builder Workflow

```text
Templates Page
      |
      v
Choose Template
      |
      v
Builder Form
      |
      v
Enter Resume Information
      |
      v
Save BuiltResume
      |
      v
Preview
```

The builder captures:

* Name
* Professional title
* Contact information
* Summary
* Skills
* Experience
* Projects
* Education
* Certifications
* Achievements

---

# 17. Resume Preview

The preview page displays the generated resume using a clean document layout.

Available actions:

```text
Edit
Download PDF
Download DOCX
Print
```

---

# 18. PDF Generation

The PDF generation module uses ReportLab.

Process:

```text
BuiltResume
     |
     v
Format Resume Content
     |
     v
Create PDF
     |
     v
HTTP Download Response
```

The generated file is provided as:

```text
Your_Name_Resume.pdf
```

---

# 19. DOCX Generation

DOCX generation uses `python-docx`.

Process:

```text
BuiltResume
     |
     v
Format Resume Content
     |
     v
Create DOCX
     |
     v
HTTP Download Response
```

The generated file is provided as:

```text
Your_Name_Resume.docx
```

---

# 20. URL Structure

Main routes include:

```text
/
```

Home page.

```text
/accounts/login/
```

Login.

```text
/accounts/register/
```

Registration.

```text
/dashboard/
```

Dashboard.

```text
/upload/
```

Resume analysis upload.

```text
/templates/
```

Resume template selection.

```text
/builder/<template>/
```

Resume builder.

Example:

```text
/builder/classic/
/builder/modern/
/builder/student/
```

Preview:

```text
/builder/preview/<resume_id>/
```

Analysis result:

```text
/result/<resume_id>/
```

Historical analysis:

```text
/analysis/<analysis_id>/
```

PDF:

```text
/builder/download/pdf/<resume_id>/
```

DOCX:

```text
/builder/download/docx/<resume_id>/
```

---

# 21. Static Files

The application uses Django static files.

Main stylesheet:

```text
static/css/style.css
```

Templates load it using Django's static template tag:

```django
{% load static %}

<link
    rel="stylesheet"
    href="{% static 'css/style.css' %}"
>
```

The interface is implemented using custom CSS without requiring Bootstrap.

---

# 22. Media Files

Uploaded resumes are stored under:

```text
media/resumes/
```

The application uses Django's `MEDIA_ROOT` and `MEDIA_URL` configuration.

For production deployment, uploaded files should use persistent or external file storage rather than relying on an ephemeral application filesystem.

---

# 23. Installation

## Step 1

Create a virtual environment:

```powershell
python -m venv venv
```

## Step 2

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

## Step 3

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Step 4

Run migrations:

```powershell
python manage.py migrate
```

## Step 5

Create an administrator:

```powershell
python manage.py createsuperuser
```

## Step 6

Check the project:

```powershell
python manage.py check
```

## Step 7

Start the development server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 24. Testing Workflow

Test the application in this order:

```text
1. Register
2. Login
3. Open Dashboard
4. Upload Resume
5. Analyze Resume
6. View ATS Result
7. Check Analysis History
8. Open Templates
9. Choose Template
10. Fill Resume Builder
11. Generate Resume
12. Open Preview
13. Download PDF
14. Download DOCX
15. Print Resume
```

---

# 25. Common Errors

## `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'reportlab'
```

Solution:

```powershell
pip install reportlab
```

For DOCX support:

```powershell
pip install python-docx
```

---

## `TemplateDoesNotExist`

Check:

```text
templates/
```

and confirm that the filename matches the path used in `render()`.

---

## 404 on `/result/`

The result URL requires a resume ID:

```text
/result/13/
```

not:

```text
/result/
```

---

## 404 on `/builder/`

The builder URL requires a template:

```text
/builder/classic/
```

not:

```text
/builder/
```

---

## 404 on `/preview/`

The preview route requires an existing built-resume ID:

```text
/builder/preview/5/
```

The ID must correspond to an actual `BuiltResume` belonging to the logged-in user.

---

## `No BuiltResume matches the given query`

This indicates that the requested resume ID does not exist for the current user.

The correct workflow is:

```text
Templates
→ Builder
→ Submit
→ BuiltResume created
→ Preview
```

Do not manually guess the ID.

---

# 26. Deployment Preparation

The project contains:

```text
build.sh
render.yaml
requirements.txt
```

These files are intended to support production deployment.

Typical production configuration:

```text
Browser
   |
   v
Render
   |
   v
Gunicorn
   |
   v
Django
   |
   +---- PostgreSQL
   |
   +---- Static Files
   |
   +---- External/Persistent File Storage
```

Before deployment:

```powershell
python manage.py check --deploy
```

Production configuration should use:

```text
DEBUG=False
```

and secrets should be stored in environment variables.

---

# 27. Security Considerations

The application should:

* Use authenticated views for private data.
* Restrict resume access to the owner.
* Restrict analysis history to the owner.
* Protect forms with CSRF tokens.
* Keep production secrets out of source control.
* Validate uploaded file types.
* Enforce reasonable upload limits.
* Use secure production settings.

Never commit:

```text
.env
db.sqlite3
media/
venv/
API keys
Passwords
Production secrets
```

---

# 28. Development vs Production

## Development

```text
Django runserver
SQLite
Local media
Local static files
DEBUG=True
```

## Production

```text
Gunicorn
PostgreSQL
Persistent/external file storage
WhiteNoise/static hosting
DEBUG=False
Environment variables
HTTPS
```

---

# 29. Limitations

The current implementation has several limitations:

* ATS systems differ between employers and platforms.
* Keyword matching does not guarantee semantic relevance.
* Resume parsing may vary depending on document structure.
* Scanned/image-only documents may require OCR support.
* The custom ATS score is not an official vendor score.
* Free hosting environments may have storage and performance limitations.

---

# 30. Future Enhancements

Potential improvements include:

* Advanced semantic Job Description matching
* Machine-learning-based resume scoring
* Grammar and spelling analysis
* Resume readability scoring
* ATS keyword recommendations
* Duplicate keyword detection
* Resume version management
* Resume comparison
* Cloud file storage
* Password reset
* Email verification
* Advanced analytics dashboard
* Recruiter-focused features
* Resume optimization suggestions based on target roles

---

# 31. Example User Flow

A typical user journey is:

```text
Open Application
       ↓
Create Account
       ↓
Login
       ↓
Dashboard
       ↓
Upload Resume
       ↓
Optional Job Description
       ↓
ATS Analysis
       ↓
View Score
       ↓
Review Skills / Keywords / Sections
       ↓
Read Recommendations
       ↓
Build Improved Resume
       ↓
Choose ATS Template
       ↓
Enter Resume Information
       ↓
Preview Resume
       ↓
Download PDF / DOCX
```

---

# 32. Project Outcome

The project demonstrates practical implementation of:

* Django web development
* User authentication
* File upload and processing
* PDF and DOCX parsing
* Text analysis
* Keyword matching
* Custom scoring
* Database design
* Resume generation
* Responsive web UI
* Document export
* Production deployment preparation

---

# 33. Disclaimer

This application is an educational and portfolio project.

The ATS score is a custom application-generated indicator. Different Applicant Tracking Systems may parse, rank and evaluate resumes differently.

Users should ensure all resume information, skills, experience and achievements are truthful and accurate.

---

# 34. Author

**Kammineni Venkata Manasa**

B.Tech, Computer Science and Engineering

Project: **ATS Resume Analyzer**

Technologies:

```text
Python
Django
SQL
PDF Processing
DOCX Processing
HTML
CSS
Data Analysis
Machine Learning Concepts
```
