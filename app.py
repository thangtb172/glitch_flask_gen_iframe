from flask import Flask, render_template,request,url_for, jsonify
from datetime import datetime
import json
app = Flask(__name__)


import time
import requests
import json

domain =  "http://139.180.152.4"

def get_acc():
    url = domain + "/get-acc"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['message']

def add_iframe(link):
    try:
        url = domain + "/add-iframe"

        payload = json.dumps({
        "iframe": link
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        return False
    return True



def get_iframe_helper(cookies,ua):
    cookie_dict= {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
        
    url = "https://openapi.lenovo.com/us/en/v1/payment/getIframAddress?walletId="

    payload={}
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://account.lenovo.com',
        'referer': 'https://account.lenovo.com/us/en/account/wallet/create.html',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua
        # 'user-agent': random.choice(ua_android)
    }
    count_error = 0
    print('run get iframe')
    count_success = 0
    for i in range(5):
        try:
            if count_error == 2:
                break
            response = requests.request("GET", url, headers=headers, data=payload, cookies=cookie_dict, timeout=8)
            link = response.json()['data']['data']['iframeUrl']
            add_iframe(link)
            print('add new iframe successfully', i + 1)
            time.sleep(1)
            count_error = 0
            count_success += 1
        except Exception as e:
            print(e)
            break
    return count_success


@app.route("/")
def index():
	return render_template("index.html", now=datetime.now())


@app.route("/api/get-iframe", methods=["POST"])
def get_iframe():
    cookies  = json.loads(request.form.get("cookies"))
    ua = request.form.get("ua")
    result = get_iframe_helper(cookies=cookies, ua=ua)
    return jsonify({"status": "OK", "result": result})
  

if __name__ == "__main__":
	app.run()