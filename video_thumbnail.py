import cv2
import os
import glob


def generate_video_thumbnail(video_path, output_dir="preview-image", frame_position=0.1):
    """
    讀取影片並產生預覽圖
    
    參數:
        video_path: 影片檔案路徑
        output_dir: 輸出目錄（預設為 preview-image）
        frame_position: 要擷取的影格位置（0.0-1.0，預設0.1代表影片10%位置）
    
    回傳:
        成功則回傳輸出檔案路徑，失敗則回傳 None
    """
    # 檢查影片檔案是否存在
    if not os.path.exists(video_path):
        print(f"錯誤: 找不到影片檔案 {video_path}")
        return None
    
    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 開啟影片
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"錯誤: 無法開啟影片 {video_path}")
        return None
    
    # 取得影片總幀數
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        print("錯誤: 影片沒有幀")
        video.release()
        return None
    
    # 計算要擷取的幀位置
    frame_number = int(total_frames * frame_position)
    
    # 設定影片位置到指定幀
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # 讀取該幀
    success, frame = video.read()
    
    if not success:
        print(f"錯誤: 無法讀取第 {frame_number} 幀")
        video.release()
        return None
    
    # 產生輸出檔案路徑
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_thumbnail.jpg")
    
    # 儲存圖片
    cv2.imwrite(output_path, frame)
    
    # 釋放影片資源
    video.release()
    
    print(f"成功產生預覽圖: {output_path}")
    return output_path


def process_video_directory(video_dir="video", output_dir="preview-image", frame_position=0.1):
    """
    處理指定目錄中的所有影片檔案
    
    參數:
        video_dir: 影片目錄（預設為 video）
        output_dir: 輸出目錄（預設為 preview-image）
        frame_position: 要擷取的影格位置（0.0-1.0）
    
    回傳:
        成功處理的影片數量
    """
    # 檢查影片目錄是否存在
    if not os.path.exists(video_dir):
        print(f"錯誤: 找不到影片目錄 {video_dir}")
        return 0
    
    # 支援的影片格式
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv', '*.m4v']
    
    # 找出所有影片檔案
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(video_dir, ext)))
        video_files.extend(glob.glob(os.path.join(video_dir, ext.upper())))
    
    if not video_files:
        print(f"在 {video_dir} 目錄中找不到影片檔案")
        return 0
    
    print(f"找到 {len(video_files)} 個影片檔案")
    
    # 處理每個影片
    success_count = 0
    for video_file in video_files:
        print(f"\n處理: {video_file}")
        result = generate_video_thumbnail(video_file, output_dir, frame_position)
        if result:
            success_count += 1
    
    print(f"\n完成! 成功處理 {success_count}/{len(video_files)} 個影片")
    return success_count


if __name__ == "__main__":
    # 處理 video 目錄中的所有影片，預覽圖儲存到 preview-image 目錄
    process_video_directory(video_dir="video", output_dir="preview-image")
    
    # 或處理單一影片
    # generate_video_thumbnail("video/your_video.mp4", "preview-image")
