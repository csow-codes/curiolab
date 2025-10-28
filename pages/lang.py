# lang.py
translations = {
    "English": {
        "Get started": "Get started",
        "Add observation": "Add observation",
        "Download CSV": "Download CSV",
        "Mini Science Report": "Mini Science Report",
        "Copy & share": "Copy & share",
        "Missions": "Missions",
        "Open module →": "Open module →",
        "Air & Weather": "Air & Weather",
        "Seeds & Growth": "Seeds & Growth",
        "Pollinator Patrol": "Pollinator Patrol",
        "Analysis Lab": "Analysis Lab",
    },
    "Español": {
        "Get started": "Empezar",
        "Add observation": "Añadir observación",
        "Download CSV": "Descargar CSV",
        "Mini Science Report": "Informe científico",
        "Copy & share": "Copiar y compartir",
        "Missions": "Misiones",
        "Open module →": "Abrir módulo →",
        "Air & Weather": "Aire y Clima",
        "Seeds & Growth": "Semillas y Crecimiento",
        "Pollinator Patrol": "Patrulla de Polinizadores",
        "Analysis Lab": "Laboratorio de Análisis",
    },
    "简体中文": {
        "Get started": "开始",
        "Add observation": "添加观察",
        "Download CSV": "下载表格",
        "Mini Science Report": "小科学报告",
        "Copy & share": "复制与分享",
        "Missions": "任务",
        "Open module →": "打开模块 →",
        "Air & Weather": "空气与天气",
        "Seeds & Growth": "种子与生长",
        "Pollinator Patrol": "传粉者巡逻",
        "Analysis Lab": "分析实验室",
    }
}

def t(key: str, lang: str = "English") -> str:
    return translations.get(lang, translations["English"]).get(key, key)
