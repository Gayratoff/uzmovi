import requests

# define the API endpoint URLs
vote_check_url = "https://openbudget.uz/api/v2/vote/check"
captcha_url = "https://openbudget.uz/api/v2/vote/captcha"

# set the request headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://openbudget.uz",
    "Referer": "https://openbudget.uz/boards-list/1/e287920f-01b6-4d18-80fc-8010a786023f",
}

# generate the captcha key using the captcha API
response = requests.get(captcha_url)

# extract the captcha key from the response JSON
captcha_key = response.json()["key"]

# create the request payload
payload = {
    "captchaKey": captcha_key,
    "captchaResult": input("Enter captcha value: "),
    "phoneNumber": "998905611628",
    "boardId": 1
}

# make the POST request
response = requests.post(vote_check_url, headers=headers, json=payload)

# check if the response was successful
if response.ok:
    print(response.json())
else:
    print(response.status_code)
    print(response.content)

# if the response is an error with code 102, generate a new captcha and retry the request
if response.status_code == 400 and response.json()["code"] == 102:
    response = requests.get(captcha_url)
    captcha_key = response.json()["key"]
    payload["captchaKey"] = captcha_key
    response = requests.post(vote_check_url, headers=headers, json=payload)
    if response.ok:
        print(response.json())
    else:
        print(response.status_code)
        print(response.content)