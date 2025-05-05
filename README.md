# ERES Emailer

I tried to figure out how to send emails via the Python API from the
eresorganizers@gmail.com email. Preserving for posterity.


## How to set up

Navigate to
[https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
and click the download button at the right under "OAuth 2.0 Client IDs". Save to
`credentials.json` in the current directory, and you should be able to send
emails using `main.py`

By default, `main.py` is configured to read `test.csv` (included in the git
repository; sends emails from eresorganizers@gmail.com to itself), so you should
immediately be able to verify whether you're properly authenticated.
