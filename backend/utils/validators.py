import re

ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".txt", ".md"}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def is_valid_password(password: str) -> bool:
    return len(password) >= 6


def is_allowed_upload(filename: str, size_bytes: int) -> tuple[bool, str]:
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        return False, f"File type '{ext}' not allowed. Allowed: {ALLOWED_UPLOAD_EXTENSIONS}"
    if size_bytes > MAX_UPLOAD_SIZE_BYTES:
        return False, "File exceeds maximum allowed size of 10MB."
    return True, ""
