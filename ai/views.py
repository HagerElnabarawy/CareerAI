from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from career.models import UserProfile, CareerAnalysis, Roadmap

from .models import Interview, ChatSession, ChatMessage
from .utils import ask_local_ai, extract_json, extract_pdf_text


# =========================================================
# AI CV ANALYSIS
# =========================================================

@login_required
def analyze_cv(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if not profile.cv:
        return redirect("/upload-cv/")

    try:

        cv_text = extract_pdf_text(profile.cv.path)

        if not cv_text:
            return render(
                request,
                "career/analysis.html",
                {
                    "error": "Could not extract text from the CV."
                }
            )

        # Limit CV text to avoid very large prompts
        cv_text = cv_text[:12000]

        prompt = f"""
You are CareerAI, an expert career advisor.

Analyze the following CV carefully.

CV TEXT:
{cv_text}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "recommended_career": "one suitable career title",
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "missing_skills": [
        "skill 1",
        "skill 2",
        "skill 3"
    ],
    "analysis": "a clear explanation of the candidate's profile and why this career was recommended"
}}

Important:
- Choose a career based only on the information in the CV.
- Keep the answer practical.
- Use short clear text.
- Do not use markdown.
- Do not add text outside the JSON.
"""

        ai_response = ask_local_ai(
            prompt,
            json_mode=True
        )

        result = extract_json(ai_response)

        analysis, created = CareerAnalysis.objects.get_or_create(
            user=request.user
        )

        analysis.recommended_career = result.get(
            "recommended_career",
            "Software Developer"
        )

        analysis.strengths = "\n".join(
            result.get("strengths", [])
        )

        analysis.missing_skills = "\n".join(
            result.get("missing_skills", [])
        )

        analysis.analysis = result.get(
            "analysis",
            ""
        )

        analysis.save()

        return redirect("/analysis/")

    except Exception as e:

        return render(
            request,
            "career/analysis.html",
            {
                "error": f"AI analysis failed: {str(e)}"
            }
        )


# =========================================================
# AI ROADMAP
# =========================================================

@login_required
def generate_roadmap(request):

    analysis = CareerAnalysis.objects.filter(
        user=request.user
    ).first()

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not analysis:
        return redirect("/analysis/")

    prompt = f"""
You are CareerAI, an expert learning advisor.

Create a personalized learning roadmap for this user.

Recommended career:
{analysis.recommended_career}

Strengths:
{analysis.strengths}

Missing skills:
{analysis.missing_skills}

Career analysis:
{analysis.analysis}

Additional user skills:
{profile.skills if profile else "Not provided"}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "roadmap": [
        {{
            "title": "Learning step title",
            "description": "Short practical description of what the user should learn."
        }}
    ]
}}

Requirements:
- Create exactly 6 learning steps.
- Start from beginner concepts and gradually move to advanced concepts.
- Focus on the recommended career.
- Focus especially on missing skills.
- Keep descriptions short and practical.
- Do not use markdown.
- Do not add text outside the JSON.
"""

    try:

        ai_response = ask_local_ai(
            prompt,
            json_mode=True
        )

        result = extract_json(ai_response)

        # Expected format:
        #
        # {
        #     "roadmap": [
        #         {
        #             "title": "...",
        #             "description": "..."
        #         }
        #     ]
        # }

        if isinstance(result, dict):

            roadmap_data = result.get(
                "roadmap",
                []
            )

        elif isinstance(result, list):

            # Compatibility in case the AI returns
            # the list directly.
            roadmap_data = result

        else:

            raise ValueError(
                "AI roadmap response has an invalid format."
            )

        if not isinstance(roadmap_data, list):

            raise ValueError(
                "AI roadmap data is not a list."
            )

        # Delete previous roadmap
        Roadmap.objects.filter(
            user=request.user
        ).delete()

        created_count = 0

        for item in roadmap_data:

            if not isinstance(item, dict):
                continue

            title = str(
                item.get(
                    "title",
                    "Learning Step"
                )
            ).strip()

            description = str(
                item.get(
                    "description",
                    ""
                )
            ).strip()

            if not title:
                continue

            Roadmap.objects.create(
                user=request.user,
                title=title,
                description=description
            )

            created_count += 1

        if created_count == 0:

            raise ValueError(
                "AI did not generate any roadmap steps."
            )

        return redirect("/roadmap/")

    except Exception as e:

        return render(
            request,
            "career/roadmap.html",
            {
                "error": f"Roadmap generation failed: {str(e)}",
                "roadmap": []
            }
        )


# =========================================================
# AI MOCK INTERVIEW
# =========================================================

@login_required
def start_interview(request):

    analysis = CareerAnalysis.objects.filter(
        user=request.user
    ).first()

    if analysis:

        career = analysis.recommended_career
        skills = analysis.missing_skills

    else:

        career = "Software Developer"
        skills = ""

    prompt = f"""
You are an expert technical interviewer.

Create ONE interview question for a beginner or intermediate candidate.

Target career:
{career}

Important skills:
{skills}

Requirements:
- Ask only ONE question.
- Make it realistic.
- Make it appropriate for a beginner/intermediate level.
- Focus on Python, Django, web development, databases, APIs, or another skill relevant to the candidate.
- Do not combine many technologies in one question.
- Do not ask about AWS, Docker, CI/CD, and databases all together.
- Return ONLY the question.
- Do not explain the answer.
- Do not use markdown.
"""

    try:

        question = ask_local_ai(
            prompt
        ).strip()

        interview = Interview.objects.create(
            user=request.user,
            question=question
        )

        return render(
            request,
            "ai/interview.html",
            {
                "interview": interview
            }
        )

    except Exception as e:

        return render(
            request,
            "ai/interview.html",
            {
                "error": f"Interview AI failed: {str(e)}"
            }
        )


# =========================================================
# SUBMIT INTERVIEW ANSWER
# =========================================================

@login_required
def submit_interview(request, interview_id):

    interview = get_object_or_404(
        Interview,
        id=interview_id,
        user=request.user
    )

    if request.method != "POST":
        return redirect("/interview/")

    answer = request.POST.get(
        "answer",
        ""
    ).strip()

    if not answer:

        return render(
            request,
            "ai/interview.html",
            {
                "interview": interview,
                "error": "Please write an answer first."
            }
        )

    analysis = CareerAnalysis.objects.filter(
        user=request.user
    ).first()

    career = (
        analysis.recommended_career
        if analysis
        else "Software Developer"
    )

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Career:
{career}

Question:
{interview.question}

Candidate answer:
{answer}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "score": 0,
    "feedback": "short constructive feedback",
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "improvements": [
        "improvement 1",
        "improvement 2"
    ]
}}

Requirements:
- Score must be an integer from 0 to 100.
- Be fair.
- Consider that the candidate may be a beginner.
- Give practical educational feedback.
- Keep the feedback concise.
- Do not use markdown.
- Do not add text outside the JSON.
"""

    try:

        ai_response = ask_local_ai(
            prompt,
            json_mode=True
        )

        result = extract_json(ai_response)

        score = int(
            result.get(
                "score",
                0
            )
        )

        score = max(
            0,
            min(
                100,
                score
            )
        )

        feedback = result.get(
            "feedback",
            ""
        )

        strengths = result.get(
            "strengths",
            []
        )

        improvements = result.get(
            "improvements",
            []
        )

        full_feedback = (
            f"{feedback}\n\n"
            f"Strengths:\n"
            + "\n".join(
                f"- {item}"
                for item in strengths
            )
            + "\n\n"
            f"Improvements:\n"
            + "\n".join(
                f"- {item}"
                for item in improvements
            )
        )

        interview.answer = answer
        interview.score = score
        interview.feedback = full_feedback

        interview.save()

        return render(
            request,
            "ai/interview_result.html",
            {
                "interview": interview
            }
        )

    except Exception as e:

        return render(
            request,
            "ai/interview.html",
            {
                "interview": interview,
                "error": f"AI evaluation failed: {str(e)}"
            }
        )


# =========================================================
# AI CHAT
# =========================================================

@login_required
def chat(request):

    session = (
        ChatSession.objects
        .filter(user=request.user)
        .order_by("-created_at")
        .first()
    )

    if not session:

        session = ChatSession.objects.create(
            user=request.user,
            title="CareerAI Chat"
        )

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if user_message:

            ChatMessage.objects.create(
                session=session,
                role="user",
                message=user_message
            )

            recent_messages = (
                ChatMessage.objects
                .filter(session=session)
                .order_by("-created_at")[:8]
            )

            recent_messages = list(
                reversed(recent_messages)
            )

            history = []

            profile = UserProfile.objects.filter(
                user=request.user
            ).first()

            career_analysis = CareerAnalysis.objects.filter(
                user=request.user
            ).first()

            career = (
                career_analysis.recommended_career
                if career_analysis
                else "Not analyzed yet"
            )

            system_context = f"""
You are CareerAI, an AI career and learning assistant.

User's recommended career:
{career}

User's skills:
{profile.skills if profile else "Not provided"}

Help the user with:
- Career planning
- Python
- Django
- Web development
- Programming
- Learning plans
- Interview preparation
- CV improvement
- Missing skills

Important:
- If the user writes in Arabic, answer in Arabic.
- If the user writes in English, answer in English.
- Give practical and clear explanations.
- Do not pretend to know information that the user did not provide.
- Keep answers reasonably concise.
"""

            history.append(
                {
                    "role": "system",
                    "content": system_context
                }
            )

            # Add previous conversation messages.
            # The current user message is already in the database,
            # so we skip it and send it separately below.
            for message in recent_messages[:-1]:

                if message.role not in [
                    "user",
                    "assistant"
                ]:
                    continue

                history.append(
                    {
                        "role": message.role,
                        "content": message.message
                    }
                )

            try:

                ai_response = ask_local_ai(
                    user_message,
                    history=history
                )

                ChatMessage.objects.create(
                    session=session,
                    role="assistant",
                    message=ai_response
                )

            except Exception as e:

                ChatMessage.objects.create(
                    session=session,
                    role="assistant",
                    message=f"AI connection error: {str(e)}"
                )

    messages = (
        ChatMessage.objects
        .filter(session=session)
        .order_by("created_at")
    )

    return render(
        request,
        "ai/chat.html",
        {
            "session": session,
            "messages": messages
        }
    )