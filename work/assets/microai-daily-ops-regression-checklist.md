# microai Daily Operations Regression Checklist

> Status: published  
> Last updated: 2026-03-15  
> Scope: Signal -> Mission -> Build -> Quality -> Release -> Feedback loop

## 1) Daily Regression Checklist

|Stage|Check Item|Method|Pass Criteria|
|---|---|---|---|
|0. Runtime|Local app service responds|HTTP check `http://localhost:8080/index.html`|HTTP 200|
|1. Company baseline|`microai` identity + mission fields exist|Inspect `CONFIG.yaml`|name/mission/north_star present|
|2. Signal integrity|Placeholder governance is clean|`python scripts/check_placeholders.py`|No placeholder violations|
|3. Mission/config integrity|Config and schemas valid|`python scripts/validate_schema.py`|Schema validation passed|
|4. Queue health|No pending blocked work|`python scripts/find_pending_work.py`|`HEARTBEAT_OK`|
|5. Governance hooks|Governance check runs|`python scripts/check_github_governance.py`|Script exits successfully|
|6. UI baseline|Chinese homepage + nav present|Browser automation on `index.html`|title/nav checks pass|
|7. Mission progression|Demo workflow moves step-by-step|Click `#wfNext` and verify active step|Active step updates|
|8. Operability controls|Pause/resume controls work|Toggle `#wfPlay`|state switches pause/run|
|9. Release visibility|Visualization embed is available|Read embedded iframe title|Contains `microai`|
|10. Feedback loop|Visualization scenario can switch and continue|Switch to `Template That Improves Itself` and step forward|Scenario selected + phase advances|
|11. Terminal observability|Activity log panel visible|Read `.term-title` on visualization page|Shows `代理活动日志`|
|12. Browser health|No frontend console errors|Browser console scan|0 error messages|

## 2) Auto Regression Run Record

### Run Metadata

- Run time: `2026-03-15 00:50:50`
- Environment: local Windows + Python + Playwright browser automation
- Target company: `microai`

### Script-Based Checks

|Check|Result|Evidence|
|---|---|---|
|Runtime endpoint|PASS|`http://localhost:8080/index.html` returned `200`|
|Placeholder integrity|PASS|`Checked 242 markdown file(s): no placeholder violations found.`|
|Schema validation|PASS|`Schema validation passed (9 artifact(s) checked).`|
|Pending work|PASS|`Nothing pending. HEARTBEAT_OK.`|
|Governance advisory|PASS|Script exited successfully (local advisory warning only)|

### UI Regression (Automated)

|Check|Result|Evidence|
|---|---|---|
|Homepage title|PASS|`microai 无人公司操作系统 — 全自动在线盈利`|
|Chinese navigation|PASS|问题, 管理层, 流程, 落地, 合规, ▶ 演示|
|Workflow step advance|PASS|Active step label changed (example: `执行`)|
|Workflow pause/resume|PASS|`已暂停` -> `运行中`|
|Visualization iframe|PASS|`microai 实时可视化`|
|Visualization page title|PASS|`microai — 动态概念可视化`|
|Scenario switch|PASS|Switched to `✦ Template That Improves Itself`|
|Feedback phase progression|PASS|Terminal header advanced to `阶段 2`|
|Visualization play toggle|PASS|`暂停` -> `播放` -> `暂停`|
|Activity log panel|PASS|`代理活动日志` visible|
|Browser console errors|PASS|`0` errors|

## 3) Summary

- Overall result: **PASS**
- Passed checks: **12 / 12**
- Blockers: **0**
- Recommendation: use this checklist as the standard daily smoke + governance regression before mission rollout or release decisions.
