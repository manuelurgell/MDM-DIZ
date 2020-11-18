import requests


def maybe(url, headers, data, status_code):

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    print(response.status_code)
    # print(response.json())

    if response.status_code == status_code:
        return True
    else:
        return False
