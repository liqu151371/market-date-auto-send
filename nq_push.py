import requests
import re

# ========== 只填你自己这两个参数 ==========
APP_TOKEN = "AT_tAibTSKNPJosjamqfQRIhYm8a8bBYhNH"
MY_UID = "UID_ml60XI7TuN1TykIpRHqrlJp9XkN6"
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
}

# 抓取单条行情数据
def get_price(url, price_reg, change_reg, pct_reg):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        text = resp.text
        price = re.search(price_reg, text).group(1)
        change = re.search(change_reg, text).group(1)
        pct = re.search(pct_reg, text).group(1)
        return float(price), float(change), float(pct)
    except:
        return None

def collect_all_data():
    msg = ["【每日14:00 全球核心品种行情】接收人：zhaojincong"]

    # 纳指100期货
    nq = get_price(
        "https://finance.sina.com.cn/futures/quotes/NQ.shtml",
        r'"price":"([\d\.]+)"',
        r'"diff":"([\d\.\-]+)"',
        r'"chg":"([\d\.\-]+)"'
    )
    if nq:
        flag = "📈" if nq[1] >= 0 else "📉"
        msg.append(f"{flag} 纳指100期货\n现价：{nq[0]} | 涨跌：{nq[1]} | 涨跌幅：{nq[2]}%")
    else:
        msg.append("❌ 纳指100期货 获取失败")

    # 美元指数
    dx = get_price(
        "https://finance.sina.com.cn/futures/quotes/DX.shtml",
        r'"price":"([\d\.]+)"',
        r'"diff":"([\d\.\-]+)"',
        r'"chg":"([\d\.\-]+)"'
    )
    if dx:
        flag = "📈" if dx[1] >= 0 else "📉"
        msg.append(f"{flag} 美元指数期货\n现价：{dx[0]} | 涨跌：{dx[1]} | 涨跌幅：{dx[2]}%")
    else:
        msg.append("❌ 美元指数期货 获取失败")

    # WTI原油
    cl = get_price(
        "https://finance.sina.com.cn/futures/quotes/CL.shtml",
        r'"price":"([\d\.]+)"',
        r'"diff":"([\d\.\-]+)"',
        r'"chg":"([\d\.\-]+)"'
    )
    if cl:
        flag = "📈" if cl[1] >= 0 else "📉"
        msg.append(f"{flag} WTI原油期货\n现价：{cl[0]} | 涨跌：{cl[1]} | 涨跌幅：{cl[2]}%")
    else:
        msg.append("❌ WTI原油期货 获取失败")

    # VIX恐慌指数
    vix = get_price(
        "https://finance.sina.com.cn/stock/usstock/c/VIX.shtml",
        r'"price":"([\d\.]+)"',
        r'"diff":"([\d\.\-]+)"',
        r'"chg":"([\d\.\-]+)"'
    )
    if vix:
        flag = "📈" if vix[1] >= 0 else "📉"
        msg.append(f"{flag} VIX恐慌指数\n现价：{vix[0]} | 涨跌：{vix[1]} | 涨跌幅：{vix[2]}%")
    else:
        msg.append("❌ VIX恐慌指数 获取失败")

    msg.append("\n数据来源：新浪财经公开行情")
    return "\n".join(msg)

# 微信推送
def send_wechat(content):
    payload = {
        "appToken": APP_TOKEN,
        "content": content,
        "contentType": 1,
        "uids": [MY_UID]
    }
    requests.post("https://wxpusher.zjiecode.com/api/send/message", json=payload, timeout=10)

if __name__ == "__main__":
    text = collect_all_data()
    send_wechat(text)