from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserProfile, CareerAnalysis, Roadmap


@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    analysis = CareerAnalysis.objects.filter(
        user=request.user
    ).first()

    roadmap_count = Roadmap.objects.filter(
        user=request.user
    ).count()

    completed_count = Roadmap.objects.filter(
        user=request.user,
        completed=True
    ).count()

    return render(
        request,
        "career/dashboard.html",
        {
            "profile": profile,
            "analysis": analysis,
            "roadmap_count": roadmap_count,
            "completed_count": completed_count,
        }
    )


@login_required
def upload_cv(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        cv_file = request.FILES.get("cv")

        if not cv_file:
            return render(
                request,
                "career/upload_cv.html",
                {"error": "Please select a PDF file."}
            )

        if not cv_file.name.lower().endswith(".pdf"):
            return render(
                request,
                "career/upload_cv.html",
                {"error": "Only PDF files are allowed."}
            )

        profile.cv = cv_file
        profile.save()

        return redirect("/analyze-cv/")

    return render(
        request,
        "career/upload_cv.html"
    )


@login_required
def analysis_page(request):
    analysis = CareerAnalysis.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "career/analysis.html",
        {
            "analysis": analysis
        }
    )


@login_required
def roadmap_page(request):
    roadmap = Roadmap.objects.filter(
        user=request.user
    )

    return render(
        request,
        "career/roadmap.html",
        {
            "roadmap": roadmap
        }
    )


@login_required
def toggle_roadmap(request, roadmap_id):
    item = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        user=request.user
    )

    item.completed = not item.completed
    item.save()

    return redirect("/roadmap/")