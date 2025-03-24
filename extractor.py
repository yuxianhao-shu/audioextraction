# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib
from videotoaudio import batch_convert
from folder_cleaner import FolderCleaner
load_dotenv()
lfasr_host = 'https://raasr.xfyun.cn/v2/api'
api_upload = '/upload'
api_get_result = '/getResult'

class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        #print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        #print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        #print("upload_url:",response.request.url)
        result = json.loads(response.text)
        #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               print("upload resp:", result)
        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        #print("")
        #print("查询部分：")
        #print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            #print(result)
            status = result['content']['orderInfo']['status']
            #print("status=",status)
            if status == 4:
                break
            time.sleep(5)
        #print("get_result resp:",result)
        return result

def process_folder(folder_path, appid, secret_key):
    # 支持的音频格式列表
    audio_extensions = ('.mp3', '.wav', '.m4a', '.aac', '.flac')
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(audio_extensions):
            file_path = os.path.join(folder_path, filename)
            print(f"正在处理文件: {filename}")
            
            try:
                # 创建API实例并获取结果
                api = RequestApi(appid=appid, 
                               secret_key=secret_key,
                               upload_file_path=file_path)
                data = api.get_result()
                
                # 提取文本内容
                order_result = json.loads(data['content']['orderResult'])
                text_parts = []
                if 'lattice2' in order_result:
                    for item in order_result['lattice2']:
                        rt_list = item.get('json_1best', {}).get('st', {}).get('rt', [])
                        for rt in rt_list:
                            for ws in rt.get('ws', []):
                                if ws.get('cw'):
                                    text_parts.append(ws['cw'][0]['w'])
                
                # 生成输出文件名
                #base_name = os.path.splitext(filename)[0]
                #output_path = os.path.join(folder_path, f"{base_name}_transcript.txt")
                
                # 写入文本文件
                #with open(output_path, 'w', encoding='utf-8') as f:
                    #f.write(''.join(text_parts))
                
                #print(f"转录完成，已保存到: {output_path}")
                print("转录结果：",''.join(text_parts))#结果是''.join(text_parts)
                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
            print("-" * 50)

if __name__ == '__main__':
    # 从环境变量读取配置信息
    APP_ID = os.environ.get('XF_APP_ID')
    SECRET_KEY = os.environ.get('XF_SECRET_KEY')
    # 检查环境变量是否设置
    if not APP_ID or not SECRET_KEY:
        raise ValueError("""
        未找到API认证信息！请按以下步骤操作：
        1. 设置环境变量：
           - Windows: 
               setx XF_APP_ID "your_app_id"
               setx XF_SECRET_KEY "your_secret_key"
           - Linux/macOS:
               export XF_APP_ID="your_app_id"
               export XF_SECRET_KEY="your_secret_key"
        2. 重新启动程序
        """)
    AUDIO_FOLDER = "audio"  # 输入音频目录

    INPUT_DIR = "videos"    # 原始视频目录
    OUTPUT_DIR = "audio"      # 输出音频目录

    WORKERS = os.cpu_count()              # 使用CPU核心数作为并发数
    # 执行转换
    batch_convert(INPUT_DIR, OUTPUT_DIR, WORKERS)
    cleaner = FolderCleaner(
        folder_path="videos",  # 要删除的文件夹路径
        delete_timeout=1      # 设置删除等待时间
    )
    cleaner.clean()
    process_folder(AUDIO_FOLDER, APP_ID, SECRET_KEY)
    cleaner = FolderCleaner(
        folder_path="audio",  # 要删除的文件夹路径
        delete_timeout=1      # 设置删除等待时间
    )
    cleaner.clean()