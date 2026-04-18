import requests

url = "http://localhost:8000/api/v1/verify"
payload = {
    "text": "Free recharge link sab users ko free data de raha hai",
    "mode": "text",
    "explain_tone": "simple"
}
try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
except Exception as e:
    print("Error:", e)
