#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Releases 监控程序
监控用户关注的 GitHub 仓库 releases 更新
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="requests")

import sys
import os
import json
import sqlite3
import time
import hashlib
import shutil
import requests
import threading
import queue
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pypinyin
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QTabWidget, QComboBox, QSpinBox, QCheckBox, QRadioButton,
    QButtonGroup, QGroupBox, QGridLayout, QMessageBox, QDialog,
    QDialogButtonBox, QFileDialog, QProgressBar, QHeaderView,
    QSplitter, QTextEdit, QListWidget, QListWidgetItem, QMenu,
    QSystemTrayIcon, QScrollArea, QFrame, QAbstractItemView,
    QDateTimeEdit, QDateEdit, QStyleFactory, QInputDialog
)
from PySide6.QtCore import (
    Qt, QThread, Signal, Slot, QTimer, QDateTime, QDate,
    QSettings, QSize, QPoint, QRect, QPropertyAnimation,
    QEasingCurve, QCoreApplication
)
from PySide6.QtGui import (
    QIcon, QPixmap, QFont, QColor, QPalette, QAction,
    QBrush, QPen, QPainter, QLinearGradient, QCursor, QTextCursor
)

# ==================== 项目信息元数据 ====================
class ProjectInfo:
    """项目信息元数据（集中管理所有项目相关信息）"""
    VERSION = "1.1.15"
    BUILD_DATE = "2026-03-10"
    AUTHOR = "杜玛"
    LICENSE = "GNU Affero General Public License v3.0"
    COPYRIGHT = "© 永久 杜玛"
    URL = "https://github.com/duma520"
    MAINTAINER_EMAIL = "不提供"
    NAME = "GitHub Releases 监控程序"
    DESCRIPTION = "GitHub Releases 监控程序 - 监控用户关注的 GitHub 仓库 releases 更新"
    
    @classmethod
    def get_version_info(cls) -> str:
        """获取版本信息字符串"""
        return f"{cls.NAME} v{cls.VERSION} ({cls.BUILD_DATE})"
    
    @classmethod
    def get_copyright_info(cls) -> str:
        """获取版权信息字符串"""
        return f"{cls.COPYRIGHT} {cls.AUTHOR}"
    
    @classmethod
    def get_full_info(cls) -> str:
        """获取完整的项目信息"""
        info = [
            f"{cls.NAME} v{cls.VERSION}",
            f"构建日期: {cls.BUILD_DATE}",
            f"作者: {cls.AUTHOR}",
            f"许可证: {cls.LICENSE}",
            f"版权: {cls.COPYRIGHT}",
            f"项目主页: {cls.URL}",
            f"维护者邮箱: {cls.MAINTAINER_EMAIL}",
            f"描述: {cls.DESCRIPTION}"
        ]
        return "\n".join(info)
    
    @classmethod
    def get_about_html(cls) -> str:
        """获取关于信息的HTML格式"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Microsoft YaHei', sans-serif; margin: 20px; }}
                h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .info {{ margin: 10px 0; }}
                .label {{ color: #7f8c8d; font-weight: bold; width: 100px; display: inline-block; }}
                .value {{ color: #2c3e50; }}
                .version {{ font-size: 24px; color: #3498db; margin: 20px 0; }}
                .copyright {{ margin-top: 30px; color: #95a5a6; font-size: 12px; text-align: center; }}
            </style>
        </head>
        <body>
            <h2>{cls.NAME}</h2>
            <div class="version">{cls.VERSION}</div>
            <div class="info"><span class="label">构建日期</span><span class="value">{cls.BUILD_DATE}</span></div>
            <div class="info"><span class="label">作者</span><span class="value">{cls.AUTHOR}</span></div>
            <div class="info"><span class="label">许可证</span><span class="value">{cls.LICENSE}</span></div>
            <div class="info"><span class="label">项目主页</span><span class="value"><a href="{cls.URL}">{cls.URL}</a></span></div>
            <div class="info"><span class="label">描述</span><span class="value">{cls.DESCRIPTION}</span></div>
            <div class="copyright">{cls.COPYRIGHT}</div>
        </body>
        </html>
        """
        return html
    
    @classmethod
    def check_for_updates(cls) -> bool:
        """
        检查是否有新版本
        返回True表示有新版本，False表示已是最新
        """
        try:
            import requests
            # 这里可以实现从GitHub检查最新版本的逻辑
            # 例如：从GitHub API获取最新的release版本
            url = f"https://api.github.com/repos/duma520/{cls.NAME}/releases/latest"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                latest_version = response.json().get('tag_name', '').lstrip('v')
                current = [int(x) for x in cls.VERSION.split('.')]
                latest = [int(x) for x in latest_version.split('.')]
                return latest > current
        except:
            pass
        return False
    
    @classmethod
    def get_update_message(cls) -> str:
        """获取更新提示信息"""
        if cls.check_for_updates():
            return f"发现新版本！当前版本: {cls.VERSION}，请访问 {cls.URL}/releases 下载最新版本。"
        return f"当前已是最新版本: {cls.VERSION}"
    
    @classmethod
    def save_to_file(cls, filepath: str):
        """将项目信息保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cls.get_full_info())
    
    @classmethod
    def get_database_info(cls) -> Dict:
        """获取数据库相关信息"""
        import os
        import hashlib
        
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
        users_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")
        
        return {
            'database_dir': db_dir,
            'backup_dir': backup_dir,
            'users_dir': users_dir,
            'database_pattern': 'user_*.db',
            'hash_algorithm': 'md5',
            'hash_length': 16
        }
    
    @classmethod
    def get_system_requirements(cls) -> Dict:
        """获取系统要求"""
        return {
            'python': '>=3.8',
            'pyside6': '>=6.0.0',
            'requests': '>=2.25.0',
            'pypinyin': '>=0.50.0',
            'memory': '>=512MB',
            'disk': '>=100MB'
        }
    
    @classmethod
    def print_info(cls):
        """打印项目信息到控制台"""
        print("=" * 60)
        print(cls.get_full_info())
        print("=" * 60)


# 如果您想在主窗口的某个地方显示关于信息，可以添加一个关于对话框
class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"关于 {ProjectInfo.NAME}")
        self.setMinimumSize(500, 400)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel(ProjectInfo.NAME)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db; margin: 10px;")
        layout.addWidget(title_label)
        
        # 版本
        version_label = QLabel(f"版本 {ProjectInfo.VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 14px; color: #2c3e50; margin: 5px;")
        layout.addWidget(version_label)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(line)
        
        # 信息表格
        info_widget = QWidget()
        info_layout = QGridLayout(info_widget)
        info_layout.setVerticalSpacing(10)
        
        # 添加信息行
        info_items = [
            ("构建日期", ProjectInfo.BUILD_DATE),
            ("作者", ProjectInfo.AUTHOR),
            ("许可证", ProjectInfo.LICENSE),
            ("项目主页", f'<a href="{ProjectInfo.URL}">{ProjectInfo.URL}</a>'),
            ("描述", ProjectInfo.DESCRIPTION)
        ]
        
        for row, (label, value) in enumerate(info_items):
            label_item = QLabel(f"{label}:")
            label_item.setStyleSheet("font-weight: bold; color: #7f8c8d;")
            label_item.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            info_layout.addWidget(label_item, row, 0)
            
            value_item = QLabel(value)
            value_item.setStyleSheet("color: #2c3e50;")
            value_item.setOpenExternalLinks(True)
            value_item.setTextFormat(Qt.RichText if 'http' in value else Qt.PlainText)
            info_layout.addWidget(value_item, row, 1)
        
        info_layout.setColumnStretch(1, 1)
        layout.addWidget(info_widget)
        
        # 版权
        copyright_label = QLabel(ProjectInfo.COPYRIGHT)
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #95a5a6; margin-top: 20px;")
        layout.addWidget(copyright_label)
        
        # 更新检查
        update_layout = QHBoxLayout()
        update_label = QLabel("更新状态:")
        update_layout.addWidget(update_label)
        
        self.update_status = QLabel("正在检查更新...")
        update_layout.addWidget(self.update_status)
        update_layout.addStretch()
        
        self.check_update_btn = QPushButton("检查更新")
        self.check_update_btn.clicked.connect(self.check_for_updates)
        update_layout.addWidget(self.check_update_btn)
        
        layout.addLayout(update_layout)
        
        # 按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)
        
        # 检查更新
        QTimer.singleShot(100, self.check_for_updates)
    
    def check_for_updates(self):
        """检查更新"""
        self.update_status.setText("正在检查...")
        self.check_update_btn.setEnabled(False)
        
        # 使用线程检查更新，避免阻塞UI
        class UpdateCheckThread(QThread):
            finished = Signal(bool, str)
            
            def run(self):
                try:
                    has_update = ProjectInfo.check_for_updates()
                    if has_update:
                        self.finished.emit(True, "发现新版本！")
                    else:
                        self.finished.emit(False, "已是最新版本")
                except:
                    self.finished.emit(False, "检查失败")
        
        self.update_thread = UpdateCheckThread()
        self.update_thread.finished.connect(self.on_update_check_finished)
        self.update_thread.start()
    
    def on_update_check_finished(self, has_update: bool, message: str):
        """更新检查完成"""
        if has_update:
            self.update_status.setText(f'<span style="color: #e74c3c;">{message}</span>')
        else:
            self.update_status.setText(f'<span style="color: #27ae60;">{message}</span>')
        self.check_update_btn.setEnabled(True)


# 您可以在主窗口的菜单或按钮中添加打开关于对话框的方法
def show_about_dialog(parent=None):
    """显示关于对话框"""
    dialog = AboutDialog(parent)
    dialog.exec()

# ==================== 配置类 ====================
@dataclass
class AppConfig:
    """应用程序配置"""
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 20808
    use_proxy: bool = True
    check_interval: int = 3600  # 秒
    backup_count: int = 30
    debug_mode: bool = False
    window_geometry: bytes = b''
    window_state: bytes = b''


@dataclass
class Repository:
    """仓库信息"""
    id: int = 0
    name: str = ""
    full_name: str = ""
    url: str = ""
    last_check: str = ""
    last_version: str = ""
    current_version: str = ""
    watch_enabled: bool = True
    created_at: str = ""
    updated_at: str = ""


@dataclass
class ReleaseInfo:
    """Release 信息"""
    id: int = 0
    repo_id: int = 0
    version: str = ""
    name: str = ""
    published_at: str = ""
    url: str = ""
    body: str = ""
    is_new: bool = False


# ==================== 枚举类 ====================
class BackupType(Enum):
    """备份类型"""
    AUTO = "自动"
    MANUAL = "手动"
    ROLLBACK = "回滚"
    PRE_RESTORE = "恢复前备份"


# ==================== OPML导入器 ====================
class OPMLImporter:
    """OPML文件导入器 - 用于导入GitHub Releases订阅源"""
    
    @staticmethod
    def parse_opml(file_path: str) -> List[Dict]:
        """
        解析OPML文件，提取GitHub Releases订阅源
        
        Args:
            file_path: OPML文件路径
            
        Returns:
            仓库信息列表，每个仓库包含full_name和url
        """
        repos = []
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # 查找所有outline元素
            for outline in root.findall(".//outline"):
                xml_url = outline.get('xmlUrl') or outline.get('xmlurl') or outline.get('xmlURL')
                html_url = outline.get('htmlUrl') or outline.get('htmlurl') or outline.get('htmlURL')
                text = outline.get('text') or outline.get('title') or ''
                
                # 提取GitHub Releases信息
                repo_info = OPMLImporter._extract_github_repo(xml_url, html_url, text)
                if repo_info:
                    repos.append(repo_info)
                    
        except ET.ParseError as e:
            print(f"解析OPML文件失败: {e}")
        except Exception as e:
            print(f"处理OPML文件时出错: {e}")
            
        return repos
    
    @staticmethod
    def _extract_github_repo(xml_url: str, html_url: str, text: str) -> Optional[Dict]:
        """
        从OPML条目中提取GitHub仓库信息
        
        支持的URL格式:
        - https://github.com/用户名/仓库名/releases
        - https://github.com/用户名/仓库名/releases.atom
        - https://github.com/用户名/仓库名/releases/tag/v1.0.0
        """
        result = None
        
        # 优先从xmlUrl提取
        if xml_url:
            result = OPMLImporter._parse_github_url(xml_url)
            
        # 如果xmlUrl没提取到，尝试htmlUrl
        if not result and html_url:
            result = OPMLImporter._parse_github_url(html_url)
            
        # 如果都没提取到，尝试从text中提取
        if not result and text and 'github.com' in text:
            # 尝试从文本中提取用户名/仓库名
            import re
            match = re.search(r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)', text)
            if match:
                full_name = match.group(1)
                result = {
                    'full_name': full_name,
                    'url': f"https://github.com/{full_name}/releases",
                    'name': full_name.split('/')[-1]
                }
                
        return result
    
    @staticmethod
    def _parse_github_url(url: str) -> Optional[Dict]:
        """
        解析GitHub URL，提取仓库信息
        """
        if not url or 'github.com' not in url:
            return None
            
        # 移除URL中的协议和域名部分
        parts = url.split('github.com/')
        if len(parts) < 2:
            return None
            
        path = parts[1].strip('/')
        
        # 处理不同URL格式
        # 格式: 用户名/仓库名/releases/...
        path_parts = path.split('/')
        
        if len(path_parts) >= 2:
            username = path_parts[0]
            reponame = path_parts[1]
            
            # 验证用户名和仓库名格式
            if username and reponame and not any(c in username + reponame for c in '?=&#%'):
                full_name = f"{username}/{reponame}"
                return {
                    'full_name': full_name,
                    'url': f"https://github.com/{full_name}/releases",
                    'name': reponame
                }
                
        return None
    
    @staticmethod
    def create_sample_opml(file_path: str):
        """
        创建示例OPML文件
        """
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>GitHub Releases 订阅源</title>
    </head>
    <body>
        <outline text="GitHub Releases" title="GitHub Releases">
            <outline type="rss" 
                    text="curl releases" 
                    title="curl releases" 
                    xmlUrl="https://github.com/curl/curl/releases.atom" 
                    htmlUrl="https://github.com/curl/curl/releases"/>
            <outline type="rss" 
                    text="FFmpeg releases" 
                    title="FFmpeg releases" 
                    xmlUrl="https://github.com/FFmpeg/FFmpeg/releases.atom" 
                    htmlUrl="https://github.com/FFmpeg/FFmpeg/releases"/>
            <outline type="rss" 
                    text"Node.js releases" 
                    title="Node.js releases" 
                    xmlUrl="https://github.com/nodejs/node/releases.atom" 
                    htmlUrl="https://github.com/nodejs/node/releases"/>
        </outline>
    </body>
</opml>'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)


# ==================== 导入OPML线程 ====================
class ImportOPMLThread(QThread):
    """导入OPML文件的线程"""
    
    progress = Signal(int, int)  # 当前进度, 总数
    log = Signal(str)  # 日志信息
    repo_found = Signal(dict)  # 发现仓库
    finished = Signal(int, int)  # 成功数量, 失败数量
    error = Signal(str)  # 错误信息
    
    def __init__(self, db_path: str, user_name: str, opml_file: str, 
                 proxy_host: str, proxy_port: int, use_proxy: bool, token: str = None):
        super().__init__()
        self.db_path = db_path
        self.user_name = user_name
        self.opml_file = opml_file
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.use_proxy = use_proxy
        self.token = token
        # 为每个线程创建独立的GitHub客户端
        self.github_client = GitHubClient(proxy_host, proxy_port, use_proxy, token)
        self._is_running = True
        self.thread_db = None
        self.success_count = 0
        self.fail_count = 0
    
    def get_thread_db(self):
        """获取当前线程的数据库连接"""
        if self.thread_db is None:
            self.thread_db = DatabaseManager(self.user_name)
            self.thread_db.connect()
        return self.thread_db
    
    def run(self):
        """运行线程"""
        try:
            self.log.emit("开始解析OPML文件...")
            
            # 解析OPML文件
            repos = OPMLImporter.parse_opml(self.opml_file)
            
            if not repos:
                self.log.emit("OPML文件中未找到GitHub仓库")
                self.finished.emit(0, 0)
                return
            
            self.log.emit(f"找到 {len(repos)} 个GitHub仓库，开始验证...")
            
            total = len(repos)
            for i, repo_info in enumerate(repos):
                if not self._is_running:
                    break
                
                self.progress.emit(i + 1, total)
                self.log.emit(f"验证: {repo_info['full_name']}")
                
                # 验证仓库是否存在
                exists = self.github_client.check_repo_exists(repo_info['full_name'])
                
                if exists:
                    # 保存到数据库
                    if self._save_repo(repo_info):
                        self.success_count += 1
                        self.repo_found.emit(repo_info)
                        self.log.emit(f"✓ 添加成功: {repo_info['full_name']}")
                    else:
                        self.fail_count += 1
                        self.log.emit(f"✗ 保存失败: {repo_info['full_name']} (可能已存在)")
                else:
                    self.fail_count += 1
                    print(f"仓库不存在: {repo_info['full_name']}")
                    self.log.emit(f"✗ 仓库不存在: {repo_info['full_name']}")
                
                # 避免请求过快
                time.sleep(0.5)
            
            self.log.emit(f"导入完成: 成功 {self.success_count} 个, 失败 {self.fail_count} 个")
            self.finished.emit(self.success_count, self.fail_count)
            
        except Exception as e:
            self.error.emit(str(e))
        finally:
            if self.thread_db:
                self.thread_db.close()
    
    def _save_repo(self, repo_info: Dict) -> bool:
        """保存仓库到数据库"""
        try:
            db = self.get_thread_db()
            now = datetime.now().isoformat()
            
            db.execute(
                """
                INSERT OR IGNORE INTO repositories 
                (name, full_name, url, created_at, updated_at, watch_enabled)
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (
                    repo_info['name'],
                    repo_info['full_name'],
                    repo_info['url'],
                    now,
                    now
                )
            )
            db.commit()
            return True
            
        except sqlite3.IntegrityError:
            # 仓库已存在
            return False
        except Exception as e:
            print(f"保存仓库失败: {e}")
            return False
    
    def stop(self):
        """停止线程"""
        self._is_running = False


# ==================== 数据库管理器 ====================
class DatabaseManager:
    """数据库管理器 - 每个用户独立数据库"""
    
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.db_path = self._get_db_path()
        self.connection = None
        self._init_database()
    
    def _get_db_path(self) -> str:
        """获取数据库路径"""
        # 对用户名进行哈希处理，避免非法文件名
        hash_name = hashlib.md5(self.user_name.encode()).hexdigest()[:16]
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, f"user_{hash_name}.db")
    
    def _init_database(self):
        """初始化数据库"""
        self.connect()
        try:
            # 开启 WAL 模式
            self.connection.execute("PRAGMA journal_mode=WAL")
            
            # 创建仓库表
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    full_name TEXT NOT NULL UNIQUE,
                    url TEXT NOT NULL,
                    last_check TEXT,
                    last_version TEXT,
                    current_version TEXT,
                    watch_enabled INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # 创建 releases 表
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS releases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_id INTEGER NOT NULL,
                    version TEXT NOT NULL,
                    name TEXT,
                    published_at TEXT NOT NULL,
                    url TEXT,
                    body TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (repo_id) REFERENCES repositories(id) ON DELETE CASCADE,
                    UNIQUE(repo_id, version)
                )
            """)
            
            # 创建索引
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_releases_repo_id 
                ON releases(repo_id)
            """)
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_releases_published_at 
                ON releases(published_at)
            """)
            
            self.connection.commit()
        except Exception as e:
            print(f"初始化数据库失败: {e}")
            raise
    
    def connect(self):
        """连接数据库"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, timeout=30)
            self.connection.row_factory = sqlite3.Row
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            try:
                # 先提交任何未完成的事务
                self.connection.commit()
                # 关闭连接
                self.connection.close()
                print(f"数据库连接已关闭: {self.db_path}")
            except Exception as e:
                print(f"关闭数据库连接时出错: {e}")
            finally:
                self.connection = None
    
    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL"""
        self.connect()
        return self.connection.execute(sql, params)
    
    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """回滚事务"""
        if self.connection:
            self.connection.rollback()
    
    def get_backup_path(self) -> str:
        """获取备份文件路径"""
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups", self.user_name)
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir
    
    def create_backup(self, backup_type: BackupType) -> str:
        """创建备份"""
        backup_dir = self.get_backup_path()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{backup_type.value}_{timestamp}.db")
        
        # 创建备份
        self.connect()
        self.connection.commit()
        self.connection.execute(f"VACUUM INTO '{backup_file}'")
        
        return backup_file
    
    def restore_backup(self, backup_file: str) -> bool:
        """恢复备份"""
        try:
            # 关闭当前连接
            self.close()
            
            # 复制备份文件
            shutil.copy2(backup_file, self.db_path)
            
            # 重新连接
            self.connect()
            
            return True
        except Exception as e:
            print(f"恢复备份失败: {e}")
            return False
    
    def get_all_backups(self) -> List[Dict]:
        """获取所有备份文件信息"""
        backup_dir = self.get_backup_path()
        backups = []
        
        if not os.path.exists(backup_dir):
            return backups
        
        for filename in os.listdir(backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                
                # 解析备份类型
                backup_type = BackupType.AUTO.value
                if filename.startswith(BackupType.MANUAL.value):
                    backup_type = BackupType.MANUAL.value
                elif filename.startswith(BackupType.ROLLBACK.value):
                    backup_type = BackupType.ROLLBACK.value
                elif filename.startswith(BackupType.PRE_RESTORE.value):
                    backup_type = BackupType.PRE_RESTORE.value
                
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    'type': backup_type
                })
        
        # 按时间排序
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 30):
        """清理旧备份"""
        backups = self.get_all_backups()
        if len(backups) <= keep_count:
            return
        
        # 删除多余的备份
        for backup in backups[keep_count:]:
            try:
                os.remove(backup['filepath'])
            except:
                pass
    
    def get_repo_releases_info(self, repo_id: int) -> List[Dict]:
        """获取仓库的 releases 信息"""
        cursor = self.execute(
            "SELECT version, published_at FROM releases WHERE repo_id = ? ORDER BY published_at DESC",
            (repo_id,)
        )
        releases = []
        for row in cursor.fetchall():
            releases.append({
                'version': row['version'],
                'published_at': row['published_at']
            })
        return releases

    def ensure_closed(self):
        """确保数据库连接已关闭（增强版）"""
        self.close()
        
        # 强制进行垃圾回收
        import gc
        gc.collect()
        
        # 再次确认连接已关闭
        if self.connection:
            try:
                # 如果还有连接，尝试强制关闭
                self.connection.close()
            except:
                pass
            finally:
                self.connection = None

# ==================== GitHub API 客户端 ====================
class GitHubClient:
    """GitHub API 客户端"""
    
    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 20808, 
                 use_proxy: bool = True, token: str = None):
        self.base_url = "https://api.github.com"
        self.token = token
        self.session = requests.Session()
        
        # 设置请求头
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Releases-Monitor/2.0'
        }
        
        # 如果有token，添加到请求头
        if token:
            headers['Authorization'] = f'token {token}'
            # 认证后的限制是5000次/小时
        else:
            # 未认证只有60次/小时
            print("警告：未使用GitHub Token，API速率限制为60次/小时")
        
        self.session.headers.update(headers)
        
        # 设置代理
        if use_proxy:
            proxy_url = f'http://{proxy_host}:{proxy_port}'
            self.session.proxies.update({
                'http': proxy_url,
                'https': proxy_url
            })
            print(f"使用代理: {proxy_url}")
    
    def get_releases(self, repo_full_name: str) -> List[Dict]:
        """获取仓库的 releases"""
        url = f"{self.base_url}/repos/{repo_full_name}/releases"
        try:
            response = self.session.get(url, timeout=10)
            
            # 处理速率限制
            if response.status_code == 403:
                reset_time = response.headers.get('X-RateLimit-Reset')
                remaining = response.headers.get('X-RateLimit-Remaining', '0')
                
                if reset_time and int(remaining) == 0:
                    # 计算需要等待的时间
                    wait_time = int(reset_time) - time.time()
                    print(f"速率限制达到，需要在 {wait_time:.0f} 秒后重试")
                    
                    # 返回空列表，但记录需要等待
                    return []
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"请求超时 {repo_full_name}")
            return []
        except requests.exceptions.ConnectionError as e:
            print(f"连接错误 {repo_full_name}: {e}")
            return []
        except Exception as e:
            print(f"获取 releases 失败 {repo_full_name}: {e}")
            return []

    def get_releases_with_backoff(self, repo_full_name: str, max_retries: int = 3) -> List[Dict]:
        """带退避重试的获取releases"""
        for attempt in range(max_retries):
            result = self.get_releases(repo_full_name)
            
            # 如果是因为速率限制返回空列表，等待后重试
            if not result and attempt < max_retries - 1:
                wait_time = 2 ** attempt * 5  # 指数退避：5, 10, 20秒
                print(f"第{attempt + 1}次失败，等待{wait_time}秒后重试: {repo_full_name}")
                time.sleep(wait_time)
            else:
                return result
        
        return []

    def check_repo_exists(self, repo_full_name: str) -> bool:
        """检查仓库是否存在"""
        url = f"{self.base_url}/repos/{repo_full_name}"
        try:
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False


# ==================== 拼音转换工具 ====================
class PinyinConverter:
    """拼音转换工具"""
    
    @staticmethod
    def to_pinyin(text: str) -> str:
        """转换为拼音"""
        if not text:
            return ""
        
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # 中文字符
                pinyin_list = pypinyin.pinyin(char, style=pypinyin.NORMAL)
                if pinyin_list:
                    result.append(pinyin_list[0][0])
            else:
                result.append(char.lower())
        
        return ''.join(result)
    
    @staticmethod
    def to_first_letter(text: str) -> str:
        """转换为拼音首字母"""
        if not text:
            return ""
        
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # 中文字符
                pinyin_list = pypinyin.pinyin(char, style=pypinyin.FIRST_LETTER)
                if pinyin_list:
                    result.append(pinyin_list[0][0])
            else:
                result.append(char.lower())
        
        return ''.join(result)
    
    @staticmethod
    def matches(text: str, keyword: str) -> bool:
        """检查是否匹配（支持中文、英文、拼音首字母）"""
        if not keyword:
            return True
        
        keyword = keyword.lower().strip()
        text_lower = text.lower()
        
        # 直接匹配
        if keyword in text_lower:
            return True
        
        # 拼音匹配
        pinyin = PinyinConverter.to_pinyin(text)
        if keyword in pinyin:
            return True
        
        # 拼音首字母匹配
        first_letter = PinyinConverter.to_first_letter(text)
        if keyword in first_letter:
            return True
        
        return False


# ==================== 工作线程 ====================
class CheckUpdatesThread(QThread):
    """检查更新线程"""
    
    progress = Signal(int, int)  # 当前进度, 总数
    log = Signal(str)  # 日志信息
    finished = Signal(list)  # 更新列表
    error = Signal(str)  # 错误信息
    
    def __init__(self, db: DatabaseManager, config: AppConfig):
        super().__init__()
        self.db_path = db.db_path  # 只保存数据库路径，不保存连接
        self.user_name = db.user_name
        self.config = config
        self.client = GitHubClient(config.proxy_host, config.proxy_port, config.use_proxy)
        self._is_running = True
        self.thread_db = None  # 线程本地数据库连接
    
    def get_thread_db(self):
        """获取当前线程的数据库连接"""
        if self.thread_db is None:
            self.thread_db = DatabaseManager(self.user_name)
            # 使用已有的数据库文件，不重新初始化
            self.thread_db.connect()
        return self.thread_db
    
    def run(self):
        """运行线程"""
        try:
            # 获取线程本地的数据库连接
            db = self.get_thread_db()
            
            # 获取所有启用的仓库
            cursor = db.execute(
                "SELECT * FROM repositories WHERE watch_enabled = 1 ORDER BY name"
            )
            repos = cursor.fetchall()
            
            if not repos:
                self.log.emit("没有需要检查的仓库")
                self.finished.emit([])
                return
            
            updates = []
            total = len(repos)
            
            # 记录速率限制信息
            rate_limited = False
            rate_limit_reset = None
            
            for i, repo in enumerate(repos):
                if not self._is_running:
                    break
                
                # 如果遇到速率限制，暂停检查
                if rate_limited and rate_limit_reset:
                    now = time.time()
                    if now < rate_limit_reset:
                        wait_time = rate_limit_reset - now
                        self.log.emit(f"达到API速率限制，等待 {wait_time:.0f} 秒...")
                        
                        # 分段等待，以便能响应停止信号
                        while wait_time > 0 and self._is_running:
                            time.sleep(min(1, wait_time))
                            wait_time -= 1
                        
                        if not self._is_running:
                            break
                        
                        rate_limited = False
                        rate_limit_reset = None
                
                self.progress.emit(i + 1, total)
                self.log.emit(f"检查: {repo['full_name']}")
                
                # 使用带退避的获取方法
                releases = self.client.get_releases_with_backoff(repo['full_name'])
                
                # 检查是否遇到速率限制
                if not releases:
                    # 检查响应头
                    if hasattr(self.client.session, 'last_response'):
                        headers = self.client.session.last_response.headers
                        remaining = headers.get('X-RateLimit-Remaining', '0')
                        
                        if remaining == '0':
                            reset_time = headers.get('X-RateLimit-Reset')
                            if reset_time:
                                rate_limited = True
                                rate_limit_reset = int(reset_time)
                                self.log.emit(f"⚠ API速率限制达到，将在 {datetime.fromtimestamp(int(reset_time)).strftime('%H:%M:%S')} 后继续")
                
                if releases:
                    latest = releases[0]
                    latest_version = latest.get('tag_name', '')
                    
                    # 检查是否有新版本
                    if latest_version != repo['current_version']:
                        # 保存新版本信息
                        self._save_releases(db, repo['id'], releases)
                        
                        # 更新仓库信息
                        db.execute(
                            """
                            UPDATE repositories 
                            SET last_version = current_version,
                                current_version = ?,
                                last_check = ?,
                                updated_at = ?
                            WHERE id = ?
                            """,
                            (latest_version, datetime.now().isoformat(), 
                             datetime.now().isoformat(), repo['id'])
                        )
                        db.commit()
                        
                        updates.append({
                            'repo': dict(repo),
                            'old_version': repo['current_version'],
                            'new_version': latest_version,
                            'releases': releases[:5]  # 最近5个版本
                        })
                        
                        self.log.emit(f"✓ 发现更新: {repo['name']} {repo['current_version']} -> {latest_version}")
                    else:
                        # 只更新检查时间
                        db.execute(
                            "UPDATE repositories SET last_check = ? WHERE id = ?",
                            (datetime.now().isoformat(), repo['id'])
                        )
                        db.commit()
                        self.log.emit(f"  已是最新: {repo['name']} {latest_version}")
                else:
                    self.log.emit(f"✗ 没有获取到 releases: {repo['full_name']}")
                
                # 动态调整请求间隔
                time.sleep(2)  # 基础间隔
            
            self.progress.emit(total, total)
            self.log.emit("检查完成")
            self.finished.emit(updates)
            
        except Exception as e:
            self.error.emit(str(e))
        finally:
            # 关闭线程本地的数据库连接
            if self.thread_db:
                self.thread_db.close()
    
    def _save_releases(self, db: DatabaseManager, repo_id: int, releases: List[Dict]):
        """保存 releases 信息"""
        now = datetime.now().isoformat()
        
        for release in releases:
            try:
                db.execute(
                    """
                    INSERT OR REPLACE INTO releases 
                    (repo_id, version, name, published_at, url, body, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        repo_id,
                        release.get('tag_name', ''),
                        release.get('name', ''),
                        release.get('published_at', now),
                        release.get('html_url', ''),
                        release.get('body', ''),
                        now
                    )
                )
            except Exception as e:
                print(f"保存 release 失败: {e}")
        
        db.commit()
    
    def stop(self):
        """停止线程"""
        self._is_running = False


# ==================== 搜索线程 ====================
class SearchThread(QThread):
    """搜索线程"""
    
    result = Signal(list)  # 搜索结果
    finished = Signal()
    
    def __init__(self, db: DatabaseManager, keyword: str):
        super().__init__()
        self.db_path = db.db_path  # 只保存数据库路径
        self.user_name = db.user_name
        self.keyword = keyword
        self.thread_db = None  # 线程本地数据库连接
    
    def get_thread_db(self):
        """获取当前线程的数据库连接"""
        if self.thread_db is None:
            self.thread_db = DatabaseManager(self.user_name)
            self.thread_db.connect()
        return self.thread_db
    
    def run(self):
        """运行线程"""
        try:
            # 获取线程本地的数据库连接
            db = self.get_thread_db()
            
            results = []
            
            # 搜索仓库
            cursor = db.execute(
                "SELECT * FROM repositories ORDER BY name"
            )
            all_repos = cursor.fetchall()
            
            for repo in all_repos:
                repo_dict = dict(repo)
                
                # 检查是否匹配
                if PinyinConverter.matches(repo_dict['name'], self.keyword) or \
                   PinyinConverter.matches(repo_dict['full_name'], self.keyword):
                    
                    # 获取最新的 release
                    release_cursor = db.execute(
                        "SELECT * FROM releases WHERE repo_id = ? ORDER BY published_at DESC LIMIT 1",
                        (repo_dict['id'],)
                    )
                    latest_release = release_cursor.fetchone()
                    
                    repo_dict['latest_release'] = dict(latest_release) if latest_release else None
                    results.append(repo_dict)
            
            self.result.emit(results)
            self.finished.emit()
            
        except Exception as e:
            print(f"搜索失败: {e}")
            self.finished.emit()
        finally:
            # 关闭线程本地的数据库连接
            if self.thread_db:
                self.thread_db.close()


# ==================== 验证仓库线程 ====================
class ValidateRepoThread(QThread):
    """验证仓库线程"""
    
    finished = Signal(bool, str)  # 成功标志, 消息
    log = Signal(str)
    
    def __init__(self, github_client, repo_full_name):
        super().__init__()
        self.github_client = github_client
        self.repo_full_name = repo_full_name
    
    def run(self):
        """运行线程"""
        try:
            exists = self.github_client.check_repo_exists(self.repo_full_name)
            
            if exists:
                self.finished.emit(True, self.repo_full_name)
            else:
                self.finished.emit(False, f"仓库不存在或无法访问: {self.repo_full_name}")
                
        except Exception as e:
            self.finished.emit(False, f"验证仓库失败: {str(e)}")
            self.log.emit(f"验证仓库失败: {e}")


# ==================== 备份恢复对话框 ====================
class BackupRestoreDialog(QDialog):
    """备份恢复对话框"""
    
    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db = db
        self.selected_backup = None
        self.setWindowTitle("数据库恢复")
        self.setMinimumSize(800, 500)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()
        self.load_backups()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 筛选栏
        filter_layout = QHBoxLayout()
        
        # 时间范围筛选
        filter_layout.addWidget(QLabel("时间范围:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("至"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        filter_layout.addWidget(self.end_date)
        
        # 类型筛选
        filter_layout.addWidget(QLabel("备份类型:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["全部", "自动", "手动", "回滚", "恢复前备份"])
        filter_layout.addWidget(self.type_filter)
        
        # 筛选按钮
        self.filter_btn = QPushButton("筛选")
        self.filter_btn.clicked.connect(self.load_backups)
        filter_layout.addWidget(self.filter_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧备份列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        left_layout.addWidget(QLabel("备份列表:"))
        
        self.backup_table = QTableWidget()
        self.backup_table.setColumnCount(4)
        self.backup_table.setHorizontalHeaderLabels(["备份时间", "类型", "大小", "操作"])
        self.backup_table.horizontalHeader().setStretchLastSection(False)
        self.backup_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.backup_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.backup_table.itemClicked.connect(self.on_backup_selected)
        
        left_layout.addWidget(self.backup_table)
        splitter.addWidget(left_widget)
        
        # 右侧预览
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addWidget(QLabel("详细信息预览:"))
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        right_layout.addWidget(self.preview_text)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter, 1)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.restore_btn = QPushButton("恢复选中备份")
        self.restore_btn.setEnabled(False)
        self.restore_btn.clicked.connect(self.restore_backup)
        button_layout.addWidget(self.restore_btn)
        
        button_layout.addStretch()
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def load_backups(self):
        """加载备份列表"""
        backups = self.db.get_all_backups()
        
        # 应用筛选
        start_date = self.start_date.date().toPython()
        end_date = self.end_date.date().toPython() + timedelta(days=1)
        
        filtered_backups = []
        for backup in backups:
            backup_date = datetime.strptime(backup['created'], "%Y-%m-%d %H:%M:%S")
            
            # 时间筛选
            if backup_date.date() < start_date or backup_date.date() >= end_date:
                continue
            
            # 类型筛选
            type_index = self.type_filter.currentIndex()
            if type_index > 0:
                type_text = self.type_filter.currentText()
                if backup['type'] != type_text:
                    continue
            
            filtered_backups.append(backup)
        
        # 显示备份列表
        self.backup_table.setRowCount(len(filtered_backups))
        
        for i, backup in enumerate(filtered_backups):
            # 备份时间
            time_item = QTableWidgetItem(backup['created'])
            self.backup_table.setItem(i, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(backup['type'])
            self.backup_table.setItem(i, 1, type_item)
            
            # 大小
            size_str = self.format_size(backup['size'])
            size_item = QTableWidgetItem(size_str)
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.backup_table.setItem(i, 2, size_item)
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            
            preview_btn = QPushButton("预览")
            preview_btn.clicked.connect(lambda checked, b=backup: self.preview_backup(b))
            btn_layout.addWidget(preview_btn)
            
            self.backup_table.setCellWidget(i, 3, btn_widget)
        
        # 调整列宽
        self.backup_table.resizeColumnsToContents()
        self.backup_table.horizontalHeader().setStretchLastSection(True)
    
    def format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def on_backup_selected(self, item):
        """选择备份"""
        row = item.row()
        self.selected_backup = row
        self.restore_btn.setEnabled(True)
        
        # 获取备份文件信息
        type_item = self.backup_table.item(row, 0)
        if type_item:
            # 预览选中的备份
            pass
    
    def preview_backup(self, backup: Dict):
        """预览备份"""
        self.preview_text.clear()
        
        # 读取备份文件信息
        try:
            # 连接备份数据库
            conn = sqlite3.connect(backup['filepath'])
            conn.row_factory = sqlite3.Row
            
            # 获取仓库信息
            cursor = conn.execute("SELECT COUNT(*) as count FROM repositories")
            repo_count = cursor.fetchone()['count']
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM releases")
            release_count = cursor.fetchone()['count']
            
            # 获取最早的 release
            cursor = conn.execute("""
                SELECT MIN(published_at) as earliest, MAX(published_at) as latest 
                FROM releases
            """)
            date_range = cursor.fetchone()
            
            conn.close()
            
            # 显示信息
            info = f"""【备份文件信息】
文件名: {backup['filename']}
创建时间: {backup['created']}
文件大小: {self.format_size(backup['size'])}
备份类型: {backup['type']}

【数据统计】
仓库数量: {repo_count}
Release数量: {release_count}

【Release时间范围】
最早: {date_range['earliest'] if date_range['earliest'] else '无'}
最新: {date_range['latest'] if date_range['latest'] else '无'}"""
            
            self.preview_text.setText(info)
            
        except Exception as e:
            self.preview_text.setText(f"读取备份信息失败: {e}")
    
    def restore_backup(self):
        """恢复备份"""
        if self.selected_backup is None:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self, "确认恢复",
            "恢复备份将覆盖当前数据库，是否继续？\n\n系统会自动备份当前数据用于回滚。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 获取选中的备份文件
        type_item = self.backup_table.item(self.selected_backup, 0)
        if not type_item:
            return
        
        # 创建恢复前备份
        try:
            self.parent().status_bar.showMessage("正在创建恢复前备份...")
            rollback_file = self.db.create_backup(BackupType.PRE_RESTORE)
            
            # 执行恢复
            self.parent().status_bar.showMessage("正在恢复数据库...")
            if self.db.restore_backup(type_item.data(Qt.UserRole)):
                QMessageBox.information(self, "恢复成功", "数据库恢复成功！")
                self.accept()
            else:
                QMessageBox.critical(self, "恢复失败", "数据库恢复失败！")
        
        except Exception as e:
            QMessageBox.critical(self, "恢复失败", f"恢复过程中出现错误: {e}")


# ==================== 用户管理对话框 ====================
class UserManagerDialog(QDialog):
    """用户管理对话框"""
    
    users_changed = Signal()
    
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user  # 当前登录的用户名
        self.setWindowTitle("用户管理")
        self.setMinimumSize(400, 500)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.users_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")
        os.makedirs(self.users_dir, exist_ok=True)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 用户列表
        layout.addWidget(QLabel("用户列表:"))
        
        self.user_list = QListWidget()
        self.user_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.user_list.itemDoubleClicked.connect(self.edit_user)
        layout.addWidget(self.user_list)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("添加用户")
        self.add_btn.clicked.connect(self.add_user)
        btn_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("修改用户名")
        self.edit_btn.clicked.connect(self.edit_user)
        btn_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("删除用户")
        self.delete_btn.clicked.connect(self.delete_user)
        btn_layout.addWidget(self.delete_btn)
        
        btn_layout.addStretch()
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
    
    def load_users(self):
        """加载用户列表"""
        self.user_list.clear()
        
        # 读取用户配置文件
        users_file = os.path.join(self.users_dir, "users.json")
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', encoding='utf-8') as f:
                    users = json.load(f)
                    for user in users:
                        self.user_list.addItem(user['name'])
            except:
                pass
    
    def save_users(self):
        """保存用户列表"""
        users = []
        for i in range(self.user_list.count()):
            users.append({'name': self.user_list.item(i).text()})
        
        users_file = os.path.join(self.users_dir, "users.json")
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    
    def add_user(self):
        """添加用户"""
        name, ok = QInputDialog.getText(self, "添加用户", "请输入用户名:")
        if ok and name.strip():
            # 检查是否已存在
            for i in range(self.user_list.count()):
                if self.user_list.item(i).text() == name:
                    QMessageBox.warning(self, "警告", "用户名已存在！")
                    return
            
            self.user_list.addItem(name)
            self.save_users()
            self.users_changed.emit()
    
    def edit_user(self):
        """编辑用户"""
        current = self.user_list.currentItem()
        if not current:
            QMessageBox.information(self, "提示", "请先选择一个用户")
            return
        
        old_name = current.text()
        new_name, ok = QInputDialog.getText(self, "修改用户名", "请输入新用户名:", text=old_name)
        
        if ok and new_name.strip() and new_name != old_name:
            # 检查是否已存在
            for i in range(self.user_list.count()):
                if self.user_list.item(i).text() == new_name:
                    QMessageBox.warning(self, "警告", "用户名已存在！")
                    return
            
            try:
                # 关键修复：确保所有数据库连接都已关闭
                
                # 1. 如果当前用户就是要修改的用户，先关闭主窗口的数据库连接
                main_window = self.parent()
                if isinstance(main_window, MainWindow) and main_window.user_name == old_name:
                    print(f"正在关闭当前用户 {old_name} 的数据库连接...")
                    
                    # 停止所有后台线程
                    main_window.stop_all_threads()
                    
                    # 关闭数据库连接
                    if main_window.db:
                        main_window.db.close()
                        main_window.db = None
                        print("主窗口数据库连接已关闭")
                    
                    # 等待一小段时间确保文件句柄释放
                    time.sleep(0.5)
                
                # 2. 创建数据库管理器实例并确保连接关闭
                old_db = DatabaseManager(old_name)
                old_db.close()  # 确保连接关闭
                print(f"旧数据库管理器连接已关闭: {old_db.db_path}")
                
                # 再次等待确保文件句柄释放
                time.sleep(0.2)
                
                # 3. 重命名数据库文件
                if os.path.exists(old_db.db_path):
                    new_db = DatabaseManager(new_name)
                    print(f"重命名数据库: {old_db.db_path} -> {new_db.db_path}")
                    shutil.move(old_db.db_path, new_db.db_path)
                    print("数据库文件重命名成功")
                
                # 4. 重命名备份目录
                old_backup = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups", old_name)
                new_backup = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups", new_name)
                if os.path.exists(old_backup):
                    print(f"重命名备份目录: {old_backup} -> {new_backup}")
                    shutil.move(old_backup, new_backup)
                    print("备份目录重命名成功")
                
                # 5. 更新用户列表
                current.setText(new_name)
                self.save_users()
                
                # 6. 如果修改的是当前用户，重新初始化主窗口
                if isinstance(main_window, MainWindow) and main_window.user_name == old_name:
                    print("重新初始化当前用户的数据连接...")
                    main_window.user_name = new_name
                    main_window.settings = QSettings("GitHubMonitor", new_name)
                    main_window.init_user_data()  # 重新初始化数据库连接
                    main_window.log(f"用户名已修改为: {new_name}")
                
                self.users_changed.emit()
                
                QMessageBox.information(self, "成功", f"用户 '{old_name}' 已成功修改为 '{new_name}'")
                
            except PermissionError as e:
                print(f"权限错误: {e}")
                error_msg = f"无法修改用户，文件被占用。\n错误: {e}\n\n可能的原因：\n1. 还有其他程序正在使用该数据库文件\n2. 数据库连接未完全关闭\n\n请尝试：\n1. 关闭程序后重试\n2. 手动重命名 {old_db.db_path} 文件"
                QMessageBox.critical(self, "错误", error_msg)
                
            except Exception as e:
                print(f"未知错误: {e}")
                QMessageBox.critical(self, "错误", f"修改用户失败: {e}")
    
    def delete_user(self):
        """删除用户"""
        current = self.user_list.currentItem()
        if not current:
            QMessageBox.information(self, "提示", "请先选择一个用户")
            return
        
        name = current.text()
        
        # 检查是否是当前登录用户
        if self.current_user and self.current_user == name:
            QMessageBox.warning(self, "警告", "不能删除当前登录的用户！")
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除用户 '{name}' 吗？\n该用户的所有数据将被永久删除！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                db = DatabaseManager(name)
                
                # 确保数据库连接已关闭
                db.close()
                
                # 等待一小段时间确保文件句柄释放
                time.sleep(0.1)
                
                # 删除数据库文件
                if os.path.exists(db.db_path):
                    os.remove(db.db_path)
                    print(f"已删除数据库文件: {db.db_path}")
                
                # 删除备份目录
                backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups", name)
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                    print(f"已删除备份目录: {backup_dir}")
                
                # 从列表中移除
                self.user_list.takeItem(self.user_list.row(current))
                self.save_users()
                self.users_changed.emit()
                
                QMessageBox.information(self, "成功", f"用户 '{name}' 已成功删除")
                
            except PermissionError as e:
                QMessageBox.critical(
                    self, "错误", 
                    f"无法删除用户，文件被占用。\n请确保没有其他程序使用该文件，然后重试。\n错误: {e}"
                )
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除用户失败: {e}")


# ==================== 登录对话框 ====================
class LoginDialog(QDialog):
    """登录对话框"""
    
    login_success = Signal(str)  # 用户名
    
    def __init__(self, parent=None, hide_current_user=False):
        super().__init__(parent)
        self.hide_current_user = hide_current_user  # 是否隐藏当前用户
        self.setWindowTitle("用户登录")
        self.setModal(True)
        self.setMinimumSize(300, 200)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.users_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")
        os.makedirs(self.users_dir, exist_ok=True)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_layout = QHBoxLayout()
        
        # 添加图标到标题
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
            title_layout.addWidget(icon_label)
        
        title = QLabel("GitHub Releases 监控系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        title_layout.addWidget(title)
        
        if os.path.exists(icon_path):
            # 添加一个占位符保持对称
            placeholder = QLabel()
            placeholder.setFixedSize(32, 32)
            title_layout.addWidget(placeholder)
        
        layout.addLayout(title_layout)
        
        # 用户选择
        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("选择用户:"), 0, 0)
        
        self.user_combo = QComboBox()
        self.user_combo.setEditable(False)
        form_layout.addWidget(self.user_combo, 0, 1)
        
        layout.addLayout(form_layout)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.login)
        self.login_btn.setEnabled(False)
        btn_layout.addWidget(self.login_btn)
        
        self.manage_btn = QPushButton("用户管理")
        self.manage_btn.clicked.connect(self.manage_users)
        btn_layout.addWidget(self.manage_btn)
        
        btn_layout.addStretch()
        
        self.exit_btn = QPushButton("退出")
        self.exit_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.exit_btn)
        
        layout.addLayout(btn_layout)
        
        # 状态提示
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
    
    def load_users(self):
        """加载用户列表"""
        self.user_combo.clear()
        
        users_file = os.path.join(self.users_dir, "users.json")
        current_user = None
        
        # 如果有父窗口且是主窗口，获取当前用户名
        if self.parent() and isinstance(self.parent(), MainWindow):
            current_user = self.parent().user_name
        
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', encoding='utf-8') as f:
                    users = json.load(f)
                    for user in users:
                        # 如果需要隐藏当前用户，且用户名等于当前用户，则跳过
                        if self.hide_current_user and current_user and user['name'] == current_user:
                            continue
                        self.user_combo.addItem(user['name'])
            except:
                pass
        
        if self.user_combo.count() > 0:
            self.login_btn.setEnabled(True)
            self.status_label.setText("")
        else:
            self.status_label.setText("请先添加用户")
    
    def login(self):
        """登录"""
        if self.user_combo.currentText():
            self.login_success.emit(self.user_combo.currentText())
            self.accept()
    
    def manage_users(self):
        """管理用户"""
        # 传入当前用户名（如果有父窗口且是主窗口）
        current_user = None
        if self.parent() and isinstance(self.parent(), MainWindow):
            current_user = self.parent().user_name
        
        dialog = UserManagerDialog(self, current_user=current_user)
        dialog.users_changed.connect(self.load_users)
        dialog.exec()
        self.load_users()


# ==================== 添加仓库对话框 ====================
class AddRepoDialog(QDialog):
    """添加仓库对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加仓库")
        self.setMinimumSize(400, 150)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("仓库地址:"), 0, 0)
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://github.com/用户名/仓库名 或 用户名/仓库名")
        form_layout.addWidget(self.url_edit, 0, 1)
        
        layout.addLayout(form_layout)
        
        # 提示信息
        self.hint_label = QLabel("")
        self.hint_label.setStyleSheet("color: gray;")
        layout.addWidget(self.hint_label)
        
        # 按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
    
    def get_repo_full_name(self) -> str:
        """获取仓库全名"""
        url = self.url_edit.text().strip()
        
        # 提取用户名/仓库名
        if 'github.com' in url:
            parts = url.split('github.com/')
            if len(parts) > 1:
                repo_path = parts[1].strip('/')
                return repo_path.split('/')[0] + '/' + repo_path.split('/')[1]
        else:
            # 直接输入 用户名/仓库名
            if '/' in url:
                return url
        
        return ""


# ==================== 导入OPML对话框 ====================
class ImportOPMLDialog(QDialog):
    """导入OPML文件对话框"""
    
    import_finished = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("导入OPML文件")
        self.setMinimumSize(600, 400)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.opml_file = None
        self.import_thread = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 文件选择
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("OPML文件:"))
        
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("请选择OPML文件...")
        self.file_edit.setReadOnly(True)
        file_layout.addWidget(self.file_edit)
        
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        
        layout.addLayout(file_layout)
        
        # 示例文件按钮
        example_layout = QHBoxLayout()
        example_layout.addStretch()
        self.example_btn = QPushButton("创建示例OPML文件")
        self.example_btn.clicked.connect(self.create_example)
        example_layout.addWidget(self.example_btn)
        layout.addLayout(example_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 日志区域
        layout.addWidget(QLabel("导入日志:"))
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_text)
        
        # 预览区域
        self.preview_group = QGroupBox("仓库预览")
        self.preview_group.setVisible(False)
        preview_layout = QVBoxLayout(self.preview_group)
        
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(3)
        self.preview_table.setHorizontalHeaderLabels(["仓库名", "完整名称", "状态"])
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        preview_layout.addWidget(self.preview_table)
        
        layout.addWidget(self.preview_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.import_btn = QPushButton("开始导入")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self.start_import)
        btn_layout.addWidget(self.import_btn)
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_import)
        btn_layout.addWidget(self.stop_btn)
        
        btn_layout.addStretch()
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
    
    def browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择OPML文件", "",
            "OPML文件 (*.opml *.xml);;所有文件 (*.*)"
        )
        
        if file_path:
            self.opml_file = file_path
            self.file_edit.setText(file_path)
            self.import_btn.setEnabled(True)
            self.preview_opml()
    
    def create_example(self):
        """创建示例OPML文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存示例OPML文件", "github_releases.opml",
            "OPML文件 (*.opml);;XML文件 (*.xml)"
        )
        
        if file_path:
            OPMLImporter.create_sample_opml(file_path)
            QMessageBox.information(self, "成功", f"示例文件已创建:\n{file_path}")
    
    def preview_opml(self):
        """预览OPML文件"""
        if not self.opml_file:
            return
        
        try:
            repos = OPMLImporter.parse_opml(self.opml_file)
            
            self.preview_table.setRowCount(len(repos))
            for i, repo in enumerate(repos):
                # 仓库名
                name_item = QTableWidgetItem(repo['name'])
                self.preview_table.setItem(i, 0, name_item)
                
                # 完整名称
                full_name_item = QTableWidgetItem(repo['full_name'])
                self.preview_table.setItem(i, 1, full_name_item)
                
                # 状态（待验证）
                status_item = QTableWidgetItem("待验证")
                status_item.setForeground(QBrush(QColor("orange")))
                self.preview_table.setItem(i, 2, status_item)
            
            self.preview_group.setVisible(True)
            self.log(f"预览: 找到 {len(repos)} 个仓库")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"解析OPML文件失败: {e}")
    
    def start_import(self):
        """开始导入"""
        if not self.opml_file:
            return
        
        # 获取主窗口的github_client和db
        main_window = self.parent()
        if not isinstance(main_window, MainWindow):
            return
        
        # 禁用UI
        self.browse_btn.setEnabled(False)
        self.import_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.log_text.clear()
        
        # 创建并启动导入线程
        self.import_thread = ImportOPMLThread(
            main_window.db.db_path,
            main_window.user_name,
            self.opml_file,
            main_window.config.proxy_host,  # 添加proxy_host
            main_window.config.proxy_port,  # 添加proxy_port
            main_window.config.use_proxy,   # 添加use_proxy
            main_window.github_token        # 添加token
        )
        self.import_thread.progress.connect(self.update_progress)
        self.import_thread.log.connect(self.log)
        self.import_thread.repo_found.connect(self.on_repo_found)
        self.import_thread.finished.connect(self.on_import_finished)
        self.import_thread.error.connect(self.on_import_error)
        self.import_thread.start()
    
    def stop_import(self):
        """停止导入"""
        if self.import_thread and self.import_thread.isRunning():
            self.import_thread.stop()
            self.stop_btn.setEnabled(False)
            self.log("正在停止导入...")
    
    def update_progress(self, current: int, total: int):
        """更新进度"""
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
    
    def on_repo_found(self, repo_info: dict):
        """发现仓库"""
        # 更新预览表格中的状态
        for i in range(self.preview_table.rowCount()):
            if self.preview_table.item(i, 1).text() == repo_info['full_name']:
                status_item = QTableWidgetItem("✓ 已添加")
                status_item.setForeground(QBrush(QColor("green")))
                self.preview_table.setItem(i, 2, status_item)
                break
    
    def on_import_finished(self, success_count: int, fail_count: int):
        """导入完成"""
        self.browse_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if fail_count > 0:
            self.import_btn.setEnabled(True)
        
        QMessageBox.information(
            self, "导入完成",
            f"导入完成!\n成功: {success_count} 个\n失败: {fail_count} 个"
        )
    
        # 发射导入完成信号
        self.import_finished.emit()

    def on_import_error(self, error: str):
        """导入错误"""
        self.browse_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "错误", f"导入失败: {error}")
        self.log(f"错误: {error}")
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # 自动滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)


# ==================== 主窗口 ====================
class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        self.config = AppConfig()
        self.db = None  # 初始化为None
        self.github_client = None
        self.check_thread = None
        self.search_thread = None
        self.import_thread = None
        self.updates = []
        self.settings = QSettings("GitHubMonitor", user_name)
        
        self.load_config()
        self.init_ui()
        self.init_user_data()  # 初始化用户数据
        
        # 启动自动备份
        self.start_auto_backup()
        self.load_settings()

    def init_user_data(self):
        """初始化用户数据"""
        # 如果有旧数据库连接，先关闭
        if self.db:
            self.db.close()
        
        # 重新初始化数据库
        self.db = DatabaseManager(self.user_name)
        
        # 加载GitHub Token
        self.github_token = self.settings.value("github_token", "")
        
        # 重新创建GitHub客户端
        self.github_client = GitHubClient(
            self.config.proxy_host,
            self.config.proxy_port,
            self.config.use_proxy,
            self.github_token
        )
        
        # 清空现有数据
        self.clear_all_data()
        
        # 重新加载数据
        self.load_repos()
        self.load_updates()
        
        # 更新界面显示
        self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} (Build: {ProjectInfo.BUILD_DATE}) - {self.user_name}")
        self.user_label.setText(f"用户: {self.user_name}")
    
        # ========== 新增：更新Token显示 ==========
        self.update_token_display()
    
        self.log(f"欢迎用户: {self.user_name}")

    def clear_all_data(self):
        """清空所有数据"""
        # 清空仓库表格
        self.repo_table.setRowCount(0)
        
        # 清空更新表格
        self.update_table.setRowCount(0)
        
        # 清空日志
        self.log_text.clear()
        
        # 清空搜索框
        self.search_edit.clear()
        
        # 重置状态栏
        self.status_label.setText("就绪")

    def switch_user(self):
        """切换用户"""
        # 停止所有后台线程
        self.stop_all_threads()
        
        # 关闭当前数据库连接
        if self.db:
            self.db.close()
            self.db = None
        
        # 隐藏主窗口
        self.hide()
        
        # 显示登录对话框
        login_dialog = LoginDialog()
        
        # 连接登录成功信号
        def on_login_success(new_user_name):
            # 更新用户名
            self.user_name = new_user_name
            
            # 更新设置对象
            self.settings = QSettings("GitHubMonitor", self.user_name)
            
            # 重新初始化用户数据
            self.init_user_data()
            
            # 重新加载配置
            self.load_config()
            
            # 更新定时器
            self.auto_check_timer.setInterval(self.config.check_interval * 1000)
            
            # 显示主窗口
            self.show()
            
            # 显示成功消息
            self.log(f"已切换到用户: {self.user_name}")
        
        login_dialog.login_success.connect(on_login_success)
        
        # 如果用户取消登录，重新显示主窗口
        if login_dialog.exec() != QDialog.Accepted:
            # 重新连接数据库
            if not self.db:
                self.db = DatabaseManager(self.user_name)
            self.show()
        
        # 显示用户选择对话框
        # self.show_user_selection_dialog()

    
    def stop_all_threads(self):
        """停止所有后台线程（增强版）"""
        threads = []
        
        # 停止检查线程
        if hasattr(self, 'check_thread') and self.check_thread and self.check_thread.isRunning():
            print("正在停止检查线程...")
            self.check_thread.stop()
            threads.append(self.check_thread)
        
        # 停止导入线程
        if hasattr(self, 'import_thread') and self.import_thread and self.import_thread.isRunning():
            print("正在停止导入线程...")
            self.import_thread.stop()
            threads.append(self.import_thread)
        
        # 停止搜索线程
        if hasattr(self, 'search_thread') and self.search_thread and self.search_thread.isRunning():
            print("正在停止搜索线程...")
            # 搜索线程没有stop方法，只能等待
            self.search_thread.quit()
            threads.append(self.search_thread)
        
        # 等待所有线程结束
        for thread in threads:
            if thread.wait(3000):  # 等待最多3秒
                print(f"线程 {thread} 已停止")
            else:
                print(f"线程 {thread} 停止超时")
        
        # 强制垃圾回收
        import gc
        gc.collect()
        
        print("所有线程已停止")
    
    def show_user_selection_dialog(self):
        """显示用户选择对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("选择用户")
        dialog.setMinimumSize(300, 150)
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # 标题
        title_label = QLabel("请选择要切换的用户：")
        title_label.setStyleSheet("font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 用户列表
        user_combo = QComboBox()
        user_combo.setEditable(False)
        
        # 加载用户列表
        users_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")
        users_file = os.path.join(users_dir, "users.json")
        
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', encoding='utf-8') as f:
                    users = json.load(f)
                    for user in users:
                        if user['name'] != self.user_name:  # 排除当前用户
                            user_combo.addItem(user['name'])
            except:
                pass
        
        # 如果没有其他用户，显示提示
        if user_combo.count() == 0:
            no_user_label = QLabel("没有其他用户可选，请先添加用户")
            no_user_label.setStyleSheet("color: orange; margin: 10px;")
            layout.addWidget(no_user_label)
            
            # 添加用户按钮
            add_user_btn = QPushButton("添加用户")
            add_user_btn.clicked.connect(lambda: self.show_user_manager(dialog))
            layout.addWidget(add_user_btn)
        else:
            layout.addWidget(user_combo)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        if user_combo.count() > 0:
            switch_btn = QPushButton("切换")
            switch_btn.clicked.connect(lambda: self.do_switch_user(user_combo.currentText(), dialog))
            btn_layout.addWidget(switch_btn)
        
        manage_btn = QPushButton("用户管理")
        manage_btn.clicked.connect(lambda: self.show_user_manager(dialog))
        btn_layout.addWidget(manage_btn)
        
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def show_user_manager(self, parent_dialog=None):
        """显示用户管理器"""
        # 关闭当前选择对话框
        if parent_dialog:
            parent_dialog.accept()
        
        # 传入当前用户名，以便在删除时检查
        dialog = UserManagerDialog(self, current_user=self.user_name)
        
        # 用户列表变化时刷新
        def on_users_changed():
            # 可以选择重新打开选择对话框
            self.show_user_selection_dialog()
        
        dialog.users_changed.connect(on_users_changed)
        dialog.exec()
    
    def do_switch_user(self, new_user: str, dialog=None):
        """执行用户切换"""
        if dialog:
            dialog.accept()
        
        # 保存当前用户设置
        self.save_settings()
        
        # 更新用户名
        self.user_name = new_user
        
        # 更新设置对象
        self.settings = QSettings("GitHubMonitor", self.user_name)
        
        # 重新初始化用户数据
        self.init_user_data()
        
        # 重新加载配置
        self.load_config()
        
        # 更新定时器
        self.auto_check_timer.setInterval(self.config.check_interval * 1000)
        
        # 显示成功消息
        self.log(f"已切换到用户: {self.user_name}")
        QMessageBox.information(self, "切换成功", f"已成功切换到用户 '{self.user_name}'")
    
    def closeEvent(self, event):
        """关闭事件"""
        self.save_settings()
        
        # 停止所有线程
        self.stop_all_threads()
        
        # 关闭数据库
        if self.db:
            self.db.close()
        
        event.accept()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} (Build: {ProjectInfo.BUILD_DATE}) - {self.user_name}")
        self.setMinimumSize(1000, 600)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(3)
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        toolbar.setSpacing(5)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索仓库 (支持中文、英文、拼音首字母)...")
        self.search_edit.textChanged.connect(self.on_search_text_changed)
        toolbar.addWidget(self.search_edit, 1)
        
        self.search_btn = QPushButton("搜索")
        self.search_btn.clicked.connect(self.on_search)
        toolbar.addWidget(self.search_btn)
        
        self.clear_search_btn = QPushButton("清除")
        self.clear_search_btn.clicked.connect(self.clear_search)
        toolbar.addWidget(self.clear_search_btn)
        
        toolbar.addSpacing(10)
        
        # 操作按钮
        self.add_repo_btn = QPushButton("添加仓库")
        self.add_repo_btn.clicked.connect(self.add_repo)
        toolbar.addWidget(self.add_repo_btn)
        
        self.import_opml_btn = QPushButton("导入OPML")
        self.import_opml_btn.clicked.connect(self.import_opml)
        toolbar.addWidget(self.import_opml_btn)
        
        self.check_btn = QPushButton("检查更新")
        self.check_btn.clicked.connect(self.check_updates)
        toolbar.addWidget(self.check_btn)
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_check)
        self.stop_btn.setEnabled(False)
        toolbar.addWidget(self.stop_btn)
        
        self.backup_btn = QPushButton("手动备份")
        self.backup_btn.clicked.connect(self.manual_backup)
        toolbar.addWidget(self.backup_btn)
        
        self.restore_btn = QPushButton("恢复")
        self.restore_btn.clicked.connect(self.show_restore_dialog)
        toolbar.addWidget(self.restore_btn)
        
        self.settings_btn = QPushButton("设置")
        self.settings_btn.clicked.connect(self.show_settings)
        toolbar.addWidget(self.settings_btn)
        
        toolbar.addStretch()
        
        # ========== 添加 Token 状态显示区域 ==========
        # 创建Token状态容器
        token_container = QWidget()
        token_layout = QHBoxLayout(token_container)
        token_layout.setContentsMargins(5, 2, 5, 2)
        token_layout.setSpacing(5)
        
        # Token状态图标
        self.token_icon = QLabel()
        self.token_icon.setFixedSize(16, 16)
        token_layout.addWidget(self.token_icon)
        
        # Token状态文本
        self.token_status_label = QLabel()
        self.token_status_label.setStyleSheet("font-size: 9pt;")
        token_layout.addWidget(self.token_status_label)
        
        # 快速设置按钮
        self.token_setting_btn = QPushButton("⚙")
        self.token_setting_btn.setToolTip("点击配置GitHub Token")
        self.token_setting_btn.setFixedSize(20, 20)
        self.token_setting_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #3498db;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #2980b9;
            }
        """)
        self.token_setting_btn.clicked.connect(self.show_token_settings)
        token_layout.addWidget(self.token_setting_btn)
        
        toolbar.addWidget(token_container)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedWidth(2)
        toolbar.addWidget(separator)
        
        # 用户信息
        self.user_label = QLabel(f"用户: {self.user_name}")
        toolbar.addWidget(self.user_label)
        
        self.switch_user_btn = QPushButton("切换用户")
        self.switch_user_btn.clicked.connect(self.switch_user)
        toolbar.addWidget(self.switch_user_btn)
        
        main_layout.addLayout(toolbar)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
    
        # Token警告条（仅在未配置Token时显示）
        self.token_warning_bar = QWidget()
        self.token_warning_bar.setFixedHeight(25)
        self.token_warning_bar.setStyleSheet("""
            QWidget {
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                border-radius: 3px;
            }
            QLabel {
                color: #856404;
                font-size: 9pt;
            }
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 2px 8px;
                font-size: 8pt;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        warning_layout = QHBoxLayout(self.token_warning_bar)
        warning_layout.setContentsMargins(10, 2, 10, 2)
        
        warning_icon = QLabel("⚠")
        warning_icon.setStyleSheet("font-size: 12px;")
        warning_layout.addWidget(warning_icon)
        
        warning_text = QLabel("未配置GitHub Token，API速率限制为60次/小时，建议设置Token以提高限制到5000次/小时")
        warning_layout.addWidget(warning_text, 1)
        
        warning_btn = QPushButton("立即设置")
        warning_btn.clicked.connect(self.show_token_settings)
        warning_layout.addWidget(warning_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #856404;
                border: none;
                font-size: 10px;
            }
            QPushButton:hover {
                color: #533f03;
            }
        """)
        close_btn.clicked.connect(self.token_warning_bar.hide)
        warning_layout.addWidget(close_btn)
        
        main_layout.addWidget(self.token_warning_bar)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 仓库列表标签页
        self.repo_tab = QWidget()
        self.init_repo_tab()
        self.tab_widget.addTab(self.repo_tab, "仓库列表")
        
        # 更新记录标签页
        self.update_tab = QWidget()
        self.init_update_tab()
        self.tab_widget.addTab(self.update_tab, "更新记录")
        
        # 日志标签页
        self.log_tab = QWidget()
        self.init_log_tab()
        self.tab_widget.addTab(self.log_tab, "运行日志")
        
        main_layout.addWidget(self.tab_widget, 1)
        
        # 状态栏
        self.status_bar = self.statusBar()
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
    
        # 在状态栏右侧添加永久性的Token状态提示
        self.status_token_label = QLabel()
        self.status_bar.addPermanentWidget(self.status_token_label)
    
        # 定时器
        self.auto_check_timer = QTimer()
        self.auto_check_timer.timeout.connect(self.check_updates)
        self.auto_check_timer.start(self.config.check_interval * 1000)

        # 初始化Token状态显示
        self.update_token_display()

    def show_token_settings(self):
        """显示Token设置对话框"""
        # 直接打开设置对话框并定位到Token设置
        self.show_settings()


    def init_repo_tab(self):
        """初始化仓库列表标签页"""
        layout = QVBoxLayout(self.repo_tab)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 仓库表格
        self.repo_table = QTableWidget()
        self.repo_table.setColumnCount(8)
        self.repo_table.setHorizontalHeaderLabels([
            "名称", "仓库", "当前版本", "上次版本", "最后检查", 
            "监控", "Release", "操作"
        ])
        self.repo_table.horizontalHeader().setStretchLastSection(False)
        self.repo_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.repo_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.repo_table.setAlternatingRowColors(True)
        
        # 设置列宽
        header = self.repo_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.repo_table)
    
    def init_update_tab(self):
        """初始化更新记录标签页"""
        layout = QVBoxLayout(self.update_tab)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 更新表格
        self.update_table = QTableWidget()
        self.update_table.setColumnCount(6)
        self.update_table.setHorizontalHeaderLabels([
            "时间", "仓库", "旧版本", "新版本", "Release说明", "操作"
        ])
        self.update_table.horizontalHeader().setStretchLastSection(False)
        self.update_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.update_table.setAlternatingRowColors(True)
        
        header = self.update_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.update_table)
    
    def init_log_tab(self):
        """初始化日志标签页"""
        layout = QVBoxLayout(self.log_tab)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_text)
        
        # 日志控制
        control_layout = QHBoxLayout()
        
        self.clear_log_btn = QPushButton("清空日志")
        self.clear_log_btn.clicked.connect(self.log_text.clear)
        control_layout.addWidget(self.clear_log_btn)
        
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
    
    def load_repos(self):
        """加载仓库列表"""
        try:
            cursor = self.db.execute(
                "SELECT * FROM repositories ORDER BY name"
            )
            repos = cursor.fetchall()
            
            self.repo_table.setRowCount(len(repos))
            
            for i, repo in enumerate(repos):
                # 名称
                name_item = QTableWidgetItem(repo['name'])
                self.repo_table.setItem(i, 0, name_item)
                
                # 仓库全名
                full_name_item = QTableWidgetItem(repo['full_name'])
                self.repo_table.setItem(i, 1, full_name_item)
                
                # 当前版本
                current_item = QTableWidgetItem(repo['current_version'] or "无")
                self.repo_table.setItem(i, 2, current_item)
                
                # 上次版本
                last_item = QTableWidgetItem(repo['last_version'] or "无")
                self.repo_table.setItem(i, 3, last_item)
                
                # 最后检查
                if repo['last_check']:
                    check_time = datetime.fromisoformat(repo['last_check']).strftime("%Y-%m-%d %H:%M")
                else:
                    check_time = "未检查"
                check_item = QTableWidgetItem(check_time)
                self.repo_table.setItem(i, 4, check_item)
                
                # 监控开关
                watch_widget = QWidget()
                watch_layout = QHBoxLayout(watch_widget)
                watch_layout.setContentsMargins(2, 2, 2, 2)
                
                watch_check = QCheckBox()
                watch_check.setChecked(bool(repo['watch_enabled']))
                watch_check.stateChanged.connect(
                    lambda state, rid=repo['id']: self.toggle_watch(rid, state)
                )
                watch_layout.addWidget(watch_check)
                watch_layout.addStretch()
                
                self.repo_table.setCellWidget(i, 5, watch_widget)
                
                # Release 按钮
                release_btn = QPushButton("查看")
                release_btn.clicked.connect(
                    lambda checked, rid=repo['id'], name=repo['name']: 
                    self.show_releases(rid, name)
                )
                self.repo_table.setCellWidget(i, 6, release_btn)
                
                # 操作按钮
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(2, 2, 2, 2)
                action_layout.setSpacing(2)
                
                delete_btn = QPushButton("删除")
                delete_btn.clicked.connect(
                    lambda checked, rid=repo['id'], name=repo['name']: 
                    self.delete_repo(rid, name)
                )
                action_layout.addWidget(delete_btn)
                
                self.repo_table.setCellWidget(i, 7, action_widget)
            
            # 更新状态栏
            self.status_label.setText(f"共 {len(repos)} 个仓库")
            
        except Exception as e:
            self.log(f"加载仓库列表失败: {e}")
    
    def load_updates(self):
        """加载更新记录"""
        try:
            # 获取最近30天的更新
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            
            cursor = self.db.execute("""
                SELECT r.full_name, rel.* 
                FROM releases rel
                JOIN repositories r ON rel.repo_id = r.id
                WHERE rel.published_at > ?
                ORDER BY rel.published_at DESC
                LIMIT 100
            """, (thirty_days_ago,))
            
            updates = cursor.fetchall()
            
            self.update_table.setRowCount(len(updates))
            
            for i, update in enumerate(updates):
                # 时间
                pub_time = datetime.fromisoformat(update['published_at']).strftime("%Y-%m-%d %H:%M")
                time_item = QTableWidgetItem(pub_time)
                self.update_table.setItem(i, 0, time_item)
                
                # 仓库
                repo_item = QTableWidgetItem(update['full_name'])
                self.update_table.setItem(i, 1, repo_item)
                
                # 版本
                old_version = "未知"  # 这里可以从其他地方获取旧版本
                old_item = QTableWidgetItem(old_version)
                self.update_table.setItem(i, 2, old_item)
                
                new_item = QTableWidgetItem(update['version'])
                self.update_table.setItem(i, 3, new_item)
                
                # Release说明
                body = update['body'] or ""
                if len(body) > 100:
                    body = body[:100] + "..."
                body_item = QTableWidgetItem(body)
                self.update_table.setItem(i, 4, body_item)
                
                # 操作按钮
                btn_widget = QWidget()
                btn_layout = QHBoxLayout(btn_widget)
                btn_layout.setContentsMargins(2, 2, 2, 2)
                
                open_btn = QPushButton("打开")
                open_btn.clicked.connect(
                    lambda checked, url=update['url']: self.open_url(url)
                )
                btn_layout.addWidget(open_btn)
                
                self.update_table.setCellWidget(i, 5, btn_widget)
            
        except Exception as e:
            self.log(f"加载更新记录失败: {e}")
    
    def add_repo(self):
        """添加仓库"""
        dialog = AddRepoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            repo_full_name = dialog.get_repo_full_name()
            
            if not repo_full_name:
                QMessageBox.warning(self, "警告", "请输入有效的仓库地址")
                return
            
            # 显示进度
            self.status_label.setText("正在验证仓库...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            self.add_repo_btn.setEnabled(False)
            
            # 创建并启动验证线程
            self.validate_thread = ValidateRepoThread(self.github_client, repo_full_name)
            self.validate_thread.finished.connect(self.on_repo_validated)
            self.validate_thread.log.connect(self.log)
            self.validate_thread.start()
    
    def import_opml(self):
        """导入OPML文件"""
        dialog = ImportOPMLDialog(self)
    
        # 连接导入完成信号
        dialog.import_finished.connect(self.on_import_completed)
    
        if dialog.exec() == QDialog.Accepted:
            # 重新加载仓库列表
            self.load_repos()
            self.log("OPML导入完成")

    def on_import_completed(self):
        """导入完成后的处理"""
        # 重新加载仓库列表
        self.load_repos()
        self.log("OPML导入完成，仓库列表已刷新")

    def on_repo_validated(self, success: bool, message: str):
        """仓库验证完成"""
        if success:
            repo_full_name = message
            try:
                # 获取仓库信息
                repo_name = repo_full_name.split('/')[1]
                
                # 保存到数据库
                now = datetime.now().isoformat()
                self.db.execute(
                    """
                    INSERT INTO repositories 
                    (name, full_name, url, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (repo_name, repo_full_name, 
                    f"https://github.com/{repo_full_name}", now, now)
                )
                self.db.commit()
                
                self.log(f"添加仓库成功: {repo_full_name}")
                QMessageBox.information(self, "成功", f"仓库添加成功: {repo_full_name}")
                
                # 刷新列表
                self.load_repos()
                self.status_label.setText(f"已添加仓库: {repo_full_name}")
                
                # 立即检查更新
                self.check_updates()
                
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "警告", f"仓库已存在: {repo_full_name}")
            except Exception as e:
                print(f"保存仓库失败: {e}")
                QMessageBox.critical(self, "错误", f"保存仓库失败: {e}")
                self.log(f"保存仓库失败: {e}")
        else:
            # 验证失败
            QMessageBox.warning(self, "警告", message)
        
        # 恢复UI
        self.progress_bar.setVisible(False)
        self.status_label.setText("就绪")
        self.add_repo_btn.setEnabled(True)
    
    def delete_repo(self, repo_id: int, repo_name: str):
        """删除仓库"""
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除仓库 '{repo_name}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.execute("DELETE FROM repositories WHERE id = ?", (repo_id,))
                self.db.commit()
                self.log(f"删除仓库: {repo_name}")
                self.load_repos()  # 确保刷新
                self.status_label.setText(f"已删除仓库: {repo_name}")
            except Exception as e:
                print(f"删除仓库失败: {e}")
                QMessageBox.critical(self, "错误", f"删除失败: {e}")
    
    def toggle_watch(self, repo_id: int, state: int):
        """切换监控状态"""
        enabled = 1 if state == Qt.Checked else 0
        self.db.execute(
            "UPDATE repositories SET watch_enabled = ? WHERE id = ?",
            (enabled, repo_id)
        )
        self.db.commit()
    
    def show_releases(self, repo_id: int, repo_name: str):
        """显示 releases"""
        try:
            releases = self.db.get_repo_releases_info(repo_id)
            
            if not releases:
                QMessageBox.information(self, "提示", f"仓库 '{repo_name}' 暂无 release 信息")
                return
            
            # 创建对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Releases - {repo_name}")
            dialog.setMinimumSize(500, 400)
            
            layout = QVBoxLayout(dialog)
            
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["版本", "发布时间"])
            table.horizontalHeader().setStretchLastSection(True)
            
            table.setRowCount(len(releases))
            for i, release in enumerate(releases):
                version_item = QTableWidgetItem(release['version'])
                table.setItem(i, 0, version_item)
                
                time_item = QTableWidgetItem(release['published_at'])
                table.setItem(i, 1, time_item)
            
            layout.addWidget(table)
            
            btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
            btn_box.accepted.connect(dialog.accept)
            layout.addWidget(btn_box)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取 releases 失败: {e}")
    
    def check_updates(self):
        """检查更新"""
        if self.check_thread and self.check_thread.isRunning():
            return
        
        self.check_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.check_thread = CheckUpdatesThread(self.db, self.config)
        self.check_thread.progress.connect(self.update_progress)
        self.check_thread.log.connect(self.log)
        self.check_thread.finished.connect(self.on_check_finished)
        self.check_thread.error.connect(self.on_check_error)
        self.check_thread.start()
    
    def stop_check(self):
        """停止检查"""
        if self.check_thread and self.check_thread.isRunning():
            self.check_thread.stop()
            self.check_thread.wait()
            self.on_check_finished([])
    
    def update_progress(self, current: int, total: int):
        """更新进度"""
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
        self.status_label.setText(f"正在检查... {current}/{total}")
    
    def on_check_finished(self, updates: list):
        """检查完成"""
        self.check_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("检查完成")
        
        if updates:
            self.updates = updates
            msg = f"发现 {len(updates)} 个仓库有更新"
            self.log(msg)
            QMessageBox.information(self, "更新通知", msg)
            self.load_updates()
        else:
            self.log("没有发现更新")
        
        # 自动备份
        self.create_auto_backup()
        
        # 刷新列表（更新版本信息）
        self.load_repos()  # 确保刷新以显示最新版本
    
        # 切换到更新记录标签页（如果有更新）
        if updates:
            self.tab_widget.setCurrentIndex(1)  # 切换到更新记录标签页

    def on_check_error(self, error: str):
        """检查错误"""
        self.check_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("检查失败")
        
        print(f"检查更新失败: {error}")
        QMessageBox.critical(self, "错误", f"检查更新失败: {error}")
        self.log(f"错误: {error}")
    
    def on_search_text_changed(self, text: str):
        """搜索文本变化"""
        if len(text) >= 2:
            self.on_search()
        elif not text:
            self.clear_search()
    
    def on_search(self):
        """执行搜索"""
        keyword = self.search_edit.text().strip()
        if not keyword:
            self.clear_search()
            return
        
        # 显示进度
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # 启动搜索线程
        self.search_thread = SearchThread(self.db, keyword)
        self.search_thread.result.connect(self.show_search_results)
        self.search_thread.finished.connect(lambda: self.progress_bar.setVisible(False))
        self.search_thread.start()
    
    def show_search_results(self, results: list):
        """显示搜索结果"""
        self.repo_table.setRowCount(len(results))
        
        for i, repo in enumerate(results):
            # 名称
            name_item = QTableWidgetItem(repo['name'])
            self.repo_table.setItem(i, 0, name_item)
            
            # 仓库全名
            full_name_item = QTableWidgetItem(repo['full_name'])
            self.repo_table.setItem(i, 1, full_name_item)
            
            # 当前版本
            current_item = QTableWidgetItem(repo.get('current_version', '无'))
            self.repo_table.setItem(i, 2, current_item)
            
            # 上次版本
            last_item = QTableWidgetItem(repo.get('last_version', '无'))
            self.repo_table.setItem(i, 3, last_item)
            
            # 最后检查
            if repo.get('last_check'):
                check_time = datetime.fromisoformat(repo['last_check']).strftime("%Y-%m-%d %H:%M")
            else:
                check_time = "未检查"
            check_item = QTableWidgetItem(check_time)
            self.repo_table.setItem(i, 4, check_item)
            
            # 监控开关
            watch_widget = QWidget()
            watch_layout = QHBoxLayout(watch_widget)
            watch_layout.setContentsMargins(2, 2, 2, 2)
            
            watch_check = QCheckBox()
            watch_check.setChecked(bool(repo.get('watch_enabled', True)))
            watch_check.stateChanged.connect(
                lambda state, rid=repo['id']: self.toggle_watch(rid, state)
            )
            watch_layout.addWidget(watch_check)
            watch_layout.addStretch()
            
            self.repo_table.setCellWidget(i, 5, watch_widget)
            
            # Release 按钮
            release_btn = QPushButton("查看")
            release_btn.clicked.connect(
                lambda checked, rid=repo['id'], name=repo['name']: 
                self.show_releases(rid, name)
            )
            self.repo_table.setCellWidget(i, 6, release_btn)
            
            # 操作按钮
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(2)
            
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(
                lambda checked, rid=repo['id'], name=repo['name']: 
                self.delete_repo(rid, name)
            )
            action_layout.addWidget(delete_btn)
            
            self.repo_table.setCellWidget(i, 7, action_widget)
        
        self.status_label.setText(f"找到 {len(results)} 个匹配的仓库")
    
    def clear_search(self):
        """清除搜索"""
        self.search_edit.clear()
        self.load_repos()
    
    def manual_backup(self):
        """手动备份"""
        try:
            self.status_label.setText("正在创建手动备份...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            # 创建备份
            backup_file = self.db.create_backup(BackupType.MANUAL)
            
            # 清理旧备份
            self.db.cleanup_old_backups(self.config.backup_count)
            
            self.status_label.setText(f"备份成功: {os.path.basename(backup_file)}")
            self.log(f"手动备份创建成功: {backup_file}")
            
            QMessageBox.information(self, "备份成功", f"备份已保存到:\n{backup_file}")
            
        except Exception as e:
            QMessageBox.critical(self, "备份失败", f"创建备份失败: {e}")
            self.log(f"备份失败: {e}")
        
        finally:
            self.progress_bar.setVisible(False)
    
    def create_auto_backup(self):
        """创建自动备份"""
        try:
            # 创建备份
            backup_file = self.db.create_backup(BackupType.AUTO)
            
            # 清理旧备份
            self.db.cleanup_old_backups(self.config.backup_count)
            
            self.log(f"自动备份创建成功")
            
        except Exception as e:
            self.log(f"自动备份失败: {e}")
    
    def show_restore_dialog(self):
        """显示恢复对话框"""
        dialog = BackupRestoreDialog(self.db, self)
        if dialog.exec() == QDialog.Accepted:
            # 重新加载数据
            self.load_repos()
            self.load_updates()
            self.log("数据库恢复完成")
    
    def show_settings(self):
        """显示设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setMinimumSize(450, 400)
        
        layout = QVBoxLayout(dialog)
        
        # GitHub Token设置
        token_group = QGroupBox("GitHub API设置")
        token_layout = QVBoxLayout()
        
        token_layout.addWidget(QLabel(
            "GitHub Token (提高API限制到5000次/小时):\n"
            "在 https://github.com/settings/tokens 创建"
        ))
        
        self.token_edit = QLineEdit()
        self.token_edit.setEchoMode(QLineEdit.Password)
        self.token_edit.setPlaceholderText("输入GitHub Personal Access Token")
        
        # 从配置加载已有的token
        saved_token = self.settings.value("github_token", "")
        if saved_token:
            self.token_edit.setText(saved_token)
        
        token_layout.addWidget(self.token_edit)
        
        # 显示当前token状态
        self.token_status = QLabel()
        self.update_token_status()
        token_layout.addWidget(self.token_status)
    
        # 添加Token测试按钮
        test_token_btn = QPushButton("测试Token有效性")
        test_token_btn.clicked.connect(self.test_github_token)
        token_layout.addWidget(test_token_btn)
    
        token_group.setLayout(token_layout)
        layout.addWidget(token_group)
        
        # 代理设置
        proxy_group = QGroupBox("代理设置")
        proxy_layout = QGridLayout()
        
        self.use_proxy_check = QCheckBox("启用代理")
        self.use_proxy_check.setChecked(self.config.use_proxy)
        proxy_layout.addWidget(self.use_proxy_check, 0, 0, 1, 2)
        
        proxy_layout.addWidget(QLabel("主机:"), 1, 0)
        self.proxy_host_edit = QLineEdit(self.config.proxy_host)
        proxy_layout.addWidget(self.proxy_host_edit, 1, 1)
        
        proxy_layout.addWidget(QLabel("端口:"), 2, 0)
        self.proxy_port_edit = QSpinBox()
        self.proxy_port_edit.setRange(1, 65535)
        self.proxy_port_edit.setValue(self.config.proxy_port)
        proxy_layout.addWidget(self.proxy_port_edit, 2, 1)
        
        # 测试代理按钮
        self.test_proxy_btn = QPushButton("测试代理连接")
        self.test_proxy_btn.clicked.connect(self.test_proxy_connection)
        proxy_layout.addWidget(self.test_proxy_btn, 3, 0, 1, 2)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        # 检查设置
        check_group = QGroupBox("检查设置")
        check_layout = QGridLayout()
        
        check_layout.addWidget(QLabel("检查间隔(秒):"), 0, 0)
        self.interval_edit = QSpinBox()
        self.interval_edit.setRange(60, 86400)
        self.interval_edit.setValue(self.config.check_interval)
        self.interval_edit.setSingleStep(60)
        check_layout.addWidget(self.interval_edit, 0, 1)
        
        check_group.setLayout(check_layout)
        layout.addWidget(check_group)
        
        # 备份设置
        backup_group = QGroupBox("备份设置")
        backup_layout = QGridLayout()
        
        backup_layout.addWidget(QLabel("保留备份数量:"), 0, 0)
        self.backup_count_edit = QSpinBox()
        self.backup_count_edit.setRange(1, 100)
        self.backup_count_edit.setValue(self.config.backup_count)
        backup_layout.addWidget(self.backup_count_edit, 0, 1)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        # 调试模式
        self.debug_check = QCheckBox("调试模式")
        self.debug_check.setChecked(self.config.debug_mode)
        layout.addWidget(self.debug_check)
        
        layout.addStretch()
        
        # 按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        layout.addWidget(btn_box)
        
        if dialog.exec() == QDialog.Accepted:
            # 保存设置
            self.config.use_proxy = self.use_proxy_check.isChecked()
            self.config.proxy_host = self.proxy_host_edit.text()
            self.config.proxy_port = self.proxy_port_edit.value()
            self.config.check_interval = self.interval_edit.value()
            self.config.backup_count = self.backup_count_edit.value()
            self.config.debug_mode = self.debug_check.isChecked()
            
            # 获取新token
            new_token = self.token_edit.text().strip()
            old_token = self.settings.value("github_token", "")
            
            # 保存token到设置
            self.settings.setValue("github_token", new_token)
            self.github_token = new_token  # 更新内存中的token
            
            # 关键修复：无论token是否变化，都重新创建GitHubClient实例
            # 这样可以确保代理设置和token都立即生效
            self.github_client = GitHubClient(
                self.config.proxy_host,
                self.config.proxy_port,
                self.config.use_proxy,
                new_token if new_token else None
            )
            
            # 更新token状态显示
            self.update_token_status()
        
            # ========== 新增：更新界面Token显示 ==========
            self.update_token_display()
        
            # 如果token发生变化，显示提示
            if new_token != old_token:
                self.log(f"GitHub Token已更新，新的Token: {'已配置' if new_token else '已清除'}")
                
                # 可选：立即测试新token是否有效
                if new_token:
                    self.test_github_token()
            
            # 更新定时器
            self.auto_check_timer.setInterval(self.config.check_interval * 1000)
            
            # 保存配置
            self.save_config()
            
            # 刷新界面显示
            self.load_repos()  # 刷新仓库列表
            self.log("设置已更新，配置立即生效")
            
            # 显示成功消息
            QMessageBox.information(self, "设置已保存", "配置已更新并立即生效")

    def test_github_token(self):
        """测试GitHub Token是否有效"""
        try:
            # 使用新的client测试API
            response = self.github_client.session.get(
                "https://api.github.com/rate_limit",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                remaining = data.get('rate', {}).get('remaining', 0)
                limit = data.get('rate', {}).get('limit', 0)
                self.log(f"Token验证成功: API限制 {limit}次/小时，剩余 {remaining}次")
                
                # 更新状态显示
                masked_token = self.github_token[:4] + "*" * (len(self.github_token) - 8) + self.github_token[-4:] if len(self.github_token) > 8 else "***"
                self.token_status.setText(f"✓ Token有效: {masked_token} (剩余 {remaining}次)")
                self.token_status.setStyleSheet("color: green")
            else:
                self.log(f"Token验证失败: HTTP {response.status_code}")
                self.token_status.setText("⚠ Token无效或已过期")
                self.token_status.setStyleSheet("color: red")
                
        except Exception as e:
            self.log(f"Token测试失败: {e}")
            self.token_status.setText(f"⚠ Token测试失败: {str(e)[:30]}...")
            self.token_status.setStyleSheet("color: orange")

    def update_token_status(self):
        """更新Token状态"""
        token = self.settings.value("github_token", "")
        if token:
            masked = token[:4] + "*" * (len(token) - 8) + token[-4:] if len(token) > 8 else "***"
            self.token_status.setText(f"✓ 已配置Token: {masked}")
            self.token_status.setStyleSheet("color: green")
        else:
            self.token_status.setText("⚠ 未配置Token，API限制60次/小时")
            self.token_status.setStyleSheet("color: orange")

    def test_proxy_connection(self):
        """测试代理连接"""
        host = self.proxy_host_edit.text()
        port = self.proxy_port_edit.value()
        use_proxy = self.use_proxy_check.isChecked()
        
        self.status_label.setText("测试代理连接...")
        
        try:
            test_client = GitHubClient(host, port, use_proxy)
            # 测试连接GitHub
            response = test_client.session.get(
                "https://api.github.com/zen", 
                timeout=5
            )
            
            if response.status_code == 200:
                QMessageBox.information(self, "成功", "代理连接正常！")
                self.log("代理测试成功")
            else:
                QMessageBox.warning(self, "警告", f"代理返回状态码: {response.status_code}")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"代理连接失败: {e}")
            self.log(f"代理测试失败: {e}")
        
        finally:
            self.status_label.setText("就绪")


            
    def _show_login_dialog(self):
        """显示登录对话框"""
        # 创建新的登录对话框，父级设为None
        login_dialog = LoginDialog()
        
        # 连接登录成功信号
        def on_login_success(user_name):
            # 创建新的主窗口
            new_main_window = MainWindow(user_name)
            new_main_window.show()
        
        login_dialog.login_success.connect(on_login_success)
    
        # 显示对话框
        result = login_dialog.exec()
    
        # 如果用户取消登录，则退出程序
        if result != QDialog.Accepted:
            QApplication.quit()

    def show_login(self):
        """显示登录窗口"""
        login_dialog = LoginDialog()
        
        def on_login_success(user_name):
            # 重新初始化当前窗口
            self.user_name = user_name
            self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} (Build: {ProjectInfo.BUILD_DATE}) - {self.user_name}")
            self.user_label.setText(f"用户: {self.user_name}")
            
            # 重新初始化数据库
            self.db = DatabaseManager(user_name)
            
            # 重新加载设置
            self.settings = QSettings("GitHubMonitor", user_name)
            self.load_settings()
            self.github_token = self.settings.value("github_token", "")
            
            # 重新创建GitHub客户端
            self.github_client = GitHubClient(
                self.config.proxy_host,
                self.config.proxy_port,
                self.config.use_proxy,
                self.github_token
            )
            
            # 重新加载所有数据
            self.load_repos()
            self.load_updates()
            self.log_text.clear()
            self.log(f"欢迎用户: {user_name}")
        
        login_dialog.login_success.connect(on_login_success)
        login_dialog.exec()
    
    def on_login_success(self, user_name: str):
        """登录成功"""
        self.user_name = user_name
        self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} (Build: {ProjectInfo.BUILD_DATE}) - {self.user_name}")
        self.user_label.setText(f"用户: {self.user_name}")
        
        # 重新初始化数据库
        self.db = DatabaseManager(user_name)
        
        # 重新加载所有数据
        self.load_repos()
        self.load_updates()
        self.log_text.clear()  # 清空日志
        self.log(f"欢迎用户: {user_name}")
        
        # 加载设置
        self.settings = QSettings("GitHubMonitor", user_name)
        self.load_settings()
    
    def start_auto_backup(self):
        """启动自动备份"""
        # 每天凌晨3点备份
        now = datetime.now()
        target = datetime(now.year, now.month, now.day, 3, 0, 0)
        if now > target:
            target += timedelta(days=1)
        
        seconds = (target - now).seconds
        QTimer.singleShot(seconds * 1000, self.create_auto_backup)
        
        # 每24小时执行一次
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.create_auto_backup)
        self.backup_timer.start(24 * 3600 * 1000)
    
    def open_url(self, url: str):
        """打开URL"""
        import webbrowser
        webbrowser.open(url)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # 自动滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    
    def load_config(self):
        """加载配置"""
        # 从 QSettings 加载配置
        self.config.proxy_host = self.settings.value("proxy_host", "127.0.0.1")
        self.config.proxy_port = int(self.settings.value("proxy_port", 20808))
        self.config.use_proxy = self.settings.value("use_proxy", "true") == "true"
        self.config.check_interval = int(self.settings.value("check_interval", 3600))
        self.config.backup_count = int(self.settings.value("backup_count", 30))
        self.config.debug_mode = self.settings.value("debug_mode", "false") == "true"
    
    def save_config(self):
        """保存配置"""
        self.settings.setValue("proxy_host", self.config.proxy_host)
        self.settings.setValue("proxy_port", self.config.proxy_port)
        self.settings.setValue("use_proxy", "true" if self.config.use_proxy else "false")
        self.settings.setValue("check_interval", self.config.check_interval)
        self.settings.setValue("backup_count", self.config.backup_count)
        self.settings.setValue("debug_mode", "true" if self.config.debug_mode else "false")
    
    def load_settings(self):
        """加载窗口设置"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
    
    def save_settings(self):
        """保存窗口设置"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    


    def _show_login_from_app(self):
        """从应用程序级别显示登录窗口"""
        # 创建新的登录对话框
        login_dialog = LoginDialog()
        
        # 连接登录成功信号
        def on_login_success(user_name):
            # 创建新的主窗口
            new_main_window = MainWindow(user_name)
            new_main_window.show()
        
        login_dialog.login_success.connect(on_login_success)
        
        # 显示对话框
        result = login_dialog.exec()
        
        # 如果用户取消登录，则退出程序
        if result != QDialog.Accepted:
            QApplication.quit()
            
    def update_token_display(self):
        """更新Token显示状态"""
        token = self.settings.value("github_token", "")
        
        # 更新图标
        if token:
            # 有Token，显示绿色勾
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#28a745"))  # 绿色
            painter.drawEllipse(2, 2, 12, 12)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Webdings", 8))
            painter.drawText(5, 12, "a")  # 对勾符号
            painter.end()
            self.token_icon.setPixmap(pixmap)
            
            # 显示Token信息
            masked_token = token[:4] + "*" * (len(token) - 8) + token[-4:] if len(token) > 8 else "***"
            self.token_status_label.setText(f"Token: {masked_token}")
            self.token_status_label.setStyleSheet("color: #28a745;")
            
            # 隐藏警告条
            self.token_warning_bar.hide()
            
            # 更新状态栏
            self.status_token_label.setText("✓ Token已配置 | 5000次/小时")
            self.status_token_label.setStyleSheet("color: #28a745;")
        else:
            # 无Token，显示红色感叹号
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#dc3545"))  # 红色
            painter.drawEllipse(2, 2, 12, 12)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Webdings", 8))
            painter.drawText(5, 12, "i")  # 感叹号
            painter.end()
            self.token_icon.setPixmap(pixmap)
            
            # 显示提示信息
            self.token_status_label.setText("未配置Token")
            self.token_status_label.setStyleSheet("color: #dc3545;")
            
            # 显示警告条
            self.token_warning_bar.show()
            
            # 更新状态栏
            self.status_token_label.setText("⚠ 未配置Token | 60次/小时")
            self.status_token_label.setStyleSheet("color: #dc3545;")

# ==================== 应用程序类 ====================
class Application(QApplication):
    """应用程序类"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("GitHub Releases Monitor")
        self.setOrganizationName("GitHubMonitor")
        
        # 设置样式
        self.setStyle(QStyleFactory.create("Fusion"))
        
        # 设置字体
        font = QFont("Microsoft YaHei", 9)
        self.setFont(font)
    
    def run(self):
        """运行应用"""
        # 显示登录窗口
        login_dialog = LoginDialog()
        
        # 连接登录成功信号
        def on_login_success(user_name):
            self.main_window = MainWindow(user_name)
            self.main_window.show()
        
        login_dialog.login_success.connect(on_login_success)
        
        # 显示登录窗口
        if login_dialog.exec() == QDialog.Accepted:
            return self.exec()
        else:
            return 0


# ==================== 程序入口 ====================
def main():
    """主函数"""
    # 创建应用
    app = Application(sys.argv)
    
    # 运行应用
    sys.exit(app.run())


if __name__ == "__main__":
    main()