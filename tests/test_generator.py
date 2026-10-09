from pathlib import Path

import pytest

from tools.new_extension import generate


@pytest.mark.parametrize(
    ("kind", "provider"),
    [
        ("in_process_plugin", None),
        ("import_only", None),
        ("kv_service_adapter", "example-kv"),
    ],
)
def test_each_profile_generates_without_placeholders(
    tmp_path: Path, kind: str, provider: str | None
) -> None:
    output = tmp_path / kind
    slug = kind.replace("_", "-")
    generate(
        kind=kind,
        name=f"example-{slug}",
        extension_id=f"org.vllm-hust.example-{slug}",
        output=output,
        provider_name=provider,
    )

    files = [path for path in output.rglob("*") if path.is_file()]
    assert files
    unresolved = (
        "{{display_name}}",
        "{{distribution}}",
        "{{module}}",
        "{{extension_id}}",
        "{{provider_name}}",
        "{{class_name}}",
    )
    assert not any(
        token in path.read_text(encoding="utf-8")
        for path in files
        for token in unresolved
    )
    assert (output / "pyproject.toml").is_file()
    assert len(list(output.rglob("vllm-hust-extension-v0.3.json"))) == 1
    metadata = output / "MOD_METADATA.json"
    assert metadata.is_file()
    assert '"schema_version": "vllm-hust-mod-metadata-v1"' in metadata.read_text(
        encoding="utf-8"
    )


def test_external_service_requires_provider_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="provider-name"):
        generate(
            kind="kv_service_adapter",
            name="example",
            extension_id="org.vllm-hust.example",
            output=tmp_path / "example",
            provider_name=None,
        )
