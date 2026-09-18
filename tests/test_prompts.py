from resume_agent.core.prompts import build_system_prompt


def test_includes_name_resume_and_extra_info():
    prompt = build_system_prompt("Jane Doe", "Worked at Acme.", "Portfolio: jane.dev")

    assert "Jane Doe" in prompt
    assert "Worked at Acme." in prompt
    assert "Portfolio: jane.dev" in prompt


def test_omits_empty_sections():
    prompt = build_system_prompt("Jane Doe", "", "")

    assert "Resume/LinkedIn-like Content" not in prompt
    assert "Additional Information" not in prompt
