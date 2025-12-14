#!/usr/bin/env python3
"""
批量替换英文文本为中文的脚本

使用方法:
    # 预览模式（不实际修改文件）
    python scripts/replace_text_to_chinese.py --dry-run

    # 实际执行替换
    python scripts/replace_text_to_chinese.py

    # 指定目录
    python scripts/replace_text_to_chinese.py --dir web

    # 自定义映射文件
    python scripts/replace_text_to_chinese.py --mapping custom_mapping.json
"""

import os
import re
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# 默认文本映射表（英文 -> 中文）
DEFAULT_MAPPING = {
    # 常见按钮
    "Save": "保存",
    "Cancel": "取消",
    "Delete": "删除",
    "Edit": "编辑",
    "Create": "创建",
    "Submit": "提交",
    "Confirm": "确认",
    "Close": "关闭",
    "Open": "打开",
    "Add": "添加",
    "Remove": "移除",
    "Update": "更新",
    "Search": "搜索",
    "Filter": "筛选",
    "Reset": "重置",
    "Apply": "应用",
    "Back": "返回",
    "Next": "下一步",
    "Previous": "上一步",
    "Finish": "完成",
    "Skip": "跳过",
    "Continue": "继续",
    "Retry": "重试",
    "Refresh": "刷新",
    "Download": "下载",
    "Upload": "上传",
    "Export": "导出",
    "Import": "导入",
    "Settings": "设置",
    "Preferences": "偏好设置",
    "Help": "帮助",
    "About": "关于",
    
    # 状态和消息
    "Loading": "加载中",
    "Loading...": "加载中...",
    "Error": "错误",
    "Success": "成功",
    "Warning": "警告",
    "Info": "信息",
    "Failed": "失败",
    "Completed": "已完成",
    "Pending": "待处理",
    "Active": "活跃",
    "Inactive": "未激活",
    
    # 常见标签和标题
    "Title": "标题",
    "Name": "名称",
    "Description": "描述",
    "Type": "类型",
    "Status": "状态",
    "Date": "日期",
    "Time": "时间",
    "User": "用户",
    "Users": "用户",
    "Project": "项目",
    "Projects": "项目",
    "Task": "任务",
    "Tasks": "任务",
    "Annotation": "标注",
    "Annotations": "标注",
    "Label": "标签",
    "Labels": "标签",
    "Data": "数据",
    "Model": "模型",
    "Models": "模型",
    
    # 操作相关
    "Actions": "操作",
    "Action": "操作",
    "View": "查看",
    "Details": "详情",
    "History": "历史",
    "Log": "日志",
    "Logs": "日志",
    "Select": "选择",
    "Select All": "全选",
    "Deselect All": "取消全选",
    "Clear": "清除",
    "Clear All": "清除全部",
    
    # 表单相关
    "Required": "必填",
    "Optional": "可选",
    "Please enter": "请输入",
    "Please select": "请选择",
    "Invalid": "无效",
    "Valid": "有效",
    
    # 确认对话框
    "Are you sure?": "确定吗？",
    "Are you sure you want to": "确定要",
    "This action cannot be undone": "此操作无法撤销",
    "Please confirm": "请确认",
    
    # 空状态
    "No data": "暂无数据",
    "No results found": "未找到结果",
    "No items": "无项目",
    "Empty": "空",
    
    # 分页
    "First page": "首页",
    "Previous page": "上一页",
    "Next page": "下一页",
    "Last page": "末页",
    "Page": "页",
    "of": "共",
    "items": "项",
    
    # 其他常见文本
    "Show more": "显示更多",
    "Show less": "显示更少",
    "See more": "查看更多",
    "See less": "查看更少",
    "Expand": "展开",
    "Collapse": "收起",
    "More": "更多",
    "Less": "更少",
    "All": "全部",
    "None": "无",
    "Yes": "是",
    "No": "否",
    "OK": "确定",
    "Welcome": "欢迎",
    "Welcome!": "欢迎！",
    "Welcome 👋": "欢迎 👋",
    "Let's get you started": "让我们开始吧",
    "Let's get you started.": "让我们开始吧。",
    "Create Project": "创建项目",
    "Create your first project": "创建您的第一个项目",
    "Recent Projects": "最近项目",
    "View All": "查看全部",
    "View all": "查看全部",
    "Invite Members": "邀请成员",
    "Import your data and set up the labeling interface to start annotating": "导入您的数据并设置标注界面以开始标注",
    "Create new project": "创建新项目",
    "Resources": "资源",
    "Learn, explore and get help": "学习、探索和获取帮助",
    "Documentation": "文档",
    "API Documentation": "API 文档",
    "Release Notes": "发布说明",
    "LabelStud.io Blog": "LabelStud.io 博客",
    "Slack Community": "Slack 社区",
    "can't load projects": "无法加载项目",
    "Home": "首页",
    "Tasks": "任务",
    "of": "共",
}

# 需要处理的文件扩展名
FILE_EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js', '.py', '.html']

# 需要排除的目录
EXCLUDE_DIRS = {
    'node_modules', '.git', 'dist', 'build', '.next', 
    'coverage', '__pycache__', '.pytest_cache', 'venv',
    'env', '.venv', 'static_build', 'migrations'
}

# 需要排除的文件模式
EXCLUDE_PATTERNS = [
    r'.*\.min\.(js|css)$',
    r'.*\.bundle\.(js|css)$',
    r'.*\.spec\.(ts|tsx|js|jsx)$',  # 测试文件可能需要保留英文
    r'.*\.test\.(ts|tsx|js|jsx)$',
    r'.*\.stories\.(ts|tsx|js|jsx)$',  # Storybook文件
]

class TextReplacer:
    def __init__(self, mapping: Dict[str, str], dry_run: bool = True):
        self.mapping = mapping
        self.dry_run = dry_run
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'replacements': 0,
            'errors': []
        }
        
    def should_exclude_file(self, file_path: Path) -> bool:
        """检查文件是否应该被排除"""
        # 检查目录
        for part in file_path.parts:
            if part in EXCLUDE_DIRS:
                return True
        
        # 检查文件模式
        file_str = str(file_path)
        for pattern in EXCLUDE_PATTERNS:
            if re.match(pattern, file_str):
                return True
        
        return False
    
    def should_process_file(self, file_path: Path) -> bool:
        """检查文件是否应该被处理"""
        if self.should_exclude_file(file_path):
            return False
        
        return file_path.suffix in FILE_EXTENSIONS
    
    def create_backup(self, file_path: Path) -> Path:
        """创建文件备份"""
        backup_dir = file_path.parent / '.text_replace_backup'
        backup_dir.mkdir(exist_ok=True)
        
        # 创建带时间戳的备份
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def replace_in_string(self, text: str, file_path: Path) -> Tuple[str, int]:
        """
        在字符串中替换文本
        返回: (替换后的文本, 替换次数)
        """
        replacements = 0
        result = text
        
        # 按长度降序排序，优先替换长文本（避免部分替换）
        sorted_items = sorted(self.mapping.items(), key=lambda x: len(x[0]), reverse=True)
        
        for english, chinese in sorted_items:
            # 转义特殊字符用于正则表达式
            escaped = re.escape(english)
            
            # 匹配引号内的文本
            # 匹配: "Save", 'Save', `Save`, "Save Button" 等
            patterns = [
                # 双引号字符串（对象属性、JSX属性等）
                (rf'"{escaped}"', f'"{chinese}"'),
                # 单引号字符串
                (rf"'{escaped}'", f"'{chinese}'"),
                # 模板字符串
                (rf'`{escaped}`', f'`{chinese}`'),
                # JSX属性值（无引号的情况，如 aria-label=Save）
                (rf'=({escaped})', f'={chinese}'),
                # JSX子元素中的文本（如 <Button>Cancel</Button>）
                # 匹配 >Cancel< 或 >Cancel</ 或 >Cancel\n
                (rf'>{escaped}<', f'>{chinese}<'),
                (rf'>{escaped}</', f'>{chinese}</'),
                (rf'>{escaped}\n', f'>{chinese}\n'),
                (rf'>{escaped}\s', f'>{chinese} '),
                # JSX 文本节点中的文本（不在引号中，如 <Typography>Welcome</Typography>）
                # 匹配: >\s*Welcome\s*< 或 >\s*Welcome\s*</
                (rf'>\s*{escaped}\s*<', f'>{chinese}<'),
                (rf'>\s*{escaped}\s*</', f'>{chinese}</'),
                # JSX 中的文本，前后可能有空格或换行
                (rf'({escaped})\s*{{', f'{chinese}{{'),
                # 对象字面量中的值（如 title: "Create Project"）
                (rf':\s*"{escaped}"', f': "{chinese}"'),
                (rf':\s*\'{escaped}\'', f": '{chinese}'"),
            ]
            
            for pattern, replacement in patterns:
                matches = len(re.findall(pattern, result))
                if matches > 0:
                    result = re.sub(pattern, replacement, result)
                    replacements += matches
        
        return result, replacements
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            new_content, replacements = self.replace_in_string(original_content, file_path)
            
            if replacements > 0:
                self.stats['files_modified'] += 1
                self.stats['replacements'] += replacements
                
                if not self.dry_run:
                    # 创建备份
                    backup_path = self.create_backup(file_path)
                    
                    # 写入新内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"✓ {file_path} ({replacements} 处替换) [备份: {backup_path.name}]")
                else:
                    print(f"[预览] {file_path} ({replacements} 处替换)")
                
                return True
            else:
                return False
                
        except Exception as e:
            error_msg = f"处理 {file_path} 时出错: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
            return False
    
    def process_directory(self, root_dir: Path):
        """递归处理目录或单个文件"""
        if root_dir.is_file():
            # 如果是文件，直接处理
            if self.should_process_file(root_dir):
                print(f"\n开始处理文件: {root_dir}")
                print(f"模式: {'预览模式（不会实际修改文件）' if self.dry_run else '执行模式（将修改文件）'}\n")
                self.stats['files_processed'] += 1
                self.process_file(root_dir)
                self.print_stats()
            else:
                print(f"文件被排除或不在处理范围内: {root_dir}")
        else:
            # 如果是目录，递归处理
            print(f"\n开始处理目录: {root_dir}")
            print(f"模式: {'预览模式（不会实际修改文件）' if self.dry_run else '执行模式（将修改文件）'}\n")
            
            for root, dirs, files in os.walk(root_dir):
                # 过滤排除的目录
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    if self.should_process_file(file_path):
                        self.stats['files_processed'] += 1
                        self.process_file(file_path)
            
            self.print_stats()
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*60)
        print("替换统计:")
        print(f"  处理文件数: {self.stats['files_processed']}")
        print(f"  修改文件数: {self.stats['files_modified']}")
        print(f"  总替换次数: {self.stats['replacements']}")
        print(f"  错误数: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print("\n错误列表:")
            for error in self.stats['errors']:
                print(f"  - {error}")
        
        if not self.dry_run:
            print("\n备份文件保存在各目录的 .text_replace_backup/ 文件夹中")
        print("="*60)


def load_mapping(mapping_file: str) -> Dict[str, str]:
    """从JSON文件加载自定义映射"""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='批量替换项目中的英文文本为中文',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 预览模式（推荐先运行）
  python scripts/replace_text_to_chinese.py --dry-run
  
  # 实际执行替换
  python scripts/replace_text_to_chinese.py
  
  # 只处理web目录
  python scripts/replace_text_to_chinese.py --dir web
  
  # 使用自定义映射文件
  python scripts/replace_text_to_chinese.py --mapping my_mapping.json
        """
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        default='.',
        help='要处理的目录（默认: 当前目录）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际修改文件（默认开启）'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='实际执行替换（关闭预览模式）'
    )
    
    parser.add_argument(
        '--mapping',
        type=str,
        help='自定义映射JSON文件路径'
    )
    
    parser.add_argument(
        '--save-mapping',
        type=str,
        help='将默认映射保存到JSON文件'
    )
    
    args = parser.parse_args()
    
    # 如果指定了保存映射，则保存并退出
    if args.save_mapping:
        with open(args.save_mapping, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_MAPPING, f, ensure_ascii=False, indent=2)
        print(f"默认映射已保存到: {args.save_mapping}")
        return
    
    # 加载映射
    if args.mapping:
        mapping = load_mapping(args.mapping)
        print(f"已加载自定义映射: {args.mapping} ({len(mapping)} 条)")
    else:
        mapping = DEFAULT_MAPPING
        print(f"使用默认映射 ({len(mapping)} 条)")
    
    # 确定是否执行（默认预览模式，除非指定 --execute）
    dry_run = not args.execute if args.execute else True
    
    # 处理目录
    root_dir = Path(args.dir).resolve()
    if not root_dir.exists():
        print(f"错误: 目录不存在: {root_dir}")
        return
    
    replacer = TextReplacer(mapping, dry_run=dry_run)
    replacer.process_directory(root_dir)


if __name__ == '__main__':
    main()

