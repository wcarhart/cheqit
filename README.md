# cheqit
*Check the status of a URL or IP address*

## Usage
```
$ python3 cheqit.py google.com amazon.com
 google.com UP
 amazon.com UP
```
All options: `python3 cheqit.py --help`
```
usage: cheqit.py [-h] [-s] [-d DELAY] url_or_ip [url_or_ip ...]

positional arguments:
  url_or_ip             the URL(s) or IP address(es) for which to check status

optional arguments:
  -h, --help            show this help message and exit
  -s, --stream          if included, status will be streamed to stdout
                        (default: False)
  -d DELAY, --delay DELAY
                        if streaming, the delay between updates, in seconds
                        (minimum is 10) (default: 10)
```
