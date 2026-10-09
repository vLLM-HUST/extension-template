# vLLM-HUST 扩展模板

这是 vLLM-HUST 组织统一的扩展脚手架。模板明确区分三种形态，不能混用：

- `in_process_plugin`：由 vLLM 进程加载的插件；
- `kv_service_adapter`：为外部 KV 系统生成 Connector 配置并做健康检查，
  Extension Manager 不接管服务启停、升级或数据删除；
- `import_only`：仅可发现和检查的研究合同，Manager 必须拒绝启用。

在 GitHub 选择 **Use this template** 创建仓库后执行：

```bash
python tools/new_extension.py \
  --kind in_process_plugin \
  --name my-extension \
  --extension-id org.vllm-hust.my-extension \
  --output generated/my-extension
```

外部 KV 系统使用 `kv_service_adapter`，并传入
`--provider-name my-kv-system`；尚无宿主接口的课题使用 `import_only`。

生成结果包含 Manifest 0.3、`MOD_METADATA.json`、正确的项目命名空间入口、
打包配置、测试和 CI。
提交前必须把示例兼容范围、协议和实现替换为项目的真实证据，禁止把
`>=0` 或示例健康接口直接当成发布承诺。
