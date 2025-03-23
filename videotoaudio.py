import os
import logging
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor

def setup_logger():
    """配置日志记录器"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conversion.log'),
            logging.StreamHandler()
        ]
    )

def validate_paths(input_dir, output_dir):
    """验证并创建必要目录"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"输出目录已创建: {output_dir}")

def get_video_files(input_dir):
    """获取待处理视频文件列表"""
    valid_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
    return [
        os.path.join(input_dir, f) for f in os.listdir(input_dir)
        if f.lower().endswith(valid_extensions)
    ]

def convert_single(video_path, output_dir):
    """单个视频转换处理"""
    try:
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.mp3")
        
        # 检查是否已存在转换后的文件
        if os.path.exists(output_path):
            logging.warning(f"文件已存在，跳过转换: {output_path}")
            return True

        with VideoFileClip(video_path) as video:
            audio = video.audio
            audio.write_audiofile(output_path, codec='mp3', 
                                bitrate='192k', 
                                ffmpeg_params=['-ar', '44100'])
            audio.close()
        
        logging.info(f"转换成功: {video_path} -> {output_path}")
        return True
    except Exception as e:
        logging.error(f"转换失败 [{video_path}]: {str(e)}")
        return False



def batch_convert(input_dir, output_dir, max_workers=4):
    """批量转换入口函数"""
    setup_logger()
    
    try:
        validate_paths(input_dir, output_dir)
        video_files = get_video_files(input_dir)
        
        if not video_files:
            logging.warning("没有找到可转换的视频文件")
            return

        logging.info(f"发现 {len(video_files)} 个待处理视频")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for video_path in video_files:
                future = executor.submit(
                    convert_single, 
                    video_path, 
                    output_dir
                )
                futures.append((video_path, future))

        logging.info("全部转换任务已完成")
        
    except Exception as e:
        logging.error(f"程序异常终止: {str(e)}")
        raise

if __name__ == "__main__":
    # 配置参数
    INPUT_DIR = "videos"    # 原始视频目录
    OUTPUT_DIR = "audio"      # 输出音频目录
    WORKERS = os.cpu_count()              # 使用CPU核心数作为并发数

    # 执行转换
    batch_convert(INPUT_DIR, OUTPUT_DIR, WORKERS)