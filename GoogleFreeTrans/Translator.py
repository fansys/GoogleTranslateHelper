import requests, execjs, json, sys
from GoogleFreeTrans.CalcTk import CalcTk
import time


class translator():
    headers = {
        'Host': 'translate.google.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': 'https://translate.google.cn/',
        'Cookie': 'NID=202=QY45ceUIMWfMf8dAxT6WD7aeH76jMrpjahesinTLEXAdUFTm8GeOMKl231EM3DukliIjhKH0sJBcxqJQ-mJrlLSc-YY7jZCwQDsoUI646Va0MF3HIqXGfVReXPYffFLmMSV94bZ6L2MTbtYLYz_8il2KGh4dgbxVabkFZRvn-pk; _ga=GA1.3.1462915422.1587184666; _gid=GA1.3.840180348.1587184666; 1P_JAR=2020-4-18-4',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    support_lauguage = {'afrikaans': 'af',
                        'arabic': 'ar',
                        'belarusian': 'be',
                        'bulgarian': 'bg',
                        'catalan': 'ca',
                        'czech': 'cs',
                        'welsh': 'cy',
                        'danish': 'da',
                        'german': 'de',
                        'greek': 'el',
                        'english': 'en',
                        'esperanto': 'eo',
                        'spanish': 'es',
                        'estonian': 'et',
                        'persian': 'fa',
                        'finnish': 'fi',
                        'french': 'fr',
                        'irish': 'ga',
                        'galician': 'gl',
                        'hindi': 'hi',
                        'croatian': 'hr',
                        'hungarian': 'hu',
                        'indonesian': 'id',
                        'icelandic': 'is',
                        'italian': 'it',
                        'hebrew': 'iw',
                        'japanese': 'ja',
                        'korean': 'ko',
                        'latin': 'la',
                        'lithuanian': 'lt',
                        'latvian': 'lv',
                        'macedonian': 'mk',
                        'malay': 'ms',
                        'maltese': 'mt',
                        'dutch': 'nl',
                        'norwegian': 'no',
                        'polish': 'pl',
                        'portuguese': 'pt',
                        'romanian': 'ro',
                        'russian': 'ru',
                        'slovak': 'sk',
                        'slovenian': 'sl',
                        'albanian': 'sq',
                        'serbian': 'sr',
                        'swedish': 'sv',
                        'swahili': 'sw',
                        'thai': 'th',
                        'filipino': 'tl',
                        'turkish': 'tr',
                        'ukrainian': 'uk',
                        'vietnamese': 'vi',
                        'yiddish': 'yi',
                        'chinese_simplified': 'zh-CN',
                        'chinese_traditional': 'zh-TW',
                        'auto': 'auto'}

    def __init__(self, src='en', dest='fr', updata_time=600):
        if src not in self.support_lauguage and src not in self.support_lauguage.values():
            raise ValueError('source language not support')
        if dest not in self.support_lauguage and dest not in self.support_lauguage.values():
            raise ValueError('destination language not support')
        self.url = 'https://translate.google.cn/translate_a/single'
        self.params = {
            'client': 'webapp',
            'sl': src,
            'tl': dest,
            'hl': 'zh-CN',
            'dt': 'at', 'dt': 'bd',
            'dt': 'ex', 'dt': 'ld', 'dt': 'md',
            'dt': 'qca', 'dt': 'rw', 'dt': 'rm', 'dt': 'sos', 'dt': 'ss', 'dt': 't',
            'ssel': '0', 'tsel': '3', 'kc': '1', 'tk': '376032.257956'
        }
        self.updata_time = updata_time
        self.__updata_tk()

    def translate(self, text, multi=False):
        if time.time() > self.__next_up_time:
            self.__updata_tk()
        data = {'q': text}
        self.params['tk'] = self.__TK.get_tk(text)
        res = self.__get_res(data)
        ret_list = json.loads(res.text)
        if multi:
            return ret_list
        return ret_list[0][0][0]

    def set_lang(self, src, dest):
        self.params['sl'] = src
        self.params['tl'] = dest

    def __updata_tk(self):
        self.__TK = CalcTk()
        self.__next_up_time = time.time() + self.updata_time

    def __get_res(self, data):
        res = requests.post(self.url,
                            headers=self.headers,
                            data=data,
                            params=self.params,
                            timeout=6)
        res.raise_for_status()
        return res
