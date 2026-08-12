# JBOD Validation Platform

<div align="center">

Enterprise-level JBOD Validation Management Platform built with Django.

The platform provides a complete validation workflow including:

- Dashboard Monitoring
- Model Management
- Firmware Management
- Test Case Management
- Test Plan Management
- Validation Management
- Validation Execution
- Authentication System
- Execution Status Tracking

Designed for enterprise JBOD validation and automation.

企業級 JBOD 驗證管理平台

</div>

---

## 📖 Introduction / 專案介紹

JBOD Validation Platform is an enterprise-level web application built with Django for validating and managing JBOD (Just a Bunch Of Disks) storage systems.

JBOD Validation Platform 是一套以 Django 開發的企業級 JBOD（Just a Bunch Of Disks）驗證管理平台，提供完整的驗證流程管理、測試規劃、執行追蹤、狀態管理與後續報告擴充能力。

---

## ✨ Features / 功能特色

* Dashboard / 儀表板
* Model Management / Model 管理
* Firmware Management / Firmware 管理
* Test Case Management / Test Case 管理
* Test Plan Management / Test Plan 管理
* Validation Center / Validation 管理
* Execute Validation Workflow / 驗證執行流程
* Execution Progress Tracking / 執行進度追蹤
* Current Test Case Tracking / 目前測試案例追蹤
* Execution Status Management / 執行狀態管理
* Execution Timeout Handling / 執行逾時處理
* Execution Log Recording / 執行日誌記錄
* Authentication System / 使用者驗證系統
* Report Center (Planned) / 報告中心（規劃中）
* Log Center (Planned) / 日誌中心（規劃中）

---

## 🏗 System Architecture / 系統架構

JBOD Validation Platform
│
├── Dashboard
│
├── Asset Management
│   ├── Models
│   └── Firmware
│
├── Validation Management
│   ├── Test Case
│   ├── Test Plan
│   └── Validation
│
├── Execute
│   ├── Execute Job
│   ├── Progress Tracking
│   ├── Current Test Case
│   ├── Execution Status
│   ├── Timeout Handling
│   └── Execution Logs
│
├── Report
│   └── Planned
│
└── User
    └── Authentication
    
---
    
## 📊 Development Progress / 開發進度
| Module            |   Progress  | Status / 說明                                                                                       |
| ----------------- | :---------: | ------------------------------------------------------------------------------------------------- |
| Dashboard         |  ✅ **100%** | 儀表板、統計卡片、Recent Jobs、Latest Firmware、Component 化完成。                                               |
| User              |  ✅ **100%** | Login、Register、Remember Username、Auto Login、Enterprise Login UI 已完成。                              |
| Models            |  ✅ **100%** | CRUD、搜尋、Detail、Edit、Delete、Component 化完成。                                                         |
| Firmware          |  ✅ **100%** | CRUD、搜尋、Filter、Component 化完成。                                                                     |
| Test Case         |  ✅ **100%** | CRUD 已完成，UI 與 URL Routing 已統一。                                                                    |
| Test Plan         |  ✅ **100%** | CRUD 已完成，可建立及管理測試計畫。                                                                              |
| Validation        |  ✅ **100%** | Validation Center、CRUD、Routing 完成                                                      |
| Execute           |   ✅ **100%** | Execute Job、PASS / FAIL / TIMEOUT、Progress、Current TestCase、Execution Log 與 Timeout Handling 已完成。 |
| Report            |  🔴 **0%**  | Coming Soon / 尚未開始。                                                                               |
| Logs              |  🟡 **30%**  | Execute Log 已建立，獨立 Log Center 尚未完成始。                                                                               |
| Automation Engine | 🟡 **40%** | 基礎 Execution Engine 已完成，硬體自動化尚未整合           |

---

## 🛠 Tech Stack / 技術架構
| Category        | Technology         | 說明       |
| --------------- | ------------------ | -------- |
| Backend         | Django 6.x         | Web 後端框架 |
| Language        | Python 3.14        | 程式語言     |
| Frontend        | HTML5, Bootstrap 5 | 前端 UI    |
| CSS             | CSS3               | UI 樣式    |
| Database        | SQLite3            | 開發階段資料庫  |
| Icons           | Font Awesome       | UI 圖示    |
| Version Control | Git                | 版本控制     |
| Repository      | GitHub             | 原始碼管理    |
| IDE             | Visual Studio Code | 開發工具     |

---

## 📁 Project Structure / 專案架構
JBOD-Validation/
│
├── dashboard/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── executor/
│   ├── services/
│   │   └── execution.py
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── ...
│
├── firmware/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── ...
│
├── models_app/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── ...
│
├── testcase/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── ...
│
├── testplan/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── ...
│
├── validation/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── ...
│
├── report/
│
├── logs/
│
├── user/
│
├── static/
│   └── css/
│
├── templates/
│   ├── base.html
│   └── includes/
│
├── docs/
│
├── manage.py
├── requirements.txt
└── README.md

---

## ⚙ Installation / 安裝方式

* Clone Repository / 複製專案
> git clone https://github.com/shingyu0205/JBOD-Validation.git

* Enter Project / 進入專案
> cd JBOD-Validation

* Create Virtual Environment / 建立虛擬環境
> python -m venv .venv

* Activate Virtual Environment / 啟用虛擬環境
> .\.venv\Scripts\Activate.ps1
   
* 如果遇到 Execution Policy 問題：
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

* 然後重新：
> .\.venv\Scripts\Activate.ps1

* Install Dependencies / 安裝套件
> pip install -r requirements.txt

* Database Migration / 建立資料庫
> python manage.py makemigrations
> python manage.py migrate

* System Check / 系統檢查
> python manage.py check

* Expected result:
> System check identified no issues (0 silenced).

* Run Server / 啟動伺服器
> python manage.py runserver

* Open Browser / 開啟瀏覽器
> http://127.0.0.1:8000/

---
## 📦 Main Applications / 主要模組

| App        | Description          | 中文            |
| ---------- | -------------------- | ------------- |
| dashboard  | Dashboard            | 儀表板           |
| models_app | Model Management     | Model 管理      |
| firmware   | Firmware Management  | Firmware 管理   |
| testcase   | Test Case Management | Test Case 管理  |
| testplan   | Test Plan Management | Test Plan 管理  |
| validation | Validation Center    | Validation 管理 |
| executor   | Execute Validation   | 執行驗證          |
| report     | Report Center        | 報告中心          |
| logs       | Log Center           | 日誌中心          |
| user       | User Management      | 使用者管理         |

---
## ⚙ Execution Engine / 執行引擎

Execution Engine 負責執行 Test Plan 中的 Test Case，並管理每一個測試案例的執行狀態。

目前支援：
TestPlan
   │
   ▼
ExecuteJob
   │
   ├── TestCase 1
   │      ├── PASS
   │      ├── FAIL
   │      └── TIMEOUT
   │
   ├── TestCase 2
   │
   └── TestCase N

### Execution Status
| Status  | 說明      |
| ------- | ------- |
| PENDING | 等待執行    |
| RUNNING | 執行中     |
| PASS    | 全部測試成功  |
| FAIL    | 測試失敗    |
| STOP    | 使用者停止執行 |

### Test Case Execution Status
| Status  | 說明       |
| ------- | -------- |
| PASS    | 測試成功     |
| FAIL    | 測試失敗     |
| TIMEOUT | 超過指定執行時間 |

---
## ⏱ Timeout Handling / 執行逾時處理
Execution Engine 支援 Test Case Timeout。

例如：
```
Command:
python -c "import time; time.sleep(10)"

Timeout:
3 seconds
```

Execution Engine 會：
Start Process
     │
     ▼
Wait for Timeout
     │
     ├── Process Finished
     │       ↓
     │      PASS / FAIL
     │
     └── Timeout
             ↓
       TIMEOUT Status
             ↓
       Terminate Process Tree
             ↓
       Record Execution Log
       
Timeout 結果包含：

* Timeout Status
* Execution Duration
* Process ID
* Termination Result
* Execution Log

Windows 環境下使用 Process Tree Termination 避免子程序持續執行。

---
## 📈 Execution Tracking / 執行追蹤
ExecuteJob 目前記錄：
* Job Status
* Progress
* Start Time
* End Time
* Current TestCase
* Current Test Index

例如：
```
Job #30

Status:
FAIL

Progress:
100%

Current TestCase:
ENGINE-TIMEOUT

Current Test Index:
1
```

---
## 📝 Execution Logs / 執行日誌
Execution Engine 會記錄 Test Case 執行過程。

```
Example:
INFO
Validation started.

INFO
Test Case started: ENGINE-TIMEOUT

FAIL
Test Case timeout: ENGINE-TIMEOUT
Timeout: 3 seconds
```

每筆 Log 包含：
* Log Level
* Test Case
* Message
* Duration
* Created Time

---
## 🔗 URL Structure / URL 架構

目前主要 URL：

| Module     | URL            | Name              |
| ---------- | -------------- | ----------------- |
| Dashboard  | `/`            | `dashboard`       |
| Models     | `/models/`     | `model_list`      |
| Firmware   | `/firmware/`   | `firmware_list`   |
| Test Case  | `/testcase/`   | `testcase_list`   |
| Test Plan  | `/testplan/`   | `testplan_list`   |
| Validation | `/validation/` | `validation_list` |
| Executor   | `/executor/`   | `executor:index`  |

---
## 🏷 Version Naming Convention / 版本命名規範

This project follows Semantic Versioning (SemVer).

本專案採用 Semantic Versioning（SemVer）。

| Version | Description      | 中文             |
| ------- | ---------------- | ---------------  |
| Major   | Breaking Changes | 架構重大變更      |
| Minor   | New Features     | 新功能            |
| Patch   | Bug Fixes        | Bug 修正與小幅改善 |

Example:
v1.0.0
   ↓
v1.1.0
   ↓
v1.1.1
   ↓
v1.2.0

---
## 📜 Release History / 版本歷程
### v1.2.1 - 2026-08-12
**Fixes / Bug Fixes**
- Fixed Authentication Login URL routing
- Fixed Login redirect with `next` parameter
- Fixed Validation namespace routing
- Fixed Test Case namespace routing
- Fixed Test Plan namespace routing
- Fixed Dashboard URL reverse errors
- Fixed Validation Add page routing
- Fixed Test Plan Add page routing
- Fixed Test Case page template routing issue
- Fixed Sidebar navigation links

**Improved / UI Improvements**
- Unified Django URL namespace architecture
- Improved Authentication flow
- Improved Dashboard navigation
- Improved Validation Center navigation
- Improved Test Case navigation
- Improved Test Plan navigation
- Unified Chinese / English UI naming
- Improved Sidebar navigation structure
- Disabled unavailable Reports and Logs navigation
- Improved Dashboard UI consistency

**Stability**
- Verified Dashboard
- Verified Login / Logout
- Verified Models navigation
- Verified Firmware navigation
- Verified Test Case navigation
- Verified Test Plan navigation
- Verified Validation navigation
- Verified Execute navigation
- Verified Execute PASS test
- Verified Execute TIMEOUT test


### v1.2.0 — 2026-08-11

**🚀 Execution Engine**
* Added Execution Engine process execution.
* Added Test Case execution.
* Added PASS / FAIL / TIMEOUT handling.
* Added execution timeout handling.
* Added Windows Process Tree termination.
* Added execution duration measurement.
* Added current TestCase tracking.
* Added current Test Index tracking.
* Added execution progress tracking.
* Added execution logs.

**🔧 Executor**
* Improved Execute Job lifecycle.
* Improved Execute Detail page.
* Added execution status tracking.
* Added current execution information.
* Added TestPlan execution workflow.
* Added execution status API.
* Improved Executor URL routing.

**🧪 Validation**
* Improved Validation workflow.
* Improved Test Case / Test Plan integration.
* Improved execution workflow between Validation and Executor.

**🎨 UI**
* Improved Dashboard UI.
* Improved Sidebar navigation.
* Improved Execute UI.
* Improved Execute Detail UI.
* Improved Login layout.
* Login page hides application Sidebar and Navbar.
* Improved URL navigation.
* Improved UI consistency.

**🔗 Routing**
* Standardized Test Case URL naming.
* Standardized Test Plan URL naming.
* Standardized Validation URL naming.
* Improved reverse URL lookup.
* Fixed URL namespace conflicts.
* Fixed Dashboard navigation links.

**🚧 Planned Modules**
* Reports
* Logs

These modules are currently displayed as:

> Coming Soon

and are intentionally disabled in the Sidebar.

---

### v1.1.2 — 2026-08-05
**Added**
* Reusable Page Header Component
* Reusable Statistic Card Component
* Reusable Status Badge Component
* Reusable Search Form Component
* Reusable Empty State Component
**Improved**
* Dashboard UI Refactoring
* Model Management UI Refactoring
* Firmware Management UI Refactoring
* Unified UI Component Library
* Improved Code Reusability
* Enhanced UI Consistency

---
### v1.1.1 — 2026-08-05
**New Features**
* Enterprise Login UI
* User Registration
* Auto Login after Registration
* Remember Username
* Password Visibility Toggle
**Improvements**
* Redesigned Login Interface
* Improved Authentication Module
* Updated Project Structure
* Enhanced UI Consistency

---
### v1.1.0 — 2026-08-04
**Added**
* Execute Validation Workflow
* Execute Detail
* Pending / Running / Stop / Retry
* Validation Center
**Improved**
* Dashboard UI
* Execute Dashboard
* Progress Bar

---
### v1.0.2 — 2026-07-31
**Added**
* Login Page

---

### v1.0.1 — 2026-07-30
**Added**
* Traditional Chinese / English UI
**Improved**
* User Interface

---
### v1.0.0 — 2026-07-27

Initial Release.

---
## 🗺 Roadmap / 開發規劃
### v1.3.0
* Execute Logs
* Timeline View
* Advanced Execution History
* Execution Result Analysis

---
### v1.4.0
* Report Center
* PDF Export
* Excel Export
* Validation Report Generation

---
### v2.0.0

Hardware and automation integration:
* SSH Integration
* IPMI Integration
* Smartctl Integration
* StorCLI Integration
* Iometer Integration
* JBOD Hardware Automation
* Automated Validation Workflow

---
## 🧪 Validation Test Examples / 驗證測試範例
Current Execution Engine verification includes:

**PASS Test**
```
Case ID:
ENGINE-PASS

Timeout:
10 seconds

Result:
PASS
```

**TIMEOUT Test**
```
Case ID:
ENGINE-TIMEOUT

Command:
python -c "import time; time.sleep(10)"

Timeout:
3 seconds

Result:
TIMEOUT

Execution Job:
FAIL
```

The Timeout Test verifies that the Execution Engine can terminate a long-running process and correctly record the execution result.

---
## 🔐 Authentication / 使用者驗證

The platform provides an authentication system including:
* Login
* Logout
* User Registration
* Remember Username
* Auto Login
* Password Visibility Toggle
* Enterprise Login UI
Login page:

> /login/

The Login page uses an independent layout and does not display the application Sidebar.

---
## 📌 Current Development Status / 目前開發狀態

Current stable release:

> v1.2.0

**Available**
✅ Dashboard
✅ Model Management
✅ Firmware Management
✅ Test Case Management
✅ Test Plan Management
✅ Validation Center
✅ Execute Validation
✅ Execute Detail
✅ Execution Timeout
✅ Execution Progress
✅ Current TestCase Tracking
✅ Authentication

**Planned**
🚧 Report Center
🚧 Log Center
🚧 Hardware Automation
🚧 SSH Integration
🚧 IPMI Integration
🚧 Smartctl Integration
🚧 StorCLI Integration
🚧 Iometer Integration

---
## 👨‍💻 Author

Shing-Yu Chou (Travis)

GitHub:

https://github.com/shingyu0205

---
## 📄 License

MIT License