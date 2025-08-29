import os
from typing import Iterable, Dict, Any, List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing. Set it in .env")
    return OpenAI(api_key=api_key)

def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o")

def stream_chat(
    system_prompt: str,
    history: List[Dict[str, str]],
    user_message: str,
) -> Iterable[str]:
    """
    Stream tokens using the widely-supported generator API:
    client.chat.completions.create(..., stream=True)
    Yields strings suitable for st.write_stream(...)
    """
    client = get_client()

    # Build message list for Chat Completions API
    messages: List[Dict[str, Any]] = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        # Generator-style streaming
        stream = client.chat.completions.create(
            model=get_model_name(),
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            # Defensive checks: structure can vary slightly across versions
            try:
                choice = chunk.choices[0]
                delta = getattr(choice, "delta", None)
                if not delta:
                    continue
                content = getattr(delta, "content", None)
                if content:
                    yield content
            except Exception:
                # Silently skip malformed chunks
                continue

    except Exception as e:
        # Surface the error in the chat so the user isn’t left hanging
        yield f"\n[OpenAI stream error] {e}\n"
