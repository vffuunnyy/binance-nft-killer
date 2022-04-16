from typing import List, Dict


class Account:
    csrftoken: str
    p20t: str
    cookies: Dict
    headers: Dict

    def __init__(self, csrftoken, p20t):
        self.csrftoken = csrftoken
        self.p20t = p20t

        self.cookies = {
            'p20t': p20t
        }
        self.headers = {
            'csrftoken' : csrftoken,
            'clienttype': 'web',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
