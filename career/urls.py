from django.urls import path

from . import views

from ai.views import (
    analyze_cv,
    generate_roadmap,
)


urlpatterns = [

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'upload-cv/',
        views.upload_cv,
        name='upload_cv'
    ),

    path(
        'analysis/',
        views.analysis_page,
        name='analysis'
    ),

    path(
        'analyze-cv/',
        analyze_cv,
        name='analyze_cv'
    ),

    path(
        'generate-roadmap/',
        generate_roadmap,
        name='generate_roadmap'
    ),

    path(
        'roadmap/',
        views.roadmap_page,
        name='roadmap'
    ),

    path(
        'roadmap/<int:roadmap_id>/toggle/',
        views.toggle_roadmap,
        name='toggle_roadmap'
    ),
]