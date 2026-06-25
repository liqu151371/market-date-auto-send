import requests
import re

# ========== 只填你自己这两个参数 ==========
APP_TOKEN = "AT_tAibTSKNPJosjamqfQRIhYm8a8bBYhNH"
MY_UID = "UID_ml60XI7TuN1TykIpRHqrlJp9XkN6"
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_tv_data(symbol):
    url = f"https://www.tradingview.com/symbols/{symbol}/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        html = resp.text
        price_match = re.search(r'"price":"([\d\.]+)"', html)
        diff_match = re.search(r'"change":"([\d\.\-]+)"', html)
        pct_match = re.search(r'"changePercent":"([\d\.\-]+)"', html)
        if price_match and diff_match and pct_match:
            return float(price_match.group(1)), float(diff_match.group(1)), float(pct_match.group(1))
        return None
    except Exception:
        return None

def generate_msg():
    msg_lines = ["【每日14:00 全球核心品种行情】接收人：zhaojincong"]
    tv_map = [
        ("CME-NQ", "纳指100期货"),
        ("ICE-DX", "美元指数期货"),
        ("NYMEX-CL", "WTI原油期货"),
        ("CBOE-VIX", "VIX恐慌指数")
    ]
    for code, name in tv_map:
        data = get_tv_data(code)
        if data:
            price, chg, pct = data
            flag = "📈" if chg >= 0 else "📉"
            msg_lines.append(f"{flag} {name}\n现价：{price} | 涨跌：{chg} | 涨跌幅：{pct}%")
        else:
            msg_lines.append(f"❌ {name} 行情获取失败")
    msg_lines.append("\n数据来源：TradingView 公开延时行情")
    return "\n".join(msg_lines)

def push_wx(content):
    payload = {
        "appToken": APP_TOKEN,
        "content": content,
        "contentType": 1,
        "uids": [MY_UID]
    }
    requests.post("https://wxpusher.zjiecode.com/api/send/message", json=payload)

if __name__ == "__main__":
    text = generate_msg()
    push_wx(text)