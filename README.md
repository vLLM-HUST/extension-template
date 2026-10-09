# vLLM-HUST Extension Template

This GitHub template creates extensions that follow the vLLM-HUST Extension
Manager boundary. It deliberately separates three shapes:

- `in_process_plugin`: code loaded by vLLM;
- `kv_service_adapter`: a Provider that renders connector configuration and
  checks an externally operated service without owning its lifecycle;
- `import_only`: discoverable research metadata that the Manager must refuse to
  enable until a real host contract exists.

## Create an extension

Use this repository as a GitHub template, then run:

```bash
python tools/new_extension.py \
  --kind in_process_plugin \
  --name my-extension \
  --extension-id org.vllm-hust.my-extension \
  --output generated/my-extension
```

For an external KV system, select `kv_service_adapter` and add
`--provider-name my-kv-system`. For an inert contract proposal, select
`import_only`.

The generated repository contains a static Manifest 0.3 descriptor,
`MOD_METADATA.json`, package entry points, tests, build metadata, and CI.
Replace every example
implementation and compatibility range with evidence from the real project.

See [README.zh.md](README.zh.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for the
required review checklist.
