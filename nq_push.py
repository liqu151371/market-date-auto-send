import requests
import json

# ==================== 仅修改此处两个参数 ====================
APP_TOKEN = "AT_tAibTSKNPJosjamqfQRIhYm8a8bBYhNH"
MY_UID = "UID_ml60XI7TuN1TykIpRHqrlJp9XkN6"  # 微信号zhaojincong扫码后生成的UID
# ==========================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def get_all_market_data():
    # 需要获取的全部品种
    symbol_list = [
        ("NQ=F", "纳指100期货"),
        ("DX=F", "美元指数期货"),
        ("CL=F", "WTI原油期货"),
        ("^VIX", "VIX恐慌指数")
    ]
    msg_lines = ["【每日14:00 全球核心品种行情】接收人：zhaojincong"]

    for sym, name in symbol_list:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            data = resp.json()
            meta = data["chart"]["result"][0]["meta"]

            price = round(meta["regularMarketPrice"], 2)
            change = round(meta["regularMarketChange"], 2)
            pct = round(meta["regularMarketChangePercent"], 2)

            flag = "📈" if change >= 0 else "📉"
            line = f"{flag} {name}\n现价：{price} | 涨跌：{change} | 涨跌幅：{pct}%"
            msg_lines.append(line)
        except Exception:
            msg_lines.append(f"❌ {name} 行情获取超时失败")

    msg_lines.append("\n数据来源：Yahoo Finance（延时行情）")
    return "\n".join(msg_lines)

# 推送至绑定微信号zhaojincong的微信
def send_wechat(text):
    api_url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": APP_TOKEN,
        "content": text,
        "contentType": 1,
        "uids": [MY_UID]
    }
    res = requests.post(api_url, json=payload)
    print("推送返回日志：", res.text)

if __name__ == "__main__":
    content = get_all_market_data()
    send_wechat(content)