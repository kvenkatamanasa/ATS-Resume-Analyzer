from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .forms import (
    ResumeUploadForm,
    RegisterForm,
    ResumeBuilderForm,
)

from .models import (
    Resume,
    ResumeAnalysis,
    JobDescription,
    BuiltResume,
)

from ai.parser import extract_resume_text
from ai.analyzer import analyze_resume

from .documents import (
    create_pdf_response,
    create_docx_response,
)


# =========================================================
# HOME
# =========================================================

def home(request):
    """
    Application home page.

    Logged-in users go to the dashboard.
    Visitors see the public home page.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "analyzer/home.html",
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):
    """
    Create a new user account.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
            )

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):
    """
    Display the logged-in user's dashboard.
    """

    analyses = (
        ResumeAnalysis.objects
        .filter(
            resume__user=request.user,
        )
        .select_related(
            "resume",
            "job_description",
        )
        .order_by(
            "-created_at",
        )
    )

    total_analyses = analyses.count()

    latest_analysis = analyses.first()

    average_score = 0

    if total_analyses > 0:

        total_score = sum(
            analysis.ats_score
            for analysis in analyses
        )

        average_score = round(
            total_score / total_analyses,
            2,
        )

    # Built resumes for this user
    built_resumes = (
        BuiltResume.objects
        .filter(
            user=request.user,
        )
        .order_by(
            "-updated_at",
        )
    )

    context = {
        "analyses": analyses,
        "total_analyses": total_analyses,
        "latest_analysis": latest_analysis,
        "average_score": average_score,
        "built_resumes": built_resumes,
    }

    return render(
        request,
        "analyzer/dashboard.html",
        context,
    )


# =========================================================
# RESUME UPLOAD + ATS ANALYSIS
# =========================================================

@login_required
def upload_resume(request):
    """
    Upload and analyze a resume.

    Job Description is optional.
    """

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            resume = form.save(
                commit=False,
            )

            resume.user = request.user

            uploaded_file = request.FILES.get("file")

            if uploaded_file:
                resume.original_filename = (
                    uploaded_file.name
                )

            job_description = None

            try:

                # -------------------------------------------------
                # EXTRACT RESUME TEXT
                # -------------------------------------------------

                extracted_text = extract_resume_text(
                    resume.file.path,
                )

                if not extracted_text.strip():

                    raise ValueError(
                        "No readable text was found in the "
                        "uploaded resume. Please upload a "
                        "text-based PDF or DOCX file."
                    )

                resume.extracted_text = extracted_text

                resume.save()


                # -------------------------------------------------
                # OPTIONAL JOB DESCRIPTION
                # -------------------------------------------------

                job_title = (
                    form.cleaned_data.get(
                        "job_title",
                        "",
                    )
                    or ""
                )

                job_description_text = (
                    form.cleaned_data.get(
                        "job_description",
                        "",
                    )
                    or ""
                )


                if job_description_text.strip():

                    job_description = (
                        JobDescription.objects.create(
                            user=request.user,
                            title=job_title,
                            description=(
                                job_description_text
                            ),
                        )
                    )


                # -------------------------------------------------
                # ATS ANALYSIS
                # -------------------------------------------------

                analysis_result = analyze_resume(
                    extracted_text,
                    job_description_text,
                )


                # -------------------------------------------------
                # SAVE ANALYSIS
                # -------------------------------------------------

                ResumeAnalysis.objects.create(

                    resume=resume,

                    job_description=(
                        job_description
                    ),

                    ats_score=(
                        analysis_result[
                            "ats_score"
                        ]
                    ),

                    keyword_score=(
                        analysis_result[
                            "keyword_score"
                        ]
                    ),

                    skills_score=(
                        analysis_result[
                            "skills_score"
                        ]
                    ),

                    section_score=(
                        analysis_result[
                            "section_score"
                        ]
                    ),

                    experience_score=(
                        analysis_result[
                            "experience_score"
                        ]
                    ),

                    formatting_score=(
                        analysis_result[
                            "formatting_score"
                        ]
                    ),

                    skills=(
                        analysis_result[
                            "skills"
                        ]
                    ),

                    sections=(
                        analysis_result[
                            "sections"
                        ]
                    ),

                    matched_keywords=(
                        analysis_result[
                            "matched_keywords"
                        ]
                    ),

                    missing_keywords=(
                        analysis_result[
                            "missing_keywords"
                        ]
                    ),

                    recommendations=(
                        analysis_result[
                            "recommendations"
                        ]
                    ),
                )

            except Exception as error:

                # Delete uploaded resume
                # if analysis fails.
                resume.delete()

                if job_description:

                    job_description.delete()

                form.add_error(
                    "file",
                    (
                        "Could not analyze the resume: "
                        f"{error}"
                    ),
                )

            else:

                return redirect(
                    "resume_result",
                    resume_id=resume.id,
                )

    else:

        form = ResumeUploadForm()

    return render(
        request,
        "analyzer/upload.html",
        {
            "form": form,
        },
    )


# =========================================================
# LATEST RESULT FOR RESUME
# =========================================================

@login_required
def resume_result(
    request,
    resume_id,
):
    """
    Display the latest analysis for a user's resume.
    """

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user,
    )

    analysis = (
        ResumeAnalysis.objects
        .filter(
            resume=resume,
        )
        .select_related(
            "job_description",
        )
        .order_by(
            "-created_at",
        )
        .first()
    )

    return render(
        request,
        "analyzer/result.html",
        {
            "resume": resume,
            "analysis": analysis,
        },
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================

@login_required
def analysis_detail(
    request,
    analysis_id,
):
    """
    Display one specific historical analysis.
    """

    analysis = get_object_or_404(
        ResumeAnalysis.objects.select_related(
            "resume",
            "job_description",
        ),
        id=analysis_id,
        resume__user=request.user,
    )

    return render(
        request,
        "analyzer/result.html",
        {
            "resume": analysis.resume,
            "analysis": analysis,
        },
    )


# =========================================================
# ATS TEMPLATE SELECTION
# =========================================================

@login_required
def resume_templates(request):
    """
    Display ATS-friendly resume templates.
    """

    templates = [
        {
            "slug": "classic",
            "name": "Classic ATS",
            "description": (
                "Traditional single-column resume format "
                "suitable for most professional applications."
            ),
            "best_for": (
                "Most professional roles"
            ),
        },
        {
            "slug": "modern",
            "name": "Modern ATS",
            "description": (
                "Clean modern layout with clear visual "
                "hierarchy while remaining ATS-readable."
            ),
            "best_for": (
                "Technology and business roles"
            ),
        },
        {
            "slug": "student",
            "name": "Student / Fresher ATS",
            "description": (
                "Designed for students and fresh graduates "
                "with emphasis on projects and education."
            ),
            "best_for": (
                "Students and freshers"
            ),
        },
        {
            "slug": "professional",
            "name": "Professional ATS",
            "description": (
                "Structured format focused on professional "
                "experience and measurable achievements."
            ),
            "best_for": (
                "Experienced professionals"
            ),
        },
        {
            "slug": "executive",
            "name": "Executive ATS",
            "description": (
                "Strong professional hierarchy for leadership "
                "and senior-level applications."
            ),
            "best_for": (
                "Leadership and senior roles"
            ),
        },
        {
            "slug": "minimal",
            "name": "Minimal ATS",
            "description": (
                "Simple, highly readable format with "
                "minimal visual distractions."
            ),
            "best_for": (
                "General applications"
            ),
        },
    ]

    return render(
        request,
        "analyzer/templates.html",
        {
            "templates": templates,
        },
    )


# =========================================================
# RESUME BUILDER
# =========================================================

@login_required
def resume_builder(
    request,
    template,
):
    """
    Create or edit a resume using the selected template.
    """

    valid_templates = {
        "classic": "Classic ATS",
        "modern": "Modern ATS",
        "student": "Student / Fresher ATS",
        "professional": "Professional ATS",
        "executive": "Executive ATS",
        "minimal": "Minimal ATS",
    }

    if template not in valid_templates:

        return redirect(
            "resume_templates"
        )

    template_name = (
        valid_templates[template]
    )

    if request.method == "POST":

        form = ResumeBuilderForm(
            request.POST,
        )

        if form.is_valid():

            built_resume = form.save(
                commit=False,
            )

            built_resume.user = request.user

            built_resume.template = template

            built_resume.save()

            return redirect(
                "resume_builder_preview",
                resume_id=built_resume.id,
            )

    else:

        form = ResumeBuilderForm()

    return render(
        request,
        "analyzer/builder.html",
        {
            "form": form,
            "template": template,
            "template_name": template_name,
        },
    )


# =========================================================
# RESUME BUILDER PREVIEW
# =========================================================

@login_required
def resume_builder_preview(
    request,
    resume_id,
):
    """
    Display a user's built resume.
    """

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return render(
        request,
        "analyzer/builder_preview.html",
        {
            "resume": resume,
        },
    )


# =========================================================
# DOWNLOAD PDF
# =========================================================

@login_required
def download_resume_pdf(
    request,
    resume_id,
):
    """
    Download the logged-in user's resume as PDF.
    """

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return create_pdf_response(
        resume
    )


# =========================================================
# DOWNLOAD DOCX
# =========================================================

@login_required
def download_resume_docx(
    request,
    resume_id,
):
    """
    Download the logged-in user's resume as DOCX.
    """

    resume = get_object_or_404(
        BuiltResume,
        id=resume_id,
        user=request.user,
    )

    return create_docx_response(
        resume
    )