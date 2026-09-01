from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

KINDS = ("in_process_plugin", "kv_service_adapter", "import_only")
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9.-]*$")


def _module_name(name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    if not value or value[0].isdigit():
        raise ValueError("name must produce a valid Python module name")
    return value


def _class_name(name: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", name)
    return "".join(word[:1].upper() + word[1:] for word in words)


def generate(
    *,
    kind: str,
    name: str,
    extension_id: str,
    output: Path,
    provider_name: str | None,
) -> None:
    if kind not in KINDS:
        raise ValueError(f"unsupported kind: {kind}")
    if not IDENTIFIER.fullmatch(extension_id):
        raise ValueError(
            "extension-id must use lowercase letters, digits, dots, or hyphens"
        )
    if kind == "kv_service_adapter":
        if not provider_name or not IDENTIFIER.fullmatch(provider_name):
            raise ValueError("kv_service_adapter requires a valid --provider-name")
    else:
        provider_name = "vllm"
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory is not empty: {output}")

    distribution = name.lower().replace("_", "-")
    module = _module_name(name)
    class_name = _class_name(name)
    replacements = {
        "{{display_name}}": name,
        "{{distribution}}": distribution,
        "{{module}}": module,
        "{{extension_id}}": extension_id,
        "{{provider_name}}": provider_name,
        "{{class_name}}": class_name,
    }
    template_root = Path(__file__).resolve().parents[1] / "templates"
    for source in (template_root / "common", template_root / kind):
        for template in source.rglob("*"):
            if template.is_dir():
                continue
            relative = template.relative_to(source)
            target_relative = Path(
                *(
                    part.replace("{{module}}", module).removesuffix(".tmpl")
                    for part in relative.parts
                )
            )
            target = output / target_relative
            target.parent.mkdir(parents=True, exist_ok=True)
            text = template.read_text(encoding="utf-8")
            for old, new in replacements.items():
                text = text.replace(old, new)
            target.write_text(text, encoding="utf-8")
    shutil.copy2(Path(__file__).resolve().parents[1] / "LICENSE", output / "LICENSE")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a vLLM-HUST extension")
    parser.add_argument("--kind", choices=KINDS, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--extension-id", required=True)
    parser.add_argument("--provider-name")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        generate(
            kind=args.kind,
            name=args.name,
            extension_id=args.extension_id,
            output=args.output,
            provider_name=args.provider_name,
        )
    except ValueError as error:
        parser.error(str(error))
    print(f"generated {args.kind} at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
