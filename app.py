from flask import Flask
from flask import render_template
from flask import request

import json

from GoogleFreeTrans import Translator

app = Flask(__name__)

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ
    
@app.errorhandler(500)
def internal_error(error):
    return ajax_resp(-1, '500', '翻译服务异常, exception: ' + error.original_exception.args[0])

@app.route('/')
def hello_world():
    return render_template('index.html')
    
@app.route('/translate', methods=['POST', 'GET'])
def translate():
    chain = 'zh-CN,en,ru,zh-CN'
    KEY_CONTENT = 'content'
    KEY_CHAIN = 'chain'
    if request.method=='POST':
        content = request.form[KEY_CONTENT] or ''
        chain = request.form.get(KEY_CHAIN) or chain
    if request.method == 'GET':
        content = request.args.get(KEY_CONTENT) or ''
        chain = request.args.get(KEY_CHAIN) or chain
    if content == '' or content is None:
        return ajax_resp(-1, 'FAIL', '没有内容')
    langs = chain.split(',')
    src = langs[0].strip()
    step_msg = ''
    translator = Translator.translator('zh-CN', 'en')
    for i in range(1, len(langs)):
        dest = langs[i].strip()
        print('%s -> %s' % (src, dest))
        translator.set_lang(src, dest)
        ret_list = translator.translate(content, multi=True)[0]
        ret_content = ''
        for i, item in enumerate(ret_list):
            ret_content = ret_content + item[0] + '.'
        content = ret_content[:-1]
        step_msg = step_msg + src + '->' + dest + ': ' + content + '\n'
        src = dest
    result = '译文: ' + content + '\n\n翻译过程:\n' + step_msg
    return ajax_resp(0, 'SUCCESS', result)
    
def ajax_resp(code, msg, data):
    resultJson = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return json.dumps(resultJson)

def start():
  return json.dumps({
    'code': '0'
  }) 
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)