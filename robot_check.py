###クローリング可能かをDisallowで判断

from time import sleep



from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

def is_crawling_allowed(url):
    robots_url = urljoin(url, "/robots.txt")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        req = Request(robots_url, headers=headers)
        response = urlopen(req, timeout=10)  # タイムアウトを設定
        robots_txt = response.read().decode("utf-8")
    except (HTTPError, URLError):
        # robots.txtが存在しない場合、クロールを許可する
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

    user_agent = "*"
    allowed = True
    for line in robots_txt.split("\n"):
        if line.startswith("User-agent:"):
            _, agent = line.split(":", 1)
            agent = agent.strip()
            if agent == user_agent:
                allowed = False
        elif not allowed:
            if line.startswith("Disallow:"):
                _, path = line.split(":", 1)
                path = path.strip()
                if urljoin(url, path) == url:
                    return False
            elif re.match("User-agent: .*", line):
                # 新しいUser-agentが指定された場合、allowedフラグをTrueに戻す
                allowed = True
    return True


urls = {'Amazon':'https://www.amazon.co.jp',
        
        
        
        
        }
for url in urls.values():
    print(url)
    print(is_crawling_allowed(url))
    sleep(1)

