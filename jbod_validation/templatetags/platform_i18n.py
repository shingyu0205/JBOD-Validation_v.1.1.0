from django import template


register = template.Library()


ENGLISH = {
    "企業級驗證管理系統": "Enterprise Validation Management System",
    "Django 管理後台": "Django Administration",
    "登出": "Sign out",
    "驗證管理平台": "Validation Management Platform",
    "總覽": "Overview",
    "儀表板": "Dashboard",
    "資產管理": "Asset Management",
    "機型管理": "Model Management",
    "韌體管理": "Firmware Management",
    "驗證作業": "Validation",
    "驗證中心": "Validation Center",
    "測試案例": "Test Cases",
    "測試計畫": "Test Plans",
    "執行作業": "Execute Jobs",
    "報告與日誌": "Reports & Logs",
    "報告": "Reports",
    "日誌": "Logs",
    "即將推出": "Coming Soon",
    "系統管理": "System",
    "管理後台": "Administration",
    "JBOD 驗證管理平台總覽": "JBOD Validation Platform Overview",
    "機型數": "Models",
    "韌體版本數": "Firmware",
    "測試案例數": "Test Cases",
    "執行中作業": "Running Jobs",
}


@register.simple_tag(takes_context=True)
def pt(context, text):
    """Return the platform UI text in the language selected for this request."""
    request = context.get("request")
    language = getattr(request, "LANGUAGE_CODE", "zh-hant")
    if language.startswith("en"):
        return ENGLISH.get(text, text)
    return text
