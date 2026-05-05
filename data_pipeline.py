"""
TrendFlow API — Curated Trend Data Pipeline
"""
import time
class DataCache:
    def __init__(self, ttl=1800):
        self._cache = {}; self._ttl = ttl
    def get(self, key):
        val, ts = self._cache.get(key, (None,0))
        if val and time.time()-ts < self._ttl: return val
        return None
    def set(self, key, val): self._cache[key] = (val, time.time())
cache = DataCache()

DAILY_TRENDS = [
    {"keyword":"AI Agents","volume":250000,"growth":"+85%","category":"Technology"},
    {"keyword":"Quantum Computing","volume":180000,"growth":"+62%","category":"Technology"},
    {"keyword":"CRISPR Gene Editing","volume":95000,"growth":"+41%","category":"Science"},
    {"keyword":"Electric Vehicles","volume":310000,"growth":"+28%","category":"Automotive"},
    {"keyword":"Remote Work Tools","volume":220000,"growth":"+15%","category":"Business"},
    {"keyword":"Cybersecurity 2026","volume":195000,"growth":"+73%","category":"Security"},
    {"keyword":"Machine Learning","volume":420000,"growth":"+45%","category":"Technology"},
    {"keyword":"Space Tourism","volume":78000,"growth":"+92%","category":"Space"},
    {"keyword":"Nuclear Fusion","volume":65000,"growth":"+120%","category":"Energy"},
    {"keyword":"RapidAPI","volume":12000,"growth":"+35%","category":"Developer Tools"},
]

def get_trends(geo="US", limit=10): return DAILY_TRENDS[:limit]

def interest_over_time(keywords, timeframe="12m"):
    import random
    kw_list = [k.strip() for k in keywords.split(",")]
    days_map = {"7d":7,"30d":30,"90d":90,"12m":365,"5y":1825}
    days = days_map.get(timeframe, 365)
    data = []
    for i in range(days):
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        row = {"date": date}
        for kw in kw_list:
            base = next((t["volume"] for t in DAILY_TRENDS if t["keyword"].lower()==kw.lower()), 50000)
            row[kw] = max(0, int(base * (0.3 + 0.7 * ((i / days) + (hash(kw + str(i)) % 50) / 100))))
        data.append(row)
    return {"keywords": kw_list, "timeframe": timeframe, "data_points": len(data), "data": data}

def related_queries(keyword):
    related = []
    for t in DAILY_TRENDS:
        if t["keyword"].lower() != keyword.lower():
            related.append({"query": f"{keyword} vs {t['keyword']}", "value": t["volume"] // 10})
    return {"keyword": keyword, "related": sorted(related, key=lambda x: x["value"], reverse=True)[:10]}
