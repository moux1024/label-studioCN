# 快速开始 - 批量文本替换

## 第一步：预览替换效果（强烈推荐）

```bash
# 预览整个项目
python scripts/replace_text_to_chinese.py --dry-run

# 只预览 web 目录
python scripts/replace_text_to_chinese.py --dir web --dry-run

# 只预览特定目录
python scripts/replace_text_to_chinese.py --dir web/libs/ui --dry-run
```

## 第二步：执行替换

确认预览结果无误后，执行实际替换：

```bash
# 替换整个项目
python scripts/replace_text_to_chinese.py --execute

# 只替换 web 目录
python scripts/replace_text_to_chinese.py --dir web --execute
```

## 重要提示

⚠️ **执行前请确保：**
1. ✅ 代码已提交到 Git（可以回滚）
2. ✅ 已运行预览模式检查结果
3. ✅ 备份重要文件

## 默认行为

- **默认模式**：预览模式（`--dry-run`），不会修改文件
- **自动备份**：执行替换时会自动创建备份
- **自动排除**：测试文件、Storybook文件、构建文件等会被自动排除

## 自定义映射

如果需要添加或修改翻译映射：

1. 保存默认映射到文件：
```bash
python scripts/replace_text_to_chinese.py --save-mapping my_mapping.json
```

2. 编辑 `my_mapping.json`，添加你的自定义映射

3. 使用自定义映射：
```bash
python scripts/replace_text_to_chinese.py --mapping my_mapping.json --execute
```

## 示例输出

```
使用默认映射 (112 条)

开始处理目录: /path/to/project
模式: 预览模式（不会实际修改文件）

[预览] web/libs/ui/src/lib/button/button.tsx (5 处替换)
[预览] web/apps/labelstudio/src/pages/Home/HomePage.tsx (3 处替换)

============================================================
替换统计:
  处理文件数: 150
  修改文件数: 45
  总替换次数: 234
  错误数: 0
============================================================
```

## 恢复备份

如果替换后出现问题，可以从备份恢复：

```bash
# 备份文件保存在各目录的 .text_replace_backup/ 文件夹中
# 例如：
cp web/libs/ui/.text_replace_backup/button.tsx.20240101_120000.bak web/libs/ui/src/lib/button/button.tsx
```

## 常见问题

**Q: 为什么某些文件没有被处理？**
A: 测试文件（`.spec.ts`, `.test.tsx`）和 Storybook 文件（`.stories.tsx`）默认被排除。如需处理，可以修改脚本中的 `EXCLUDE_PATTERNS`。

**Q: 替换后代码报错怎么办？**
A: 从备份文件恢复，或使用 Git 回滚。

**Q: 如何只替换特定类型的文本？**
A: 创建自定义映射文件，只包含需要替换的文本。

## 下一步

替换完成后，建议：
1. 运行项目测试确保功能正常
2. 检查 UI 显示效果
3. 手动调整特殊情况的文本
4. 提交代码到版本控制

