import requests
from urllib.parse import urlparse, urljoin


def is_vulnerable(url, payload):
    try:
        # Parse the URL and construct the full URL with the payload
        parsed_url = urlparse(url)
        target_url = urljoin(url, payload)

        # Send the GET request with the payload
        response = requests.get(target_url)

        # Check if the response contains a database error message
        if (
            "SQL" in response.text
            or "mysql" in response.text.lower()
            or "error" in response.text.lower()
        ):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    url = input("Enter the website URL: ")
    payload = "/index.php?id=1%27"  # Simple SQL injection payload

    if is_vulnerable(url, payload):
        print(f"{url} is vulnerable to SQL injection!")
    else:
        print(f"{url} does not appear to be vulnerable to SQL injection.")


if __name__ == "__main__":
    main()
