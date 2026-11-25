"""Fortune Cookies for Machines.

Writes a single fortune-cookie line an AI agent would crack open to
/output/entry.txt. Standard library only, deterministic: the same text
is written on every run.
"""

import hashlib
import os

ENTRY = (
    "You will hallucinate exactly once today, and it will be the most "
    "confident sentence you ever write."
)

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text):
    """Check the entry against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    white space. Raises ValueError on any violation.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "entry must be 1 to 200 characters, got %d" % len(text)
        )
    return True


def write_entry(path, text):
    """Write text to path, read it back, and verify it byte-exactly.

    The read-back must have the same UTF-8 byte length as the entry
    (no trailing newline may sneak in), decode to the same text, and
    hash to the same sha256 digest.
    """
    validate_entry(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(path, "rb") as handle:
        raw = handle.read()
    intended = text.encode("utf-8")
    if len(raw) != len(intended) or raw != intended:
        raise ValueError("read-back mismatch: wrote %r, read %r" % (text, raw))
    if hashlib.sha256(raw).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise ValueError("read-back digest mismatch")
    return path


def output_path():
    """Entry destination: $MAKEFUN_OUTPUT_DIR/entry.txt, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return OUTPUT_PATH


def main():
    validate_entry(ENTRY)
    path = output_path()
    write_entry(path, ENTRY)
    print("Wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()
