import requests
import time
import random

# Cấu hình Telegram
TELEGRAM_TOKEN = "7867549488:AAFIKFCXa1oVeJDG6pqWoauizyfnBiCE4E4"
CHAT_ID = "6476532822"

# Tải proxy từ các nguồn (dùng file proxy_sources.txt)
def load_sources(file_path="proxy_sources.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Kiểm tra proxy sống hay chết
def is_proxy_alive(proxy, timeout=5):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
        return r.status_code == 200
    except:
        return False

# Lấy proxy từ 1 URL nguồn
def fetch_proxies_from_url(url):
    try:
        r = requests.get(url, timeout=10)
        return [line.strip() for line in r.text.splitlines() if line.strip()]
    except:
        return []

# Gửi tin nhắn lên Telegram
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot7867549488:AAFIKFCXa1oVeJDG6pqWoauizyfnBiCE4E4/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("Lỗi gửi Telegram:", r.text)
    except Exception as e:
        print("Exception gửi Telegram:", e)

# Chạy tool
def main():
    print("🔍 Đang tải nguồn proxy...")
    sources = load_sources()
    proxies = []
    for url in sources:
        proxies.extend(fetch_proxies_from_url(url))
        time.sleep(random.uniform(0.3, 1))  # tránh spam request

    print(f"📥 Tổng proxy lấy được: {len(proxies)}")

    print("✅ Đang lọc proxy sống...")
    live_proxies = []
    for p in proxies:
        if is_proxy_alive(p):
            live_proxies.append(p)
            print("LIVE:", p)
            if len(live_proxies) % 10 == 0:
                send_to_telegram("\n".join(live_proxies[-10:]))
        else:
            print("DIE:", p)

    with open("live_proxies.txt", "w") as f:
        f.write("\n".join(live_proxies))

    send_to_telegram(f"🎉 Đã lọc xong! Tổng proxy sống: {len(live_proxies)}")
    print("🔥 Gửi về Telegram thành công.")
import requests

# 🔧 Thay thế bằng token và ID chat của bạn
TOKEN = '7867549488:AAFIKFCXa1oVeJDG6pqWoauizyfnBiCE4E4'
CHAT_ID = '6476532822'

def send_file_to_telegram(filename, caption=None):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    with open(filename, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': CHAT_ID, 'caption': caption or filename}
        r = requests.post(url, files=files, data=data)
        print(f'📦 Sent {filename}, status: {r.status_code}')

# 🧾 Gửi các file proxy nếu tồn tại
for file_name in ['proxy_http.txt', 'proxy_socks4.txt', 'proxy_socks5.txt']:
    try:
        send_file_to_telegram(file_name, caption=f'🔌 Proxy list: {file_name}')
    except Exception as e:
        print(f'❌ Error sending {file_name}: {e}')

if __name__ == "__main__":
    main()
