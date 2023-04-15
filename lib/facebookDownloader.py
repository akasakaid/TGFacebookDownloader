import os
import re
import json
import time
import urllib
from urllib.parse import unquote
import requests
from dotenv import load_dotenv

load_dotenv()
cookieFacebook = os.environ.get("COOKIE_FACEBOOK")

var_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': cookieFacebook,
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
}


class FacebookDownloader:
    def __init__(self):
        self.ses = requests.Session()

    def getMe(self):
        req = self.ses.get("https://facebook.com/me",
                           allow_redirects=True, headers=var_headers)
        open("hasil_me.html", "w", encoding="utf-8").write(req.text)
        print(req.url)

    def url_verify(self, url: str):
        url_test = requests.get(url, allow_redirects=True, headers=var_headers)
        open("hasil_verify.html", "w", encoding="utf-8").write(url_test.text)
        print(url_test.url)
        unquoteUrl = urllib.parse.unquote(url_test.url)
        if '/login/' in url_test.url:
            nextUrl = re.search('next=(.*)', unquoteUrl).group(1)
            # new_url = url.replace('https://www.facebook.com/login/?next=', '')
            # decode_url = urllib.parse.unquote(new_url)
            # print(decode_url)
            # return decode_url
            # print(nextUrl)
            return nextUrl
        else:
            return url_test.url

    def alpha_version(self, url):
        req = requests.get(url, allow_redirects=True, headers=var_headers)
        if req.status_code != 200:
            req = requests.get(req.url)
        open("hasil.html", "w", encoding="utf-8").write(req.text)
        data_json = re.findall(
            'requireLazy\(\["JSScheduler","ServerJS","ScheduledApplyEach"],function\(JSScheduler,ServerJS,'
            'ScheduledApplyEach\)\{JSScheduler\.runWithPriority\(3,function\(\)\{\(new ServerJS\('
            '\)\)\.handleWithCustomApplyEach\(ScheduledApplyEach,(.*?)\);}\);}\);</script>',
            req.text)
        if len(data_json) == 0:
            # print('- failed download with alpha version !')
            return None
        for data in data_json:
            if 'playable_url' in data:
                # url_dl = None
                data_loads = json.loads(data)
                url_sd = re.search("playable_url': '(.*?)'",
                                   str(data_loads))
                url_hd = re.search("playable_url_quality_hd': '(.*?)'",
                                   str(data_loads))
                if url_sd is None and url_hd is None:
                    return None
                if url_sd is not None:
                    url_dl = url_sd.group(1)
                    note = "SD QUALITY"
                if url_hd is not None:
                    url_dl = url_hd.group(1)
                    note = 'HD QUALITY'
                output_name = "Facebook_" + str(int(time.time())) + ".mp4"
                reqcontent = requests.get(url_dl, stream=True)
                total_size = int(reqcontent.headers.get('content-length', 0))
                block_size = 1024
                t = total_size / block_size
                with open(output_name, 'wb') as f:
                    for data in reqcontent.iter_content(block_size):
                        f.write(data)
                f.close()
                print('- download videos success with ' +
                      note + ' ,save to', output_name)
                return output_name, note

    def beta_version(self, url):
        url_dl = None
        req = requests.get(url, allow_redirects=True, headers=var_headers)
        #        open('hasil.html', 'w').write(req.text)
        open("hasil.html", "w", encoding="utf-8").write(req.text)
        data_json = re.findall(
            '<script type="application/json" data-content-len="(.*?)" data-sjs>(.*?)</script>', req.text)
        if len(data_json) == 0:
            # print('- failed download with beta version')
            return None
        for dat, data in data_json:
            if 'playable_url' in data:
                data_loads = json.loads(data)

                url_sd = re.search("playable_url': '(.*?)'",
                                   str(data_loads))
                url_hd = re.search("playable_url_quality_hd': '(.*?)'",
                                   str(data_loads))
                if url_sd is None and url_hd is None:
                    return None
                if url_sd is not None:
                    url_dl = url_sd.group(1)
                    note = "SD QUALITY"
                if url_hd is not None:
                    url_dl = url_hd.group(1)
                    note = 'HD QUALITY'
                output_name = "Facebook_" + str(int(time.time())) + ".mp4"
                reqcontent = requests.get(url_dl, stream=True)
                total_size = int(reqcontent.headers.get('content-length', 0))
                block_size = 1024
                t = total_size / block_size
                # tq = tqdm(total=total_size, unit='iB', unit_scale=True)
                with open(output_name, 'wb') as f:
                    for data in reqcontent.iter_content(block_size):
                        # tq.update(len(data))
                        # for data in track(reqcontent.iter_content(block_size), total=t, description="Downloading..."):
                        f.write(data)
                # open(output_name, 'wb').write(reqcontent.content)
                # tq.close()
                f.close()
                print('- download videos success with ' +
                      note + ' ,save to', output_name)
                return output_name, note

    def greed(self, url):
        # urlDl = None
        req = requests.get(url, allow_redirects=True, headers=var_headers)
        # print(req.headers)
        open("hasil.html", "w", encoding='utf-8').write(req.text)
        urlSd = re.findall('"playable_url":"(.*?)"', req.text)
        urlHd = re.findall('"playable_url_quality_hd":"(.*?)"', req.text)
        if len(urlSd) == 0 and len(urlHd) == 0:
            return None
        if len(urlSd) != 0:
            urlDl = urlSd[0]
            note = "SD QUALITY"
        if len(urlHd) != 0:
            urlDl = urlHd[0]
            note = "HD QUALITY"
        # print(urlDl)
        urlDl = bytes(urlDl.replace('\\/', '/'),
                      'utf-8').decode('unicode_escape')
        # print(urlDl)
        # exit()
        output_name = "Facebook_" + str(int(time.time())) + ".mp4"
        reqcontent = requests.get(urlDl, stream=True)
        total_size = int(reqcontent.headers.get('content-length', 0))
        block_size = 1024
        t = total_size / block_size
        # tq = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(output_name, 'wb') as f:
            for data in reqcontent.iter_content(block_size):
                # tq.update(len(data))
                # for data in track(reqcontent.iter_content(block_size), total=t, description="Downloading..."):
                f.write(data)
        # open(output_name, 'wb').write(reqcontent.content)
        # tq.close()
        f.close()
        print('- download videos success with ' +
              note + ' ,save to', output_name)
        return output_name, note


# if __name__ == "__main__":
#     dl = FacebookDownloader()
#     veri = dl.url_verify(
#         "https://www.facebook.com/100083755765191/posts/133750996093425/?mibextid=rS40aB7S9Ucbxw6v")
#     x = dl.greed(url=veri)
