"""
Building the prompts sent to the models.

Three techniques (Role Prompting, Few-Shot and Chain-of-Thought) with the
same task core; only the technique layer varies between them. The texts live
in prompts/*.txt and are loaded verbatim: this module fills the fields and
builds the message, it never rewrites the instructions.

Every technique becomes ONE single message with the "user" role, without a
"system" message. If the Role persona went into "system" and the other two
had no such message, the structure of the conversation would vary together
with the text, and the technique would stop being the only manipulated
factor. Without "system" in the request, each model receives the default
SYSTEM of its Modelfile, fixed per model and recorded at every run
(client.environment).
"""

import functools
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"

TECHNIQUES = ("role", "few_shot", "chain_of_thought")


@functools.lru_cache(maxsize=None)
def catalog():
    """Returns the smell catalog (name, definition, technique and example pair)."""
    with open(PROMPTS_DIR / "smells.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


@functools.lru_cache(maxsize=None)
def template(technique):
    """Returns the raw prompt text of a technique."""
    if technique not in TECHNIQUES:
        raise ValueError(
            f"Unknown technique: {technique!r}. Expected one of {TECHNIQUES}."
        )
    return (PROMPTS_DIR / f"{technique}.txt").read_text(encoding="utf-8")


def build(technique, smell, code):
    """Builds the messages of one generation.

    technique: "role", "few_shot" or "chain_of_thought".
    smell:     catalog key (e.g. "LM", "LPL", "LLF" or "MNC").
    code:      the original code of the instance, already adapted.

    Returns the list of messages in the format client.call_model expects.
    """
    smells = catalog()
    if smell not in smells:
        raise ValueError(
            f"Unknown smell: {smell!r}. Expected one of {tuple(smells)}."
        )
    s = smells[smell]

    # The few-shot example is always of the same smell as the instance, so
    # {smell}/{technique} and {example_smell}/{example_technique} come from
    # the same catalog entry. The example fields are unused in the other two
    # templates; format() ignores unused keys.
    # The code goes inside ```python fences in the templates; only trailing
    # line breaks are removed, so the fence closes right after the last line.
    text = template(technique).format(
        smell=s["name"],
        definition=s["definition"],
        technique=s["technique"],
        code=code.rstrip("\n"),
        example_smell=s["name"],
        example_definition=s["definition"],
        example_technique=s["technique"],
        example_before=s["example_before"],
        example_after=s["example_after"],
    )
    return [{"role": "user", "content": text}]
