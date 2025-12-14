# 批量文本替换脚本使用说明

## 概述

`replace_text_to_chinese.py` 是一个用于批量将项目中的英文文本替换为中文的脚本。

## 功能特点

- ✅ **安全预览模式**：默认预览模式，不会实际修改文件
- ✅ **自动备份**：执行替换时自动创建备份文件
- ✅ **智能匹配**：支持多种引号格式（单引号、双引号、模板字符串）
- ✅ **排除机制**：自动排除测试文件、构建文件等
- ✅ **统计报告**：显示详细的替换统计信息
- ✅ **自定义映射**：支持使用自定义的文本映射文件

## 使用方法

### 1. 预览模式（推荐先运行）

```bash
# 预览整个项目
python scripts/replace_text_to_chinese.py --dry-run

# 只预览 web 目录
python scripts/replace_text_to_chinese.py --dir web --dry-run
```

### 2. 实际执行替换

```bash
# 执行替换（会自动创建备份）
python scripts/replace_text_to_chinese.py --execute

# 只处理 web 目录
python scripts/replace_text_to_chinese.py --dir web --execute
```

### 3. 使用自定义映射

```bash
# 使用自定义映射文件
python scripts/replace_text_to_chinese.py --mapping my_custom_mapping.json --execute
```

### 4. 保存默认映射到文件

```bash
# 将默认映射保存为JSON文件，方便编辑
python scripts/replace_text_to_chinese.py --save-mapping text_mapping.json
```

## 默认映射

脚本包含了一个默认的文本映射表，包括：

- 常见按钮：Save, Cancel, Delete, Edit, Create 等
- 状态消息：Loading, Error, Success, Warning 等
- UI标签：Title, Name, Description, Status 等
- 操作相关：Actions, View, Details, History 等
- 表单相关：Required, Optional, Please enter 等

完整列表请查看 `text_mapping_example.json`。

## 自定义映射文件格式

映射文件是JSON格式，键为英文文本，值为中文翻译：

```json
{
  "Save": "保存",
  "Cancel": "取消",
  "Delete": "删除",
  "Custom Text": "自定义文本"
}
```

## 处理范围

### 处理的文件类型
- `.tsx`, `.ts` (TypeScript/React)
- `.jsx`, `.js` (JavaScript/React)
- `.py` (Python)
- `.html` (HTML)

### 自动排除的目录
- `node_modules`
- `.git`
- `dist`, `build`
- `__pycache__`
- `venv`, `env`
- `static_build`
- `migrations`

### 自动排除的文件
- 测试文件 (`.spec.ts`, `.test.tsx` 等)
- Storybook 文件 (`.stories.tsx` 等)
- 压缩文件 (`.min.js`, `.bundle.js` 等)

## 备份机制

执行替换时，脚本会在每个文件所在目录创建 `.text_replace_backup/` 文件夹，并保存带时间戳的备份文件。

备份文件命名格式：`原文件名.20240101_120000.bak`

## 注意事项

⚠️ **重要提示**：

1. **先预览再执行**：强烈建议先使用 `--dry-run` 预览替换结果
2. **版本控制**：执行前确保代码已提交到版本控制系统
3. **测试文件**：默认排除测试文件，如需替换请手动处理
4. **代码逻辑**：脚本只替换字符串字面量，不会修改代码逻辑
5. **部分匹配**：某些复杂文本可能需要手动调整

## 示例输出

```
开始处理目录: /path/to/project
模式: 预览模式（不会实际修改文件）

[预览] web/libs/ui/src/lib/button/button.tsx (5 处替换)
[预览] web/apps/labelstudio/src/pages/Home/HomePage.tsx (3 处替换)
✓ web/libs/ui/src/lib/drawer/drawer.stories.tsx (8 处替换) [备份: drawer.stories.tsx.20240101_120000.bak]

============================================================
替换统计:
  处理文件数: 150
  修改文件数: 45
  总替换次数: 234
  错误数: 0

备份文件保存在各目录的 .text_replace_backup/ 文件夹中
============================================================
```

## 故障排除

### 问题：替换后代码报错

**解决方案**：
1. 检查备份文件，恢复原文件
2. 检查是否有语法错误（如引号不匹配）
3. 某些动态生成的文本可能需要手动处理

### 问题：某些文本没有被替换

**可能原因**：
1. 文本不在映射表中
2. 文本格式特殊（如包含变量）
3. 文件被排除规则过滤

**解决方案**：
1. 添加到自定义映射文件
2. 手动处理特殊情况
3. 检查排除规则

### 问题：编码错误

**解决方案**：
确保文件使用 UTF-8 编码

## 进阶使用

### 只处理特定文件类型

修改脚本中的 `FILE_EXTENSIONS` 变量：

```python
FILE_EXTENSIONS = ['.tsx', '.ts']  # 只处理 TypeScript 文件
```

### 添加更多排除规则

修改 `EXCLUDE_PATTERNS` 列表：

```python
EXCLUDE_PATTERNS = [
    r'.*\.min\.(js|css)$',
    r'.*\.spec\.(ts|tsx|js|jsx)$',
    r'.*custom_pattern.*',  # 添加自定义模式
]
```

## 贡献

如需添加更多默认映射或改进脚本，请：

1. 编辑 `replace_text_to_chinese.py` 中的 `DEFAULT_MAPPING`
2. 或创建自定义映射文件
3. 提交改进建议

