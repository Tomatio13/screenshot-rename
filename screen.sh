#!/bin/zsh
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# APIキーを設定
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'

# ここでは上記pythonスクリプト があるフォルダに移動
cd /path/to/screenshot-rename

# 仮想環境をアクティベート
source venv/bin/activate

# ログファイル（デバッグ用、パスは適宜）
LOG_FILE="/path/to/screenshot-rename/rename_log.txt"
echo "$(date): Starting script" | tee -a "$LOG_FILE"

# 第1引数をディレクトリとして処理
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <ディレクトリパス>" | tee -a "$LOG_FILE"
    exit 1
fi

TARGET_DIR="$1"
if [ ! -d "$TARGET_DIR" ]; then
    echo "エラー: $TARGET_DIR は有効なディレクトリではありません" | tee -a "$LOG_FILE"
    exit 1
fi

# ディレクトリ内のファイルを処理
for f in "$TARGET_DIR"/*; do
    if [ -f "$f" ]; then
        echo "Processing: $f" | tee -a "$LOG_FILE"
        python screenshot_rename.py "$f" 2>&1 | tee -a "$LOG_FILE"
    fi
done

# 仮想環境終了
deactivate

echo "$(date): Script finished" | tee -a "$LOG_FILE"