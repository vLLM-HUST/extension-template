# Extension review checklist

Before requesting inclusion on the vLLM-HUST website:

1. Declare the correct `kind`, `host`, `runtime`, and `lifecycle_owner`.
2. Use `vllm_hust.extension_bundles` for manifests and
   `vllm_hust_ext.providers` only for Host Provider factories.
3. Prove wheel installation and static discovery in a clean environment.
4. Pin compatibility to tested host and protocol evidence; do not invent a
   semantic protocol version for an unversioned upstream surface.
5. Preserve existing plugin constraints such as device count, prefix-cache
   mode, model family, architecture, and Python versions.
6. Mark incomplete implementations `import_only`; CI must prove enablement is
   rejected.
7. For external services, test unreachable, unhealthy, recovery, and config
   conflicts. Providers may plan, render, and check, but may not start, stop,
   clear, upgrade, or delete shared services.
8. Declare a license before publication and document install, inspect, enable,
   run, disable, forget, and uninstall behavior that actually exists.
