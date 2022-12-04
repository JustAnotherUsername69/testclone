import re
import time
import requests
import cloudscraper
import base64
import json
from base64 import b64decode
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup
from threading import Thread, Event
from bot import *
from bot.helper.ext_utils.bot_utilss import new_thread
from bot.helper.ext_utils.exceptionss import ExceptionHandler
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    key = ''.join(key)
    decrypted = b64decode(key)[16:-16]
    return decrypted.decode('utf-8')
    
def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer
    
ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'    



def mdis_k(urlx):
    scraper = cloudscraper.create_scraper(interpreter="nodejs", allow_brotli=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"http://x.egraph.workers.dev/?param={urlx}"
    response = scraper.get(apix, headers=headers)
    query = response.json()
    return query

def mdisk_ddl(url: str) -> str:
    """ MDisk DDL link generator
    By https://github.com/dishapatel010 """

    check = re.findall(r"\bhttps?://.*mdisk\S+", url)
    if not check:
        textx = f"Invalid mdisk url"
        return textx
    else:
        try:
            fxl = url.split("/")
            urlx = fxl[-1]
            uhh = mdis_k(urlx)
            direct_dl_link = f'{uhh["download"]}'
            file_name = f'{uhh["filename"]}'
            if file_name:
                return direct_dl_link, file_name
            else:
                return direct_dl_link
        except ValueError:
            raise DirectDownloadLinkException("The content is deleted.")


def gplink(url):
    check = re.findall(r"\bhttps?://.*gplink\S+", url)
    if not check:
        textx = f"Invalid GPLinks url"
        return textx
    else:
        client = cloudscraper.create_scraper(allow_brotli=False)
        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        res = client.head(url)
        header_loc = res.headers['location']
        param = header_loc.split('postid=')[-1]
        req_url = f'{p.scheme}://{p.netloc}/{param}'
        p = urlparse(header_loc)
        ref_url = f'{p.scheme}://{p.netloc}/'
        h = { 'referer': ref_url }
        res = client.get(req_url, headers=h, allow_redirects=False)
        bs4 = BeautifulSoup(res.content, 'html.parser')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }
        h = {
            'referer': ref_url,
            'x-requested-with': 'XMLHttpRequest',
        }
        Event().wait(10)
        res = client.post(final_url, headers=h, data=data)
        try:
            return res.json()['url'].replace('\/','/')
        except: return 'Something went wrong :('


def droplink(url):
    check = re.findall(r"\bhttps?://.*droplink\S+", url)
    if not check:
        textx = f"Invalid DropLinks url"
        return textx
    else:
        client = requests.Session()
        res = client.get(url)
        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
        h = {'referer': ref}
        res = client.get(url, headers=h)
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = {input.get('name'): input.get('value') for input in inputs}
        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
        }
        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()['url']
        return res

def linkvertise(url):
    client = requests.Session()
    headers = {
        "User-Agent": "AppleTV6,2/11.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    client.headers.update(headers)
    url = url.replace("%3D", " ").replace("&o=sharing", "").replace("?o=sharing", "").replace("dynamic?r=", "dynamic/?r=")
    id_name = re.search(r"\/\d+\/[^\/]+", url)
    if not id_name: return None
    paths = [
        "/captcha", 
        "/countdown_impression?trafficOrigin=network", 
        "/todo_impression?mobile=true&trafficOrigin=network"
    ]
    for path in paths:
        url = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}{path}"
        response = client.get(url).json()
        if response["success"]: break
    
    data = client.get(f"https://publisher.linkvertise.com/api/v1/redirect/link/static{id_name[0]}").json()

    out = {
        'timestamp':int(str(time.time_ns())[0:13]),
        'random':"6548307", 
        'link_id':data["data"]["link"]["id"]
    }
    options = {
        'serial': base64.b64encode(json.dumps(out).encode()).decode()
    }
    data = client.get("https://publisher.linkvertise.com/api/v1/account").json()
    user_token = data["user_token"] if "user_token" in data.keys() else None
    url_submit = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}/target?X-Linkvertise-UT={user_token}"
    data = client.post(url_submit, json=options).json()
    return data["data"]["target"]        


def adfly(url):
    res = requests.get(url).text
    out = {'error': False, 'src_url': url}
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    return out['bypassed_url']
    
    
def sirigan(url):    
    check = re.findall(r"\bhttps?://.*sirigan\S+", url)
    if not check:
        textx = f"Invalid Sirigan url"
        return textx
    else:
        client = requests.Session()
        res = client.get(url)
        url = res.url.split('=', maxsplit=1)[-1]
        while True:
            try: url = b64decode(url).decode('utf-8')
            except: break
        return url.split('url=')[-1]
        

def ouo(url):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"
    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
    return (res.headers.get('Location'))
    
    
def shorte(url):
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    res = client.get(url)
    sess_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5) # !important
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace('\/','/')
    return (dest_url)

def try2link(url):
    client = requests.Session()
    h = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    res = client.get(url, cookies={}, headers=h)
    
#    url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
    
    res = client.head(url)
    
    id = re.findall('d=(.*?)&', res.headers['location'])[0]
    id = base64.b64decode(id).decode('utf-8')
    
    url += f'/?d={id}'
    res = client.get(url)
    
    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }
    
    time.sleep(6.5)
    res = client.post(
        'https://try2link.com/links/go',
        headers={
            'referer': url,
            'x-requested-with': 'XMLHttpRequest',
        }, data=data
    )
    out = res.json()['url'].replace('\/','/')

    return out

def rocklinks_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("
    
       
def bypasslink(update, context):
  
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
    else:
        link = ''   
    
    if 'try2link' in link:
       is_try2link = True
    else:
       is_try2link = False

    if 'rocklink' in link:
       is_rocklink = True
    else:
       is_rocklink = False

    if 'gplink' in link:
       is_gplink = True
    else:
       is_gplink = False
       
    if 'droplink' in link:
       is_droplink = True
    else:
       is_droplink = False
       
    if "linkvertise" in link or "link-to.net" in link or "direct-link.net" in link or "up-to-down.net" in link or "filemedia.net" in link or "file-link.net" in link or "link-hub.net" in link or "link-center.net" in link or "link-target.net" in link:
       is_linkvertise = True
    else:
       is_linkvertise = False
       
    if "adf.ly" in link or "clickyfly" in link or "gyanilinks" in link:
       is_adfly = True
    else:
       is_adfly = False
       
    if 'sirigan.my.id' in link:
       is_sirigan = True
    else:
       is_sirigan = False
       
    if "ouo.io" in link or "ouo.press" in link:
       is_ouo = True  
    else:
       is_ouo = False
       
    if 'shorte.st' in link:
       is_shorte = True
    else:
       is_shorte = False

    if 'mdisk.me' in link:
       is_mdisk = True
    else:
       is_mdisk = False
        
        
    if is_gplink:
        try:
            msg = sendMessage(f"Processing GP link...\n<code>{link}</code>", context.bot, update.message)
            link = gplink(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)

    elif is_mdisk:
        try:
            msg = sendMessage(f"Processing Mdisk Link...\n<code>{link}</code>", context.bot, update.message)
            link = mdisk_ddl(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
            
    elif is_droplink:
        try:
            msg = sendMessage(f"Processing Droplink...\n<code>{link}</code>", context.bot, update.message)
            link = droplink(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)

    elif is_try2link:
        try:
            msg = sendMessage(f"Processing Try2link...\n<code>{link}</code>", context.bot, update.message)
            link = try2link(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
            
    elif is_linkvertise:
        try:
            msg = sendMessage(f"Processing Linkvertise Link...\n<code>{link}</code>", context.bot, update.message)
            link = linkvertise(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
            
    elif is_adfly:
        try:
            msg = sendMessage(f"Processing Adfly Link...\n<code>{link}</code>", context.bot, update.message)
            link = adfly(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
            
    elif is_sirigan:
        try:
            msg = sendMessage(f"Processing Sirigan Link...\n<code>{link}</code>", context.bot, update.message)
            link = sirigan(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
            
    elif is_ouo:
        try:
            msg = sendMessage(f"Processing OUO Link...\n<code>{link}</code>", context.bot, update.message)
            link = ouo(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message) 
            
    elif is_shorte:
        try:
            msg = sendMessage(f"Processing Shorte Link...\n<code>{link}</code>", context.bot, update.message)
            link = shorte(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message) 

    elif is_rocklink:
        try:
            msg = sendMessage(f"Processing Rocklink link...\n<code>{link}</code>", context.bot, update.message)
            link = rocklinks_bypass(link)
            deleteMessage(context.bot, msg)
            sendMessage(f"Bypassed Link -\n{link}", context.bot, update.message)
        except ExceptionHandler as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
 

    else:
        sendMessage(f"Send GP Link or <code>sirigan.my.id</code> Link or Droplink Link or ouo Link or Try2link Link or Rocklink Link or Mdisk Link to be bypassed along with Command", context.bot, update.message)   
            
            
bypass_handler = CommandHandler(BotCommands.BypassCommand, bypasslink, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(bypass_handler)
