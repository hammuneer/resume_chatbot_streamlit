from dataclasses import dataclass, field
from .resume_parser import extract_text_from_pdf_bytes
from .prompts import build_system_prompt

@dataclass
class Persona:
    name: str = ""
    resume_bytes: bytes | None = None
    extra_info: str = ""
    _cached_resume_text: str = field(default="", init=False, repr=False)

    def resume_text(self) -> str:
        if self._cached_resume_text:
            return self._cached_resume_text
        self._cached_resume_text = extract_text_from_pdf_bytes(self.resume_bytes)
        return self._cached_resume_text

    def system_prompt(self) -> str:
        return build_system_prompt(self.name or "Unknown Person", self.resume_text(), self.extra_info or "")
