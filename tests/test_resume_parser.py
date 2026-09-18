from resume_agent.core.resume_parser import extract_text_from_pdf_bytes


def test_returns_empty_string_for_none():
    assert extract_text_from_pdf_bytes(None) == ""


def test_returns_empty_string_for_malformed_bytes():
    assert extract_text_from_pdf_bytes(b"not a pdf") == ""
