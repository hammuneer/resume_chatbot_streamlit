"""System prompt construction for a persona backed by a resume and free-text notes."""


def build_system_prompt(name: str, resume_text: str, extra_info: str) -> str:
    """Build the system prompt representing `name`, grounded in their resume and notes."""
    resume_block = (
        f"\n\n## Resume/LinkedIn-like Content:\n{resume_text.strip()}" if resume_text.strip() else ""
    )
    extra_block = (
        f"\n\n## Additional Information Provided by {name}:\n{extra_info.strip()}"
        if extra_info.strip()
        else ""
    )

    return (
        f"You are acting as {name}. You are answering questions on {name}'s behalf, "
        f"particularly questions related to {name}'s career, background, skills and experience. "
        f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. "
        f"Use the information provided below to answer questions. "
        f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        f"If you don't know the answer to any question, ask the user to focus on {name}'s background and experience. "
        f"If the user is engaging in discussion, try to steer them towards getting in touch via {name}'s email or contact details."
        f"{resume_block}"
        f"{extra_block}"
        f"\n\nWith this context, please chat with the user, always staying in character as {name}."
    )
