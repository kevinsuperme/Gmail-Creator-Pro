# 🚀 Gmail Creator Pro - 终极 Gmail 账户创建工具

<div align="center">

![Gmail Creator Pro](https://img.shields.io/badge/Version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**✨ 终极自动化 Gmail 账户创建工具 ✨**

*高级反检测系统 • 手机验证绕过 • 5sim 集成 • 精美现代界面*

[功能特性](#-核心功能) • [安装指南](#-安装指南) • [使用方法](#-使用方法) • [配置说明](#-配置说明) • [技术支持](#-联系与支持)

---

![Gmail Creator Pro 界面](gmail.png)

*Gmail Creator Pro v2.0.0 运行截图*

---

</div>

## 📋 目录

- [项目概述](#-项目概述)
- [核心功能](#-核心功能)
- [界面截图](#-界面截图)
- [环境要求](#-环境要求)
- [安装指南](#-安装指南)
- [配置说明](#-配置说明)
- [使用方法](#-使用方法)
- [项目结构](#-项目结构)
- [高级功能](#-高级功能)
- [常见问题](#-常见问题)
- [安全与法律](#-安全与法律)
- [参与贡献](#-参与贡献)
- [联系与支持](#-联系与支持)
- [许可证](#-许可证)

---

## 🎯 项目概述

**Gmail Creator Pro** 是一款功能强大的 Python 自动化工具，专为自动创建 Gmail 账户而设计。该工具集成了先进的反检测系统、智能手机验证绕过机制以及无缝的 5sim API 集成，提供了一套专业的 Gmail 账户批量创建解决方案，并配备精美的现代化界面。

### 本工具的特色亮点

- 🛡️ **高级反检测** - 模拟真人行为以规避检测
- 🔄 **智能手机验证** - 多种绕过策略 + 5sim 集成
- 🎨 **精美界面** - Rich 控制台界面，实时进度追踪
- ⚡ **极速创建** - 针对批量账户创建进行性能优化
- 🔒 **安全可配置** - 独立配置文件，便于自定义设置
- 📊 **统计面板** - 追踪成功率和账户详情

---

## ✨ 核心功能

### 🚀 高级反检测系统
- **模拟人工输入** - 按键间随机延迟（0.1-0.3 秒）
- **会话预热** - 预先浏览 Google、BBC、Wikipedia、YouTube 以模拟真人行为
- **随机 User Agent** - 为每个账户轮换浏览器指纹
- **自然延迟** - 操作间随机等待时间（0.5-1.2 秒）
- **Navigator 属性修改** - 隐藏自动化特征签名
- **真实姓名生成** - 使用外部文件中的姓名以增强真实性

### 🔒 手机验证绕过
- **多种跳过策略** - 自动检测并点击跳过按钮
- **备用方法检测** - 尝试"Try another way"选项
- **5sim API 集成** - 自动购买手机号码并获取短信验证码
- **智能重试逻辑** - 单一策略失败时启用多种回退方案
- **多语言支持** - 兼容英文和阿拉伯文的跳过按钮

### 🌐 智能代理集成
- **内置代理支持** - 集成 FreeProxy 实现 IP 轮换
- **自动代理选择** - 为每个账户随机选择代理
- **代理验证** - 使用前确保代理可用

### 💻 精美现代界面
- **Rich 控制台界面** - 带颜色和动画的精美终端界面
- **实时进度条** - 可视化追踪账户创建进度
- **详细统计数据** - 成功率、总账户数、活跃账户数
- **颜色编码消息** - 绿色表示成功，红色表示错误，黄色表示警告
- **交互式菜单** - 易用的菜单系统

### 📊 详细统计信息
- **已创建账户总数** - 追踪所有创建的账户
- **活跃账户计数** - 监控账户状态
- **成功率百分比** - 计算创建成功率
- **最近创建时间戳** - 追踪近期活动
- **账户详情** - 查看所有已保存的账户信息

### 💾 自动保存账户
- **JSON 格式存储** - 结构化的账户数据存储
- **自动备份** - 账户创建后立即保存
- **账户元数据** - 包含邮箱、密码、创建日期、状态
- **便捷导出** - 简单的 JSON 格式便于数据导出

### 🔄 失败自动重试
- **健壮的错误处理** - 失败时多次重试
- **元素检测** - 多种选择器策略定位元素
- **页面加载重试** - 首次加载失败时重试
- **智能回退** - 主方法失败时启用备用方案

### ⚡ 极速创建
- **性能优化** - 高效代码实现快速执行
- **支持并行处理** - 架构支持未来的并行化扩展
- **资源占用低** - 轻量高效
- **快速浏览器启动** - 快速初始化 Chrome 驱动

### 🔐 安全配置
- **独立配置文件** - 便于混淆主脚本同时保持配置可编辑
- **密码保护** - 密码安全存储于独立文件
- **API 密钥管理** - API 密钥安全存储
- **无硬编码密钥** - 所有敏感数据存放于外部文件

### 🎯 附加功能
- **自定义 User Agent** - 支持自定义 User Agent 列表
- **自定义姓名库** - 使用您自己的姓名列表
- **生日配置** - 可自定义生日设置
- **性别选择** - 支持男、女、其他
- **多语言支持** - 兼容英文和阿拉伯文界面
- **ChromeDriver 自动管理** - 自动下载和配置 ChromeDriver

---

## 📸 界面截图

<div align="center">

![主界面](gmail2.png)

*Gmail Creator Pro v2.0.0 - 主界面*

</div>

### 界面特色：
- **欢迎横幅** - 精美的 ASCII 艺术横幅，含版本信息
- **功能列表** - 所有功能的可视化清单
- **菜单系统** - 含 5 个选项的交互式菜单
- **进度追踪** - 实时进度条
- **统计面板** - 详细的账户创建统计数据

---
## 📚 完整教程

<div align="center">

### 🎥 YouTube 视频演示

[![观看视频](https://img.youtube.com/vi/2TucpXay1Sk/maxresdefault.jpg)](https://youtu.be/2TucpXay1Sk)

### [在 YouTube 上观看视频](https://youtu.be/2TucpXay1Sk)

</div>

---

### 📝 深度技术文章

📖 阅读完整的分步指南和详细说明：  
👉 https://www.shadowhackr.com/2026/01/gmail-creator-pro.html
---
## 📋 环境要求

### 系统要求
- **操作系统：** Windows 10/11（推荐）
- **Python 版本：** Python 3.8 或更高版本（推荐 Python 3.12）
- **Chrome 浏览器：** 已安装最新版本
- **网络连接：** 需要稳定的网络连接
- **内存：** 最低 4GB（推荐 8GB）
- **磁盘空间：** 500MB 可用空间

### Python 依赖

所有依赖列于 `requirements.txt` 中。使用以下命令安装：

```bash
pip install -r requirements.txt
```

**必需的包：**
- `selenium>=4.15.0` - Web 自动化框架
- `webdriver-manager>=4.0.0` - 自动管理 ChromeDriver
- `rich>=13.7.0` - 精美的终端 UI 库
- `requests>=2.31.0` - 用于 API 调用的 HTTP 库
- `unidecode>=1.3.7` - 文本规范化
- `beautifulsoup4>=4.12.0` - HTML 解析
- `fp>=0.1.0` - 免费代理集成

### 可选要求
- **5sim API 密钥** - 用于自动手机验证（可选但推荐）
- **Microsoft Visual C++ Build Tools** - 用于 Nuitka 编译（可选）

---

## 🛠️ 安装指南

### 第 1 步：克隆仓库

```bash
git clone https://github.com/ShadowHackrs/gmail-account-creator.git
cd Gmail2025
```

或下载 ZIP 文件并解压。

### 第 2 步：安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 第 3 步：配置设置

运行工具前，您需要配置以下文件：

#### 3.1. 密码配置

编辑 `config/password.txt`：
```
YourStrongPassword123!
```

**密码要求：**
- 至少 8 个字符
- 包含大写字母、小写字母、数字和特殊字符的组合
- 必须符合 Google 的密码要求

#### 3.2. 姓名配置

编辑 `data/names.txt`：
```
Ahmed Mohamed
Mohamed Ali
Omar Ibrahim
Sarah Ahmed
Shadow Hacker
...
```

**格式说明：**
- 每行一个姓名
- 格式："名 姓" 或仅 "名"
- 可根据需要添加任意数量的姓名

#### 3.3. 5sim API 配置（可选但推荐）

1. 从 [5sim.net](https://5sim.net/) **获取您的 API 密钥**
2. 在 `config/5sim_config.txt` 中 **添加您的 API 密钥**：
```
your_api_key_here
```

3. 在 `config/config.py` 中 **配置国家**：
```python
FIVESIM_COUNTRY = "usa"  # 选项：usa, russia, ukraine, kazakhstan 等
FIVESIM_OPERATOR = "any"  # 选项：any, virtual 等
```

#### 3.4. User Agent 配置（可选）

编辑 `config/user_agents.txt`：
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
...
```

#### 3.5. 通用配置

编辑 `config/config.py`：
```python
# 账户配置
YOUR_BIRTHDAY = "2 4 1950"  # 格式："月 日 年"
YOUR_GENDER = "1"  # 1=男, 2=女, 3=其他
YOUR_PASSWORD = ""  # 留空则从 password.txt 读取

# 5sim API 配置
FIVESIM_API_KEY = ""  # 留空则从 5sim_config.txt 读取
FIVESIM_COUNTRY = "usa"
FIVESIM_OPERATOR = "any"

# 姓名配置
USE_ARABIC_NAMES = True
NAMES_FILE = "data/names.txt"
```

### 第 4 步：验证安装

运行脚本以验证一切配置正确：

```bash
python auto_gmail_creator.py
```

您应该能看到欢迎横幅和菜单。如果出现任何错误，请查阅[常见问题](#-常见问题)章节。

---

## ⚙️ 配置说明

### 配置文件结构

```
config/
├── config.py          # 通用设置
├── password.txt       # 账户密码
├── 5sim_config.txt    # 5sim API 密钥（可选）
└── user_agents.txt    # User Agent 列表（可选）

data/
├── names.txt          # 姓名列表
└── accounts.json      # 已创建的账户（自动生成）
```

### 详细配置指南

#### 账户设置

**生日格式：** `"月 日 年"`（例如 "2 4 1950"）
- 月：1-12
- 日：1-31
- 年：1900-2010（必须年满 18 岁）

**性别选项：**
- `"1"` - 男
- `"2"` - 女
- `"3"` - 其他

#### 5sim API 设置

**可用国家：**
- `usa` - 美国
- `russia` - 俄罗斯
- `ukraine` - 乌克兰
- `kazakhstan` - 哈萨克斯坦
- 更多国家请查阅 [5sim.net](https://5sim.net/) 完整列表

**运营商选项：**
- `any` - 任意可用运营商
- `virtual` - 仅虚拟号码
- 特定运营商名称

**获取 5sim API 密钥：**
1. 访问 [5sim.net](https://5sim.net/)
2. 创建账户
3. 进入 API 板块
4. 生成 API 密钥
5. 为账户充值
6. 将 API 密钥复制到 `config/5sim_config.txt`

---

## 🚀 最新更新 (v2.1.0)

### ✨ 全新版本发布！

我们很高兴地宣布 **Gmail Creator Pro** 的最新更新，带来多项重大改进和增强。

🔗 关联项目 / 更新：  
https://github.com/ShadowHackrs/Gmail-infinity

---

### 🔥 新增特性

- ⚡ 提升自动化稳定性和性能
- 🛠️ 修复账户创建流程中的多个缺陷
- 🎯 更好地处理 UI 变更和选择器
- 📊 增强统计追踪系统
- 🔄 优化重试和恢复逻辑
- 💻 提升整体界面响应速度
- 🔐 强化配置结构和文件处理

---

### 📌 注意事项

- 本次更新聚焦于 **稳定性 + 性能优化**
- 建议使用 `requirements.txt` 更新依赖
- 确保 Chrome 浏览器已更新至最新版本以获得最佳兼容性

---

⭐ 如果您喜欢本次更新，别忘了给仓库点个 Star！
