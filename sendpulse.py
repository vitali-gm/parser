
import requests
import csv
import time


def get_emails(url, headers):
    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('sleep time')
        time.sleep(10)
        return get_emails(url, headers)

CLIENT_ID = '09e35c1502b8e5ecc2e703ed0e4855be'
CLIENT_SECRET = '76c8fbfa7301d1f4016ec1c025f2fabb'

AUTH_URL = 'https://api.sendpulse.com/oauth/access_token'
URL = 'https://api.sendpulse.com/addressbooks'

data_auth = {
    'grant_type' : 'client_credentials',
    'client_id' : CLIENT_ID,
    'client_secret' : CLIENT_SECRET
}


response_auth = requests.post(AUTH_URL, data=data_auth)

if response_auth.status_code == 200:
    res_token = response_auth.json()
    access_token = res_token['access_token']
    
    headers = {"Authorization": "Bearer " + access_token}

    limit = 100
    count_all = 0
    count = 0
    users = []

    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        with open('users.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['email', 'phone', 'status'])
            for book in response.json():
                offset = 0
                while True:
                    print(offset, count_all, count)
                    req_url = 'https://api.sendpulse.com/addressbooks/' + str(book['id']) + '/emails?limit=' + str(limit) + '&offset=' + str(offset)
                    res = get_emails(req_url, headers)
                    if res.status_code == 200:
                        list_users = res.json()
                        for item in list_users:
                            # email = item['email'].lower()
                            email = item['email']
                            phone = item['phone']
                            status = item['status']
                            if not email in users:
                                writer.writerow([email, phone, status])
                                users.append(email)
                                count += 1
                        
                        offset += limit
                        count_all += limit
                        if len(list_users) < limit:
                            break
            
        