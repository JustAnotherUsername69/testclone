import base64
import cloudscraper
import re
import requests
import html.parser
from abc import ABC
from markdown import markdown

from lxml import etree
from urllib.parse import urlparse, parse_qs

from bot import APPDRIVE_EMAIL, APPDRIVE_PASS, GDTOT_CRYPT, HD_CRYPT, XSRF_TOKEN, laravel_session, K_CRYPT, DRIVEHUB_CRYPT
from bot.helper.ext_utils.exceptionss import ExceptionHandler

account = {
    'email': APPDRIVE_EMAIL,
    'passwd': APPDRIVE_PASS
}

class HTMLTextExtractor(html.parser.HTMLParser, ABC):
    # https://stackoverflow.com/a/7778368/15215201
    def __init__(self):
        super(HTMLTextExtractor, self).__init__()
        self.result = []

    def handle_data(self, d):
        self.result.append(d)

    def get_text(self):
        return ''.join(self.result)

def html2text(html_string):
    s = HTMLTextExtractor()
    s.feed(html_string)
    return s.get_text()

def account_login(client, url, email, password):
    data = {
        'email': email,
        'password': password
    }
    client.post(f'https://{urlparse(url).netloc}/login', data=data)

def gen_payload(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string

def appdrive(url: str) -> str:
    if (APPDRIVE_EMAIL or APPDRIVE_PASS) is None:
        raise ExceptionHandler("APPDRIVE_EMAIL and APPDRIVE_PASS env vars not provided")
    elif "appdrive.in" in url:
        domain = url.split('/')[2]
        url = url.replace(domain, "appdrive.info")
    client = requests.Session()
    client.headers.update({
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })
    account_login(client, url, account['email'], account['passwd'])
    res = client.get(url)
    try:
        key = re.findall(r'"key",\s+"(.*?)"', res.text)[0]
    except IndexError:
        raise ExceptionHandler("Invalid link")
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
    info = {}
    info['error'] = False
    info['link_type'] = 'login'  # direct/login
    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }
    data = {
        'type': 1,
        'key': key,
        'action': 'original'
    }
    if len(ddl_btn):
        info['link_type'] = 'direct'
        data['action'] = 'direct'
    while data['type'] <= 3:
        try:
            response = client.post(url, data=gen_payload(data), headers=headers).json()
            break
        except:
            data['type'] += 1
    if 'url' in response:
        info['gdrive_link'] = response['url']
    elif 'error' in response and response['error']:
        info['error'] = True
        info['message'] = response['message']
    if urlparse(url).netloc == 'driveapp.in' and not info['error']:
        res = client.get(info['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
        info['gdrive_link'] = drive_link
        
    if urlparse(url).netloc == "gdflix.pro" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivesharer.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivebit.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivelinks.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "driveace.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivepro.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
        
    if not info['error']:
        return info
    else:
        raise ExceptionHandler(f"{info['message']}")

def gdtot(url: str) -> str:
    if GDTOT_CRYPT is None:
        raise ExceptionHandler("GDTOT_CRYPT env var not provided")
    elif "new2.gdtot.sbs" not in url:
        domain = url.split('/')[2]
        url = url.replace(domain, "new2.gdtot.sbs")
    client = requests.Session()
    client.cookies.update({'crypt': GDTOT_CRYPT})
    res = client.get(url)
    res = client.get(f"https://new2.gdtot.sbs/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info['error'] = False
    params = parse_qs(urlparse(url).query)
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        info['error'] = True
        if 'msgx' in params:
            info['message'] = params['msgx'][0]
        else:
            info['message'] = 'ERROR: Try in your broswer, mostly file not found or user limit exceeded!'
    else:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        drive_link = f'https://drive.google.com/open?id={decoded_id}'
        info['gdrive_link'] = drive_link
    if not info['error']:
        return info['gdrive_link']
    else:
        raise ExceptionHandler(f"{info['message']}")

def sharer(url: str, forced_login=False) -> str:
    if (XSRF_TOKEN or laravel_session) is None:
        raise ExceptionHandler("XSRF_TOKEN and laravel_session env vars not provided")
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome', allow_brotli=False)
    scraper.cookies.update({
        "XSRF-TOKEN": XSRF_TOKEN,
        "laravel_session": laravel_session
    })
    res = scraper.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
    info = {}
    info['error'] = True
    info['link_type'] = 'login'  # direct/login
    info['forced_login'] = forced_login
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        '_token': token
    }
    if len(ddl_btn):
        info['link_type'] = 'direct'
    if not forced_login:
        data['nl'] = 1
    try: 
        res = scraper.post(url+'/dl', headers=headers, data=data).json()
        if 'message' in res:
            info['error_msg'] = res['message']
    except:
        return info['error_msg']
    if 'url' in res and res['url']:
        info['error'] = False
        info['gdrive_link'] = res['url']
    if len(ddl_btn) and not forced_login and not 'url' in info:
        # retry download via login
        return sharer(url, forced_login=True)
    if not info['error']:
        return info['gdrive_link']
    else:
        raise ExceptionHandler(html2text(f"{info['error_msg']}"))
        
class HubDrive:
    client = requests.Session()

    @staticmethod
    def parse_info(res):
        info_parsed = {}
        title = re.findall('>(.*?)<\/h4>', res.text)[0]
        info_chunks = re.findall('>(.*?)<\/td>', res.text)
        info_parsed['title'] = title
        for i in range(0, len(info_chunks), 2):
            info_parsed[info_chunks[i]] = info_chunks[i + 1]
        return info_parsed

    def hubdrive_dl(self, url: str) -> str:
        if HD_CRYPT is None:
            raise ExceptionHandler("HD_CRYPT env var not provided")
        elif "hubdrive.in" in url or "hubdrive.cc" in url or "hubdrive.pro" in url:
            domain = url.split('/')[2]
            url = url.replace(domain, "hubdrive.me")
        if 'hubdrive' in url:
            self.client.cookies.update({'crypt': HD_CRYPT})
        elif 'drivehub' in url:
            self.client.cookies.update({'crypt': DRIVEHUB_CRYPT})
        elif 'kolop' in url:
            self.client.cookies.update({'crypt': K_CRYPT})
        elif 'katdrive' in url:
            self.client.cookies.update({'crypt': K_CRYPT})
        res = self.client.get(url)
        info_parsed = self.parse_info(res)
        info_parsed['error'] = False
        up = urlparse(url)
        req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
        file_id = url.split('/')[-1]
        data = {'id': file_id}
        headers = {
            'x-requested-with': 'XMLHttpRequest'
        }
        res = self.client.post(req_url, headers=headers, data=data).json()
        if res['code'] == "200":
            res = res['file']
            gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
            return f'https://drive.google.com/open?id={gd_id}'
        else:
            return res['file']
