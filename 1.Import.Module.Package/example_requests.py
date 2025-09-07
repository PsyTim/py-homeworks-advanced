import requests

def check_website():
    try:
        response = requests.get('https://httpbin.org/get')
        print(f"Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    check_website()
