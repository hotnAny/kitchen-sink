import requests

def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download file: HTTP {response.status_code}")

# Example usage
url = "https://www.csauthors.net/xiang--anthony--chen/xiang--anthony--chen.bib"  # Replace with the actual URL
destination = "./xac-csauthors.bib"  # Replace with your desired local filename
download_file(url, destination)