# 软件截图

<img width="1199" height="639" alt="image" src="https://github.com/user-attachments/assets/367943cf-19ca-4997-a763-b59ab816da7d" />

<img width="1199" height="639" alt="image" src="https://github.com/user-attachments/assets/6fc22da0-1576-4eeb-b9d1-ffdc87bf7aac" />

<img width="1296" height="639" alt="image" src="https://github.com/user-attachments/assets/61c6b1da-bcbe-4ead-8cc6-91d300d2a06b" />

<img width="1296" height="639" alt="image" src="https://github.com/user-attachments/assets/6c8d0e75-fb93-4d8d-a80f-00a05fcae21e" />

<img width="1296" height="639" alt="image" src="https://github.com/user-attachments/assets/83c4b7ea-e94e-42c9-9842-10e5bc979d56" />

<img width="1296" height="639" alt="image" src="https://github.com/user-attachments/assets/3b1e2a19-7802-4319-a19b-1c599a7f6ca9" />

<img width="1296" height="639" alt="image" src="https://github.com/user-attachments/assets/a8fffcd7-41a4-4a7b-bd09-a34e16c2877a" />

<img width="1447" height="639" alt="image" src="https://github.com/user-attachments/assets/b0f0af7c-ac95-4e67-8376-66c61db49f03" />

----
# GitHub Releases 监控程序 完全使用指南

## 📚 文档信息

| 项目 | 内容 |
|------|------|
| **软件名称** | GitHub Releases 监控程序 |
| **版本** | 1.1.15 |
| **发布日期** | 2026-03-10 |
| **作者** | 杜玛 |
| **版权** | © 永久 杜玛 保留所有权利 |
| **许可证** | GNU Affero General Public License v3.0 |
| **项目主页** | https://github.com/duma520 |
| **项目地址** | https://github.com/duma520/GitHub_Release_Monitor |

---

## 📑 目录

1. [版本更新历史](#版本更新历史)
2. [软件简介（三分钟快速了解）](#软件简介三分钟快速了解)
3. [零基础入门指南](#零基础入门指南)
4. [基础应用教程](#基础应用教程)
5. [高级应用指南](#高级应用指南)
6. [专业开发人员手册](#专业开发人员手册)
7. [常见问题解答（FAQ）](#常见问题解答faq)
8. [故障排除指南](#故障排除指南)
9. [最佳实践建议](#最佳实践建议)
10. [附录](#附录)

---

## 🚀 版本更新历史

### 版本 1.1.15 (2026-03-10)
- **新功能**：添加了直观的Token状态显示图标和警告条
- **改进**：优化了用户切换时的数据库连接处理
- **修复**：修复了修改用户名时的文件占用问题
- **优化**：提升了搜索功能的响应速度

### 版本 1.1.14 (2026-02-15)
- **新功能**：支持OPML文件批量导入
- **改进**：增强了代理连接的稳定性
- **修复**：修复了备份恢复时的数据一致性

### 版本 1.1.13 (2026-01-20)
- **新功能**：多用户管理系统
- **改进**：优化了拼音搜索功能
- **修复**：修复了API速率限制处理

### 版本 1.1.12 (2025-12-25)
- **新功能**：自动备份和恢复功能
- **改进**：改进了更新通知界面
- **修复**：修复了Windows系统兼容性问题

---

## 📖 软件简介（三分钟快速了解）

### 这是什么软件？

**GitHub Releases 监控程序** 就像是一个"仓库管家"，帮你自动关注和检查你在GitHub上感兴趣的软件仓库是否有新版本发布。

### 举个生活中的例子 🌰

想象一下：
- 你订阅了10本杂志（GitHub仓库）
- 每本杂志不定期出版新刊（新版本发布）
- 你不可能每天去报刊亭查看每本杂志是否出了新刊（手动检查太麻烦）
- 这个软件就是帮你"订阅"这些杂志，每当有新刊出版，它就会第一时间通知你

### 为什么需要这个软件？

| 场景 | 手动检查 | 使用本软件 |
|------|----------|------------|
| 关注10个仓库 | 每天访问10个页面 | 一键自动检查 |
| 发现新版本 | 靠运气或频繁刷新 | 立即通知 |
| 记录版本历史 | 手动记录或遗忘 | 自动保存 |
| 多人使用 | 无法区分 | 多用户支持 |

### 核心功能一览

✅ **自动监控** - 定期检查仓库更新  
✅ **多用户支持** - 家庭成员/团队成员各自独立  
✅ **智能搜索** - 支持中文、英文、拼音搜索  
✅ **批量导入** - 通过OPML文件一键导入  
✅ **数据备份** - 自动备份，防止数据丢失  
✅ **代理支持** - 解决网络访问问题  
✅ **更新通知** - 新版本即时提醒  

---

## 🎯 零基础入门指南

### 第一章：准备工作

#### 1.1 什么是GitHub？

**简单来说**：GitHub是一个存放代码的"网盘"，全球开发者都在这里分享和协作开发软件。

**你需要知道的几个术语**：
- **仓库(Repository)**：就像是一个软件的"文件夹"
- **Release/版本发布**：开发者正式发布的软件版本
- **Token**：相当于你的"通行证"，让软件能代表你访问GitHub

#### 1.2 我需要准备什么？

**硬件要求**：
- 任何能运行Windows的电脑（内存512MB以上，硬盘100MB以上）

**软件要求**：
- Windows 7/8/10/11 或 macOS 或 Linux
- Python 3.8或更高版本（如已安装请确认版本）

#### 1.3 获取GitHub Token（重要！）

> **为什么要获取Token？**
> - 没有Token：每小时只能查询60次
> - 有Token：每小时可查询5000次

**图文步骤**：

1. **登录GitHub**
   - 打开 https://github.com
   - 登录你的账号（没有账号就免费注册一个）

2. **进入Token设置页面**
   - 点击右上角你的头像
   - 选择 Settings（设置）
   - 在左侧菜单最底部，点击 Developer settings
   - 点击 Personal access tokens → Tokens (classic)

3. **生成新Token**
   - 点击 "Generate new token (classic)"
   - 在 Note 中输入一个名称，比如 "GitHub Monitor"
   - **重要：不要勾选任何权限选项**（public repos only）
   - 滑到页面底部，点击 "Generate token"

4. **保存Token**
   - **复制并保存好显示的token！**（关掉页面后就看不到了）
   - 格式类似：`ghp_xxxxxxxxxxxxxxxxxxxx`

### 第二章：安装软件

#### 2.1 方法一：直接下载可执行文件（推荐新手）

1. 访问项目主页：https://github.com/duma520/GitHub_Release_Monitor
2. 点击右侧的 Releases
3. 下载最新版本的 `.exe` 文件（Windows用户）
4. 双击运行即可

#### 2.2 方法二：从源代码运行（进阶用户）

**步骤1：安装Python**
- 访问 https://python.org
- 下载Python 3.8或更高版本
- 安装时**记得勾选** "Add Python to PATH"

**步骤2：下载源代码**
```
# 方法A：直接下载ZIP
访问项目主页 → Code → Download ZIP → 解压

# 方法B：使用Git（如果有安装）
git clone https://github.com/duma520/GitHub_Release_Monitor.git
```

**步骤3：安装依赖**
```
# 打开命令行（CMD或终端）
cd 你解压的文件夹路径
pip install -r requirements.txt
```

**步骤4：运行软件**
```
python GitHub_Release_Monitor.py
```

### 第三章：第一次启动

#### 3.1 首次运行界面

当你第一次运行软件，会看到**用户登录**窗口：

```
╔════════════════════════════╗
║   GitHub Releases 监控系统  ║
╠════════════════════════════╣
║ 选择用户: [下拉框]           ║
║                            ║
║ [登录] [用户管理] [退出]     ║
╚════════════════════════════╝
```

**情况1：你是第一次使用**
- 点击"用户管理" → "添加用户" → 输入你的名字（如"张三"）
- 返回登录界面，选择刚创建的用户，点击"登录"

**情况2：已有用户**
- 直接选择你的用户名，点击"登录"

#### 3.2 主界面介绍

登录后，你会看到主窗口，分为几个区域：

```
┌─────────────────────────────────────┐
│ [搜索框] [按钮区] [用户:张三]        │
├─────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐            │
│ │仓库 │ │更新 │ │日志 │             │
│ │列表 │ │记录 │ │    │             │
│ └─────┘ └─────┘ └─────┘            │
├─────────────────────────────────────┤
│ 状态栏：就绪                        │
└─────────────────────────────────────┘
```

**功能区说明**：
- **顶部工具栏**：搜索、添加仓库、检查更新等主要操作
- **标签页**：切换不同视图（仓库列表/更新记录/运行日志）
- **状态栏**：显示当前状态和信息

---

## 🏗️ 基础应用教程

### 第四章：添加你的第一个仓库

#### 4.1 手动添加单个仓库

**步骤演示**：添加"curl"工具仓库

1. **找到仓库地址**
   - 打开浏览器，访问 https://github.com/curl/curl
   - 复制地址栏的URL

2. **添加仓库**
   - 在主界面点击"添加仓库"按钮
   - 在弹出的窗口中粘贴地址：`https://github.com/curl/curl`
   - 点击"确定"

3. **验证添加**
   - 软件会自动验证仓库是否存在
   - 验证通过后，仓库会出现在列表中
   - 状态栏显示"已添加仓库: curl/curl"

#### 4.2 批量导入（OPML方式）

**什么是OPML文件？**
OPML是一种用于交换订阅列表的文件格式，常用于RSS阅读器。

**场景**：你已经在使用其他RSS阅读器订阅了GitHub Releases

**操作步骤**：

1. **导出OPML文件**
   - 在你的RSS阅读器中找到"导出订阅"功能
   - 保存为 `.opml` 或 `.xml` 文件

2. **导入到本软件**
   - 点击"导入OPML"按钮
   - 选择你的OPML文件
   - 软件会自动识别GitHub相关的订阅
   - 点击"开始导入"

3. **预览和确认**
   - 导入前可以预览找到的仓库
   - 每个仓库会验证是否存在
   - 导入完成后会显示成功/失败数量

### 第五章：使用仓库列表

#### 5.1 理解仓库表格

仓库列表的每一列代表什么？

| 列名 | 含义 | 举例 |
|------|------|------|
| 名称 | 仓库的简短名称 | curl |
| 仓库 | 完整的仓库标识 | curl/curl |
| 当前版本 | 最新的版本号 | 7.88.1 |
| 上次版本 | 之前的版本号 | 7.87.0 |
| 最后检查 | 最近检查时间 | 2026-03-10 14:30 |
| 监控 | 是否自动检查 | [√] 勾选 |
| Release | 查看历史版本 | [查看]按钮 |
| 操作 | 删除等操作 | [删除]按钮 |

#### 5.2 管理监控状态

**开启/关闭监控**：
- 勾选"监控"列中的复选框，表示监控该仓库
- 取消勾选，表示暂停监控

**什么时候需要关闭监控？**
- 仓库已不再维护
- 暂时不想收到该仓库的更新通知
- 该仓库发布太频繁（如每天发布）

#### 5.3 查看版本历史

点击某个仓库的"查看"按钮，可以看到该仓库所有的历史版本：

```
┌─ Releases - curl ───────────────┐
│ 版本        发布时间            │
│ 7.88.1    2026-03-01 10:00:00  │
│ 7.88.0    2026-02-15 09:30:00  │
│ 7.87.0    2026-02-01 14:20:00  │
│ 7.86.0    2026-01-15 11:10:00  │
└─────────────────────────────────┘
```

### 第六章：搜索功能详解

#### 6.1 搜索方式

本软件支持**三种搜索方式**：

1. **直接搜索** - 输入仓库名称的一部分
2. **中文搜索** - 可以直接搜索中文名
3. **拼音搜索** - 支持拼音首字母

#### 6.2 搜索示例

**场景1**：你想找"curl"相关的仓库
- 在搜索框输入：`curl`
- 结果：显示所有名称含"curl"的仓库

**场景2**：你只记得仓库中文名
- 假设仓库名叫"文件传输工具"
- 输入：`文件` 或 `传输`
- 结果：会匹配到包含这些词的仓库

**场景3**：你只记得拼音首字母
- 输入：`wjcs`（文件传输的拼音首字母）
- 结果：也能找到对应的仓库

#### 6.3 搜索技巧

| 你想找... | 可以输入 | 说明 |
|-----------|----------|------|
| Node.js相关 | `node` | 直接匹配 |
| 中文名"微信" | `微信` 或 `wx` | 中文或拼音 |
| 多个关键词 | `curl http` | 会分别匹配 |
| 精确匹配 | 用引号（暂不支持） | - |

### 第七章：检查更新

#### 7.1 手动检查

**操作**：
1. 点击主界面的"检查更新"按钮
2. 软件开始逐个检查所有开启监控的仓库
3. 进度条显示检查进度
4. 日志区域显示检查过程

**检查过程示例**：
```
[14:30:15] 开始检查更新...
[14:30:16] 检查: curl/curl
[14:30:18]   已是最新: curl 7.88.1
[14:30:19] 检查: nodejs/node
[14:30:22] ✓ 发现更新: node v18.14.0 -> v18.15.0
[14:30:25] 检查完成，发现1个更新
```

#### 7.2 自动检查

软件会按照设定的时间间隔自动检查：

- **默认设置**：每小时检查一次
- **如何修改**：在"设置"中调整"检查间隔"

#### 7.3 发现更新后

当发现新版本时：
1. 软件会弹出通知窗口
2. 自动切换到"更新记录"标签页
3. 新版本信息会保存在数据库中

---

## 🚀 高级应用指南

### 第八章：多用户管理

#### 8.1 为什么需要多用户？

**使用场景**：
- 家庭成员共用一台电脑，各自关注不同项目
- 团队成员需要独立的数据记录
- 个人区分工作和兴趣项目

#### 8.2 创建新用户

1. 点击"切换用户"按钮
2. 在弹出的登录窗口点击"用户管理"
3. 点击"添加用户"
4. 输入用户名（如"work"或"personal"）
5. 新用户出现在列表中

#### 8.3 切换用户

1. 点击"切换用户"按钮
2. 选择要切换到的用户
3. 点击"登录"
4. 软件会自动加载该用户的数据

#### 8.4 修改用户名

1. 进入用户管理
2. 选中要修改的用户
3. 点击"修改用户名"
4. 输入新名称
5. 软件会自动重命名相关的数据文件

**注意事项**：
- 不能修改当前登录的用户名
- 修改后原用户数据会迁移到新名称

#### 8.5 删除用户

1. 进入用户管理
2. 选中要删除的用户
3. 点击"删除用户"
4. 确认删除
5. 该用户的所有数据（数据库、备份）都会被删除

**⚠️ 警告**：删除操作不可恢复！

### 第九章：代理设置

#### 9.1 什么时候需要代理？

**适用场景**：
- 所在网络访问GitHub不稳定
- 企业内网需要代理才能访问外网
- 希望提高访问速度

#### 9.2 配置代理

1. 点击"设置"按钮
2. 在"代理设置"区域：
   - 勾选"启用代理"
   - 输入代理服务器地址（如：127.0.0.1）
   - 输入代理端口（如：20808）

3. 点击"测试代理连接"
   - 如果成功：显示"代理连接正常！"
   - 如果失败：检查地址和端口是否正确

#### 9.3 代理示例

**常见代理配置**：

| 代理软件 | 默认地址 | 默认端口 |
|----------|----------|----------|
| Clash | 127.0.0.1 | 7890 |
| V2Ray | 127.0.0.1 | 10808 |
| Shadowsocks | 127.0.0.1 | 1080 |
| 公司代理 | 根据管理员提供 | 根据管理员提供 |

### 第十章：数据备份与恢复

#### 10.1 备份类型

本软件支持四种备份类型：

| 类型 | 触发方式 | 用途 |
|------|----------|------|
| **自动备份** | 每天凌晨3点自动创建 | 日常数据保护 |
| **手动备份** | 用户点击"手动备份" | 重要操作前备份 |
| **检查后备份** | 每次检查更新后 | 保存检查状态 |
| **恢复前备份** | 恢复操作前自动创建 | 防止恢复失败 |

#### 10.2 手动备份

**操作步骤**：
1. 点击工具栏的"手动备份"按钮
2. 软件开始创建备份
3. 完成后显示备份文件路径
4. 可以在备份目录查看

**备份文件命名规则**：
- 自动备份：`自动_20260310_030001.db`
- 手动备份：`手动_20260310_143022.db`

#### 10.3 查看和管理备份

1. 点击"恢复"按钮
2. 打开备份恢复对话框
3. 可以看到所有备份列表：
   - 备份时间
   - 备份类型
   - 文件大小
   - 预览按钮

#### 10.4 预览备份内容

点击某个备份的"预览"按钮，可以看到：
```
【备份文件信息】
文件名: 手动_20260310_143022.db
创建时间: 2026-03-10 14:30:22
文件大小: 1.2 MB
备份类型: 手动

【数据统计】
仓库数量: 25
Release数量: 346

【Release时间范围】
最早: 2025-01-01 10:00:00
最新: 2026-03-10 11:20:00
```

#### 10.5 恢复备份

**操作流程**：
1. 在备份列表中选择要恢复的备份
2. 点击"恢复选中备份"
3. 确认恢复（系统会自动创建恢复前备份）
4. 等待恢复完成
5. 软件自动刷新数据

**⚠️ 注意**：恢复操作会覆盖当前数据库，请谨慎操作！

#### 10.6 备份清理

- 软件默认保留最近30个备份
- 可以在"设置"中调整保留数量
- 超过数量的旧备份自动删除

### 第十一章：GitHub Token高级设置

#### 11.1 Token的作用详解

| Token状态 | API限制 | 适用场景 |
|-----------|---------|----------|
| 无Token | 60次/小时 | 试用、少量仓库 |
| 有Token | 5000次/小时 | 正式使用、大量仓库 |

**计算示例**：
- 假设你关注100个仓库
- 每小时检查一次
- 无Token：60次/小时只能检查60个仓库
- 有Token：5000次/小时绰绰有余

#### 11.2 如何创建Token（图文详解）

**步骤1：进入Token管理页面**
```
GitHub首页 → 头像 → Settings → 
Developer settings → Personal access tokens → 
Tokens (classic)
```

**步骤2：生成新Token**
- 点击 "Generate new token (classic)"
- 填写 Note：`GitHub Release Monitor`
- Expiration：选择 "No expiration"（永不过期）或自定义时间
- **权限设置**：不要勾选任何权限！只需要public访问

**步骤3：复制Token**
- 生成后立即复制（关掉页面就看不到了）
- Token格式：`ghp_xxxxxxxxxxxxxxxxxxxx`

#### 11.3 在软件中配置Token

1. 点击"设置"按钮
2. 在"GitHub API设置"区域
3. 粘贴你的Token
4. 点击"测试Token有效性"
5. 看到"Token有效"提示即配置成功

#### 11.4 Token安全建议

✅ **好习惯**：
- 定期更换Token
- 只用于公开仓库监控
- 妥善保管（像密码一样）

❌ **坏习惯**：
- 分享给他人
- 上传到公开网络
- 截图包含完整Token

---

## 👨‍💻 专业开发人员手册

### 第十二章：系统架构

#### 12.1 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| GUI框架 | PySide6 (Qt for Python) | ≥6.0.0 |
| 数据库 | SQLite3 | 内置 |
| HTTP客户端 | Requests | ≥2.25.0 |
| 中文处理 | pypinyin | ≥0.50.0 |
| Python版本 | CPython | ≥3.8 |

#### 12.2 项目结构

```
GitHub_Release_Monitor/
├── GitHub_Release_Monitor.py  # 主程序
├── data/                       # 数据库目录
│   └── user_*.db              # 用户数据库文件
├── backups/                    # 备份目录
│   └── [用户名]/               # 各用户备份
├── users/                      # 用户配置
│   └── users.json              # 用户列表
└── icon.ico                    # 程序图标
```

#### 12.3 核心类设计

```
ProjectInfo          # 项目信息元数据
AppConfig            # 应用程序配置
DatabaseManager      # 数据库管理器
GitHubClient         # GitHub API客户端
PinyinConverter      # 拼音转换工具
MainWindow           # 主窗口
```

#### 12.4 数据库设计

**repositories表**
```sql
CREATE TABLE repositories (
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
);
```

**releases表**
```sql
CREATE TABLE releases (
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
);
```

### 第十三章：二次开发指南

#### 13.1 环境搭建

```bash
# 克隆代码
git clone https://github.com/duma520/GitHub_Release_Monitor.git
cd GitHub_Release_Monitor

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 13.2 主要功能扩展点

**1. 添加新的通知方式**

在`MainWindow`类中添加：

```python
def send_custom_notification(self, message):
    """自定义通知"""
    # 这里可以实现邮件、钉钉、企业微信等通知
    pass
```

**2. 扩展搜索功能**

修改`PinyinConverter`类：

```python
@staticmethod
def matches_custom(text: str, keyword: str) -> bool:
    """自定义匹配规则"""
    # 添加新的匹配逻辑
    pass
```

**3. 添加导出功能**

```python
def export_to_csv(self, filepath: str):
    """导出数据到CSV"""
    import csv
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入数据
        pass
```

#### 13.3 自定义GitHub API调用

**示例：获取仓库详情**

```python
def get_repo_details(self, repo_full_name: str) -> Dict:
    """获取仓库详细信息"""
    url = f"{self.base_url}/repos/{repo_full_name}"
    response = self.session.get(url)
    if response.status_code == 200:
        return response.json()
    return {}
```

#### 13.4 调试模式

开启调试模式（在设置中勾选"调试模式"）：
- 输出详细的API请求日志
- 显示数据库操作信息
- 记录线程执行状态

### 第十四章：性能优化

#### 14.1 数据库优化

```python
# 启用WAL模式（已在代码中实现）
self.connection.execute("PRAGMA journal_mode=WAL")

# 创建索引（已在代码中实现）
CREATE INDEX idx_releases_repo_id ON releases(repo_id)
CREATE INDEX idx_releases_published_at ON releases(published_at)
```

#### 14.2 API调用优化

**指数退避重试机制**：
```python
def get_releases_with_backoff(self, repo_full_name: str, max_retries: int = 3) -> List[Dict]:
    """带退避重试的获取releases"""
    for attempt in range(max_retries):
        result = self.get_releases(repo_full_name)
        if not result and attempt < max_retries - 1:
            wait_time = 2 ** attempt * 5  # 5, 10, 20秒
            time.sleep(wait_time)
        else:
            return result
    return []
```

#### 14.3 线程管理

```python
def stop_all_threads(self):
    """停止所有后台线程"""
    for thread in [self.check_thread, self.import_thread, self.search_thread]:
        if thread and thread.isRunning():
            if hasattr(thread, 'stop'):
                thread.stop()
            thread.wait(3000)  # 最多等待3秒
    gc.collect()  # 强制垃圾回收
```

### 第十五章：打包部署

#### 15.1 使用PyInstaller打包

```bash
# 安装PyInstaller
pip install pyinstaller

# 单文件打包
pyinstaller --onefile --windowed --icon=icon.ico GitHub_Release_Monitor.py

# 目录打包（启动更快）
pyinstaller --windowed --icon=icon.ico GitHub_Release_Monitor.py
```

#### 15.2 创建安装程序（Windows）

使用Inno Setup创建安装包：

```iss
[Setup]
AppName=GitHub Releases Monitor
AppVersion=1.1.15
DefaultDirName={pf}\GitHubReleaseMonitor
DefaultGroupName=GitHub Release Monitor

[Files]
Source: "dist\GitHub_Release_Monitor.exe"; DestDir: "{app}"
Source: "icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\GitHub Release Monitor"; Filename: "{app}\GitHub_Release_Monitor.exe"
```

#### 15.3 跨平台注意事项

**Windows**：
- 确保icon.ico文件存在
- 处理Windows防火墙提示

**macOS**：
- 需要代码签名或用户授权
- 使用.app捆绑包格式

**Linux**：
- 依赖Qt库（通过包管理器安装）
- 桌面快捷方式文件

---

## ❓ 常见问题解答（FAQ）

### 第十六章：新手常见问题

#### Q1：为什么我打不开软件？

**可能原因及解决方法**：

| 症状 | 原因 | 解决方法 |
|------|------|----------|
| 双击没反应 | 未安装Python | 安装Python 3.8+ |
| 报错"no module named..." | 缺少依赖 | 运行 pip install -r requirements.txt |
| 一闪而过 | Python版本太低 | 升级到Python 3.8+ |

#### Q2：如何添加仓库？

**方法一**：直接输入GitHub地址
```
https://github.com/用户名/仓库名
例如：https://github.com/curl/curl
```

**方法二**：输入用户名/仓库名
```
用户名/仓库名
例如：curl/curl
```

**方法三**：批量导入OPML
```
使用RSS阅读器导出OPML文件，然后导入
```

#### Q3：为什么我添加的仓库显示"仓库不存在"？

**可能原因**：
1. 仓库地址拼写错误（检查大小写）
2. 仓库是私有的（本软件只能监控公开仓库）
3. 仓库已被删除或改名

**解决方法**：
- 访问GitHub确认仓库存在
- 检查URL是否正确
- 如果是私有仓库，无法监控

#### Q4：检查更新时出现"API速率限制"怎么办？

**问题**：出现提示"达到API速率限制"

**原因**：没有配置GitHub Token，每小时只能查询60次

**解决**：配置GitHub Token（见11.3节）

**临时措施**：等待1小时后继续使用

#### Q5：如何备份我的数据？

**自动备份**：软件每天凌晨3点自动备份

**手动备份**：点击"手动备份"按钮

**备份位置**：软件目录下的 `backups/你的用户名/`

#### Q6：换了电脑，如何迁移数据？

1. **在旧电脑上**：
   - 找到 `data` 和 `backups` 文件夹
   - 复制 `users` 文件夹下的 `users.json`

2. **在新电脑上**：
   - 安装软件
   - 将复制的文件夹覆盖到相同位置
   - 启动软件，选择用户即可

#### Q7：如何修改检查间隔？

1. 点击"设置"按钮
2. 找到"检查间隔(秒)"
3. 修改数值（例如：3600秒=1小时）
4. 点击"确定"保存

#### Q8：为什么搜索不到我想要的仓库？

**可能原因**：
- 仓库名称包含特殊字符
- 搜索关键词太具体
- 数据库还未包含该仓库（需要先添加）

**建议**：
- 尝试更简单的关键词
- 确认仓库已被添加到列表
- 使用拼音首字母搜索

### 第十七章：进阶问题

#### Q9：可以同时监控多少个仓库？

**理论上**：没有上限

**实际限制**：
- 有Token：5000次/小时 ÷ 检查次数
- 无Token：60次/小时 ÷ 检查次数

**计算示例**：
- 每小时检查一次
- 有Token：可监控5000个仓库
- 无Token：只能监控60个仓库

#### Q10：软件会消耗多少系统资源？

| 操作 | CPU | 内存 | 网络 |
|------|-----|------|------|
| 空闲 | 0-1% | 50-80MB | 无 |
| 检查更新 | 5-10% | 80-120MB | 少量 |
| 搜索 | 2-5% | 100-150MB | 无 |

#### Q11：如何备份到其他位置？

目前不支持自定义备份路径，但可以通过以下方式：

1. **计划任务同步**：
```batch
@echo off
xcopy "软件目录\backups" "D:\我的备份\GitHub监控\" /E /I /Y
```

2. **软链接**（Windows）：
```cmd
mklink /J "软件目录\backups" "D:\我的备份\GitHub监控\backups"
```

#### Q12：如何导出仓库列表？

目前暂无导出功能，可通过数据库文件导出：

```sql
-- 直接操作数据库文件
sqlite3 data\user_xxx.db
.headers on
.mode csv
.output repos.csv
SELECT * FROM repositories;
.quit
```

#### Q13：如何更新软件版本？

**方法一**：下载新版本覆盖
1. 从GitHub Releases下载最新版
2. 覆盖旧文件（保留data、backups、users文件夹）

**方法二**：使用Git更新
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

#### Q14：如何报告问题或建议新功能？

1. 访问项目Issues页面：
   https://github.com/duma520/GitHub_Release_Monitor/issues

2. 点击"New Issue"

3. 选择类型：
   - Bug report（问题报告）
   - Feature request（功能建议）

4. 填写详细信息：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 截图（如有）

---

## 🔧 故障排除指南

### 第十八章：常见错误及解决方案

#### 错误1：`ConnectionError` 连接错误

**现象**：
```
连接错误 curl/curl: HTTPSConnectionPool(host='api.github.com', port=443)
```

**原因**：
- 网络不通
- 需要代理但未配置
- GitHub被屏蔽

**解决方案**：

1. **检查网络**：
   ```bash
   ping github.com
   ```

2. **配置代理**（见第九章）

3. **使用镜像**（如修改hosts文件）：
   ```
   140.82.114.4 github.com
   199.232.69.194 github.global.ssl.fastly.net
   ```

#### 错误2：`sqlite3.IntegrityError` 数据库错误

**现象**：
```
UNIQUE constraint failed: repositories.full_name
```

**原因**：尝试添加已存在的仓库

**解决**：
- 仓库已存在，无需重复添加
- 如需重新添加，先删除原仓库

#### 错误3：`PermissionError` 权限错误

**现象**：
```
PermissionError: [WinError 32] 另一个程序正在使用此文件
```

**原因**：
- 数据库文件被其他进程占用
- 修改用户名时文件未释放

**解决方案**：
1. 关闭所有程序实例
2. 等待几秒后重试
3. 检查是否有杀毒软件锁定文件

#### 错误4：`JSONDecodeError` 解析错误

**现象**：
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**原因**：
- API返回的不是JSON格式
- 可能是HTML错误页面

**解决**：
1. 检查网络连接
2. 可能是GitHub服务暂时异常
3. 稍后重试

### 第十九章：性能问题排查

#### 症状1：软件启动慢

**可能原因**：
- 数据库过大（上万条记录）
- 同时加载太多数据

**优化方案**：
```sql
-- 优化数据库
VACUUM;
-- 删除过期数据
DELETE FROM releases WHERE published_at < date('now', '-1 year');
```

#### 症状2：检查更新很慢

**可能原因**：
- 网络延迟高
- 仓库数量多
- 遇到速率限制

**优化方案**：
1. 配置Token提高限制
2. 延长检查间隔
3. 分批监控（使用多用户）

#### 症状3：内存占用过高

**可能原因**：
- 线程未正常退出
- 数据库连接未关闭

**解决方案**：
```python
# 确保正确关闭连接
def closeEvent(self, event):
    self.stop_all_threads()
    if self.db:
        self.db.close()
    event.accept()
```

---

## 💡 最佳实践建议

### 第二十章：不同用户群体的最佳实践

#### 20.1 普通用户（关注少量项目）

**场景**：关注5-10个常用工具

**建议配置**：
- ✅ 配置GitHub Token（5000次/小时足够）
- ✅ 检查间隔：6小时（86400秒）
- ✅ 备份保留：10个
- ✅ 开启自动备份

**推荐仓库**：
```
curl/curl          # 网络传输工具
FFmpeg/FFmpeg      # 音视频处理
nodejs/node        # Node.js运行时
python/cpython     # Python语言
git/git            # Git版本控制
```

#### 20.2 开发者（关注技术生态）

**场景**：关注30-50个技术项目

**建议配置**：
- ✅ 必须配置Token
- ✅ 检查间隔：2小时
- ✅ 备份保留：30个
- ✅ 定期手动备份

**分类管理建议**：
- 创建多个用户分类（如：前端、后端、工具）
- 使用OPML导入已有订阅
- 定期清理不活跃项目

#### 20.3 团队管理员（多人共用）

**场景**：5-10人团队共用一台服务器

**建议配置**：
- ✅ 为每个成员创建独立用户
- ✅ 统一Token管理（使用团队账号）
- ✅ 检查间隔：1小时
- ✅ 备份保留：60个
- ✅ 定期备份到其他位置

**权限管理**：
- 团队成员只能看到自己的数据
- 管理员可以查看所有用户
- 重要操作（如删除用户）需授权

#### 20.4 企业用户（大规模监控）

**场景**：监控数百个内部和开源项目

**建议配置**：
- ✅ 必须配置Token（考虑多个备用）
- ✅ 检查间隔：30分钟
- ✅ 备份保留：90个
- ✅ 开启调试模式监控状态
- ✅ 外置存储定期备份

**高级设置**：
```python
# 自定义通知（示例：企业微信）
def send_wechat_notification(self, updates):
    webhook = "https://qyapi.weixin.qq.com/..."
    data = {"msgtype": "text", "text": {"content": str(updates)}}
    requests.post(webhook, json=data)
```

### 第二十一章：数据管理最佳实践

#### 21.1 定期维护

**每周维护**：
- 检查是否有仓库不再更新
- 清理不活跃的仓库
- 查看日志有无异常

**每月维护**：
- 执行数据库优化
- 检查备份完整性
- 更新Token（如有需要）

**每季度维护**：
- 整理备份文件
- 评估监控列表
- 软件版本更新检查

#### 21.2 备份策略

**3-2-1备份原则**：
- **3**份数据副本（1份原数据+2份备份）
- **2**种存储介质（如：硬盘+云存储）
- **1**份异地备份（如：其他电脑/服务器）

**实施示例**：
1. 软件自动备份（本地硬盘）
2. 每周手动复制到外置硬盘
3. 每月同步到云存储（如：百度网盘）

#### 21.3 性能优化建议

**数据库优化**：
```sql
-- 定期执行VACUUM（每年1-2次）
VACUUM;

-- 删除1年前的旧记录
DELETE FROM releases 
WHERE published_at < datetime('now', '-1 year');
```

**监控策略优化**：
- 高频率项目：重要且频繁更新的仓库（检查间隔短）
- 低频率项目：稳定不常更新的仓库（检查间隔长）

---

## 📋 附录

### 附录A：GitHub Release URL格式参考

| 仓库 | Release页面 | Atom订阅 |
|------|-------------|----------|
| curl/curl | https://github.com/curl/curl/releases | https://github.com/curl/curl/releases.atom |
| FFmpeg/FFmpeg | https://github.com/FFmpeg/FFmpeg/releases | https://github.com/FFmpeg/FFmpeg/releases.atom |
| nodejs/node | https://github.com/nodejs/node/releases | https://github.com/nodejs/node/releases.atom |
| python/cpython | https://github.com/python/cpython/releases | https://github.com/python/cpython/releases.atom |
| git/git | https://github.com/git/git/releases | https://github.com/git/git/releases.atom |

### 附录B：常用GitHub仓库推荐

#### 开发工具
- **Microsoft/vscode** - Visual Studio Code编辑器
- **atom/atom** - Atom编辑器
- **vim/vim** - Vim编辑器
- **notepad-plus-plus/notepad-plus-plus** - Notepad++

#### 编程语言
- **python/cpython** - Python
- **nodejs/node** - Node.js
- **golang/go** - Go语言
- **rust-lang/rust** - Rust语言

#### 框架和库
- **vuejs/vue** - Vue.js框架
- **facebook/react** - React框架
- **angular/angular** - Angular框架
- **django/django** - Django框架

#### 数据库
- **mysql/mysql-server** - MySQL
- **postgres/postgres** - PostgreSQL
- **redis/redis** - Redis
- **mongodb/mongo** - MongoDB

#### 网络工具
- **curl/curl** - 网络传输工具
- **wget/wget** - 文件下载工具
- **nginx/nginx** - Web服务器
- **apache/httpd** - Apache服务器

### 附录C：OPML文件示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
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
                    text="Node.js releases" 
                    title="Node.js releases" 
                    xmlUrl="https://github.com/nodejs/node/releases.atom" 
                    htmlUrl="https://github.com/nodejs/node/releases"/>
        </outline>
    </body>
</opml>
```

### 附录D：命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--version` | 显示版本信息 | `python GitHub_Release_Monitor.py --version` |
| `--help` | 显示帮助信息 | `python GitHub_Release_Monitor.py --help` |
| `--user USER` | 指定用户启动 | `python GitHub_Release_Monitor.py --user "张三"` |
| `--debug` | 启用调试模式 | `python GitHub_Release_Monitor.py --debug` |

### 附录E：配置文件说明

配置文件位置：`用户目录/.config/GitHubMonitor/用户名.conf`

```ini
[GitHub]
token = ghp_xxxxxxxxxxxx
use_proxy = true
proxy_host = 127.0.0.1
proxy_port = 20808

[Monitor]
check_interval = 3600
backup_count = 30
debug_mode = false

[Window]
geometry = ...  # 窗口位置和大小
state = ...     # 窗口状态
```

### 附录F：版本兼容性说明

| 软件版本 | Python版本 | PySide6版本 | 操作系统 |
|---------|-----------|------------|---------|
| 1.1.x | 3.8-3.11 | 6.0-6.4 | Windows 7+/macOS 10.15+/Linux |
| 1.0.x | 3.6-3.9 | 5.15 | Windows 7+/macOS 10.14+/Linux |

### 附录G：术语表

| 术语 | 解释 |
|------|------|
| **GitHub** | 全球最大的代码托管平台 |
| **Repository/仓库** | 存放项目代码的地方 |
| **Release/版本发布** | 开发者正式发布的软件版本 |
| **Token** | 访问GitHub API的凭证 |
| **OPML** | 用于交换订阅列表的格式 |
| **API** | 应用程序编程接口，用于程序间通信 |
| **Rate Limit/速率限制** | API的访问频率限制 |
| **Proxy/代理** | 中间服务器，帮助访问网络 |
| **SQLite** | 轻量级嵌入式数据库 |
| **PySide6** | Python的Qt界面库 |

### 附录H：快捷键参考

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+F` | 聚焦搜索框 |
| `Ctrl+N` | 添加新仓库 |
| `Ctrl+U` | 检查更新 |
| `Ctrl+S` | 打开设置 |
| `Ctrl+B` | 手动备份 |
| `Ctrl+R` | 打开恢复对话框 |
| `Ctrl+1` | 切换到仓库列表 |
| `Ctrl+2` | 切换到更新记录 |
| `Ctrl+3` | 切换到日志 |
| `F5` | 刷新当前列表 |
| `Ctrl+Q` | 退出程序 |

---

## 📝 结语

感谢您选择使用 **GitHub Releases 监控程序**！我们希望这份详尽的指南能帮助您充分利用本软件的所有功能。

无论您是初学者还是专业开发者，本软件都致力于为您提供简洁高效的GitHub Releases监控体验。我们会持续改进软件，添加新功能，优化用户体验。

如果您有任何问题、建议或想法，欢迎通过以下渠道与我们交流：

- **项目主页**：https://github.com/duma520/GitHub_Release_Monitor
- **问题反馈**：通过GitHub Issues提交
- **版本更新**：关注GitHub Releases页面

**再次感谢您的使用！**

---

*版权所有 © 永久 杜玛 保留所有权利*

*本文档内容未经书面许可不得转载或用于商业用途。所有技术支持都通过公开渠道进行，以便其他用户也能受益。*
