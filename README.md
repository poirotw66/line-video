# LINE 推播影片與預覽圖空間

此專案用來集中管理要透過 LINE Bot / LINE Notify 推播的媒體資源，並提供 `video_thumbnail.py` 腳本協助從影片中擷取預覽圖，方便在訊息中附上縮圖或在後台快速檢視內容。

## 目前內容

```
├── video/              # 放置待推播的影片（範例：spark.mp4）
├── preview_image/      # 已生成的縮圖範例（spark.png）
├── preview-image/      # 腳本預設輸出資料夾（執行後會自動建立）
├── video_thumbnail.py  # 影片轉縮圖腳本
└── requirement.txt     # Python 依賴，目前僅需 opencv-python
```

> 提示：腳本預設輸出目錄名稱為 `preview-image`，若希望沿用既有的 `preview_image`，可在程式中調整 `output_dir` 參數或在 Python 互動式環境呼叫 `process_video_directory(..., output_dir="preview_image")`。

## 環境準備

1. 安裝 Python 3.10+。
2. （可選）建立虛擬環境：`python -m venv .venv && source .venv/bin/activate`
3. 安裝依賴：`pip install -r requirement.txt`

## 產生影片預覽圖

`video_thumbnail.py` 提供兩個主要函式：

- `generate_video_thumbnail(video_path, output_dir="preview-image", frame_position=0.1)`
  - 讀取單一影片並擷取指定位置（預設 10%）的影格作為縮圖。
- `process_video_directory(video_dir="video", output_dir="preview-image", frame_position=0.1)`
  - 批次處理資料夾內的所有影片。

### 全自動批次流程

1. 將欲推播的影片放入 `video/`。
2. 執行 `python video_thumbnail.py`。
3. 產生的縮圖會儲存在 `preview-image/`（或自訂目錄），檔名為 `<影片檔名>_thumbnail.jpg`。

### 自訂擷取位置與輸出目錄

```bash
python - <<'PY'
from video_thumbnail import process_video_directory
process_video_directory(
    video_dir="video",
    output_dir="preview_image",   # 與現有資料夾一致
    frame_position=0.25           # 擷取影片 25% 位置
)
PY
```

## 與 LINE 推播串接的建議流程

- 將影片上傳到 LINE 消息可存取的公開 URL（或透過 LIFF/後端動態提供）。
- 使用上述腳本生成的縮圖作為 `previewImageUrl`（適用於 Video message）或作為 Carousel/Rich Menu 素材。
- 依照 LINE Messaging API 文件設定 `originalContentUrl`（指向實際影片）與 `previewImageUrl`（縮圖）。

## 版本控管與擴充建議

- 將每次推播所用的影片與縮圖打包存入 Git，可追蹤歷史素材。
- 若需自動產生影片公開連結，可在此專案加入簡易的靜態網站或物件儲存同步腳本。
- 如要長期維護，建議加入 `Makefile` 或簡易 CLI，將「放影片 → 產縮圖 → 上傳」流程自動化。

有更多需求（如自動上傳至 CDN、加入 LINE webhook 範例等）歡迎提出，我們可以進一步擴充。
