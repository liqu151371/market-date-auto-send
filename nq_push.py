import requests
import json
import time

# ============ 这里保留你自己的参数，不要修改 ============
APP_TOKEN = "AT_tAibTSKNPJosjamqfQRIhYm8a8bBYhNH"
MY_UID = "UID_ml60XI7TuN1TykIpRHqrlJp9XkN6"
# ======================================================

# 强化请求头，避免被服务器拦截
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept": "application/json,text/plain,*/*"
}

# 单次接口重试2次，延长超时时间
def fetch_data(symbol, retry=2, timeout=15):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    for i in range(retry + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            if i < retry:
                time.sleep(1)
                continue
            return None

def get_all_market_data():
    symbol_list = [
        ("NQ=F", "纳指100期货"),
        ("DX=F", "美元指数期货"),
        ("CL=F", "WTI原油期货"),
        ("^VIX", "VIX恐慌指数")
    ]
    msg_lines = ["【每日14:00 全球核心品种行情】接收人：zhaojincong"]

    for sym, name in symbol_list:
        data = fetch_data(sym)
        if not data:
            msg_lines.append(f"❌ {name} 行情获取超时失败")
            continue
        try:
            meta = data["chart"]["result"][0]["meta"]
            price = round(meta["regularMarketPrice"], 2)
            change = round(meta["regularMarketChange"], 2)
            pct = round(meta["regularMarketChangePercent"], 2)
            flag = "📈" if change >= 0 else "📉"
            line = f"{flag} {name}\n现价：{price} | 涨跌：{change} | 涨跌幅：{pct}%"
            msg_lines.append(line)
        except Exception:
            msg_lines.append(f"❌ {name} 数据解析失败")

    msg_lines.append("\n数据来源：Yahoo Finance（延时行情）")
    return "\n".join(msg_lines)

# WxPusher推送函数
def send_wechat(text):
    api_url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": APP_TOKEN,
        "content": text,
        "contentType": 1,
        "uids": [MY_UID]
    }
    requests.post(api_url, json=payload, timeout=10)

if __name__ == "__main__":
    content = get_all_market_data()
    send_wechat(content)