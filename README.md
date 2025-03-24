# audioextraction
 ```markdown
# 音频提取与语音转文字工具

本项目提供将视频文件转换为音频，并利用科大讯飞API进行语音转文字的功能，适用于视频内容分析、字幕生成等场景。

## 主要功能

- 🎬 视频文件转音频（支持常见视频格式）
- 🎙️ 音频内容转文字（基于科大讯飞语音转写API）
- 🧹 自动清理临时文件
- 🔒 环境变量保护敏感信息

## 环境要求

- Python 3.9
- pip 包管理工具
- 科大讯飞开发者账号（免费获取50小时试用时长）

## 🛠️ 安装指南

### 1. 克隆仓库
```bash
git clone https://github.com/yuxianhao-shu/audioextraction.git
cd audioextraction
```

### 2. 创建虚拟环境
```bash
python -m venv venv  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. API密钥配置
1. 访问[科大讯飞控制台](https://www.xfyun.cn/services/lfasr)注册并完成实名认证
2. 创建`.env`文件：
```bash
touch .env
```
3. 添加密钥信息：
```ini
XF_APP_ID = "您的应用ID"
XF_SECRET_KEY = "您的密钥"
```

## 🚀 快速开始

1. 将待处理视频文件放入`/videos`目录
2. 运行主程序：
```bash
python extractor.py
```
3. 转写结果将保存在`/results`目录（自动创建）

## ⚠️ 重要注意事项

- 处理完成后将自动清空以下目录：
  - `/videos` 
  - `/audio`（临时音频存储）
- 支持视频格式：mp4, avi, mov 等常见格式
- 转写时长限制：单文件最长4小时（讯飞API限制）

## 📁 目录结构
```
.
├── videos/          # 视频输入目录
├── audio/           # 临时音频存储（自动清理）
├── results/         # 转写结果输出
├── .env             # 密钥配置文件
├── extractor.py     # 主程序
├── folder_cleaner.py# 用于清空文件夹
├── videotoaudio.py  # 用于视频转音频
└── requirements.txt # 依赖列表
```

## 📄 许可证
MIT License - 详见项目文件
```