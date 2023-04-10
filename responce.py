import datetime
import json
import os
from typing import Any
import pprint

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

### driverを生成
def setting_driver() -> WebDriver:

    caps = DesiredCapabilities.CHROME  # Chromeで要求されるブラウザ設定
    # print(caps)
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    # WebDriverのオプション指定
    options = Options()
    options.add_argument("--ignore-certificate-erroes")  # 証明書エラー回避
    options.add_argument("--incognito")  # シークレットモードの設定付与
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    # chrome_service = fs.Service(executable_path="/usr/local/bin/chromedriver")
    # driver = webdriver.Chrome(service=chrome_service, options=options)
    executable_path=r'G:\マイドライブ\クローリング\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path, options=options)

    driver.implicitly_wait(5)

    return driver

### パフォーマンスログから"message"というプロパティを抽出する
def retrieve_value_by_key_message(performance_log: dict[Any, Any]) -> dict[Any, Any]:
    response: dict[Any, Any] = json.loads(performance_log["message"])["message"]
    return response

### 計測を実施し、データを作成する
def make_evaluation_data_list(driver: WebDriver, number_of_page: int, number_of_input_items: int, evaluation_data_list: list[dict[Any, Any]]) -> list[dict[Any, Any]]:

    current_datatime = datetime.datetime.now().strftime("%m%d_%H%M")
    browser_current_url: str = driver.current_url

    net_log: dict[Any, Any] = driver.get_log("performance")
    # パフォーマンスログから"message"というプロパティを抽出
    events = [retrieve_value_by_key_message(performance_log) for performance_log in net_log]
    # "method"名にNetwork.responseReceived含むものを抽出
    events = [event for event in events if "Network.respons" in event["method"]]

    # 各performanceからタイムスタンプとURLを抽出
    detected_url = []
    timestamp_url = []
    for item in events:
        if "response" in item["params"]:
            if "url" in item["params"]["response"]:
                # 詳細のアクセスURL
                detected_url.append(item["params"]["response"]["url"])
                # timestamp
                timestamp_url.append(item["params"]["timestamp"])

    # 詳細のアクセスURL数
    number_of_detected_url: int = len(detected_url)
    # アクセストータル時間 タイムスタンプの終わり - タイムスタンプの始まり
    loading_time = float(timestamp_url[number_of_detected_url - 1]) - float(timestamp_url[0])
    # 推定入力時間（仮）
    input_time: float = 6 + 12.8 * number_of_input_items

    evaluation_data_dict = {
        "1.測定日時": current_datatime,
        "2.ID": item["params"]["requestId"],
        "3.URL": browser_current_url,
        "4.遷移数": number_of_page + 1,
        "5.読込時間": round(loading_time, 2),
        "6.推定入力時間": input_time,
        "7.合計表示時間": round(loading_time + input_time, 2),
    }
    evaluation_data_list.append(evaluation_data_dict)
    return evaluation_data_list

### 計測する関数を呼び出し、出力する
def conversion_measurement(driver,forms,data_list):
    """
    forms: 遷移するために利用するフォームの数
    data_list: データを格納するリスト
    """
    # ページの読み込みが終わるまで待つ
    WebDriverWait(driver, 15).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    # データを格納するためのリスト作成
    evaluation_data_list: list[dict[Any, Any]] = data_list
    # 計測、データ作成の関数を呼び出す
    evaluation_data_list = make_evaluation_data_list(driver, len(evaluation_data_list), forms,evaluation_data_list)
    # 作成したデータを出力
    pprint.pprint(evaluation_data_list)


# データを格納するリスト
data_list = []

# ドライバー生成
driver = setting_driver()

try:
    # 対象のサイトにアクセス
    driver.get('https://www.amazon.co.jp')

    # 計測
    conversion_measurement(driver,0,data_list)

    # ドライバーを閉じる
    driver.quit()
    
finally:
    driver.quit()


# 参考：https://note.com/shakeshake108/n/nd76dea39d2a0