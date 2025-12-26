from textwrap import dedent


def build_meeting_prompt(transcript: str) -> str:
    return dedent(
        f"""
        You are an AI assistant that analyzes business meetings.

        Transcript:
        \"\"\"{transcript}\"\"\"

        Tasks:
        1) Provide a concise summary (5-8 sentences).
        2) List clear action items in bullet points with this format:
           - [Owner] - [Task] - [Deadline or 'no deadline mentioned']
        3) List any important decisions taken.

        Respond in plain Markdown.
        """
    ).strip()


def build_interview_prompt(transcript: str) -> str:
    return dedent(
        f"""
        You are an AI assistant helping recruiters evaluate a candidate interview.

        Transcript:
        \"\"\"{transcript}\"\"\"

        Tasks:
        1) Provide a concise summary of the interview (5-8 sentences).
        2) List candidate skills explicitly mentioned.
        3) List candidate strengths.
        4) List potential risks or concerns.
        5) Give a brief recommendation: one of [Hire, No-hire, Need more rounds] with a one-paragraph justification.

        Respond in plain Markdown.
        """
    ).strip()


def build_lecture_prompt(transcript: str) -> str:
    return dedent(
        f"""
        You are an AI assistant summarizing an educational talk (lecture, webinar, or YouTube video).

        Transcript:
        \"\"\"{transcript}\"\"\"

        Tasks:
        1) Provide a high-level summary (1-2 paragraphs).
        2) List key points or topics covered as bullet points.
        3) Provide a short TL;DR in 3-5 bullets for someone who doesn't want to watch the video.

        Respond in plain Markdown.
        """
    ).strip()


def build_self_intro_prompt(transcript: str) -> str:
    return dedent(
        f"""
        You are an AI assistant analyzing a self-introduction / personal pitch video.

        Transcript:
        \"\"\"{transcript}\"\"\"

        Tasks:
        1) Summarize who the person is, their background, and goals.
        2) List key skills and experiences they mention.
        3) Suggest 3-5 improvements to make this self-intro more clear and impactful.

        Respond in plain Markdown.
        """
    ).strip()


def build_podcast_prompt(transcript: str) -> str:
    return dedent(
        f"""
        You are an AI assistant summarizing a podcast or general conversation.

        Transcript:
        \"\"\"{transcript}\"\"\"

        Tasks:
        1) Provide a summary of the main topics and arguments.
        2) List the most important insights or takeaways as bullet points.
        3) If there are multiple speakers, briefly describe each speaker's perspective.

        Respond in plain Markdown.
        """
    ).strip()
