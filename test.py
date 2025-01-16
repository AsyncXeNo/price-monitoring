import requests


send_mail_webhook_url = 'https://hook.eu2.make.com/hu657hxcakj94aedv4qjjjl9tblv602u'

file_paths = ['data/output.xlsx', 'logs/script.log']

files = [("files", (file, open(file, "rb"))) for file in file_paths]


data = {
    "sender": "dev.kartikaggarwal117@gmail.com",
    "recipients": ",".join(["dev.kartikaggarwal117@gmail.com", "kartik.aggarwal117@gmail.com"]),
    "subject": "Testing if this works",
    "message": "Hello, this is a test email sent via Make.com webhook!",
}

response = requests.post(send_mail_webhook_url, data=data, files=files)

print("Response Status Code:", response.status_code)
print("Response Text:", response.text)