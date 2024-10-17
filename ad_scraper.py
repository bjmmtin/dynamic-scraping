import requests
from bs4 import BeautifulSoup
import json

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def fetch_facebook_ads(q):
    # URL with q as a variable
    url = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&media_type=all&q={q}&search_type=keyword_unordered'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-TW;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'dpr': '2',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.101", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"15.0.1"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'viewport-width': '547'
    }

    # Step 1: Send the GET request to the URL
    response = requests.get(url, headers=headers)

    # Step 2: Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find all <script> tags with type="application/json"
    script_tags = soup.find_all('script', {'type': 'application/json'})

    # Step 4: Loop through and find the script containing the string "ad_library_main"
    target_script = None
    for script in script_tags:
        if script.string and "ad_library_main" in script.string:
            target_script = script.string
            break

    # Step 5: If found, extract and return the JSON content
    if target_script:
        data = json.loads(target_script)
        try:
            ads = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["ad_library_main"]["search_results_connection"]["edges"]
            return ads
        except:
            print("No ads were found.")
            return []
    else:
        print("No script tag containing 'ad_library_main' was found.")
        return []

# Example usage:
q_value = "Captions: For Talking Videos"
ads_data = fetch_facebook_ads(q_value)

# Save ads_data to a JSON file
save_to_json(ads_data, 'ads_data.json')
# print(ads_data[0])