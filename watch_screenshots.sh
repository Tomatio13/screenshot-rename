#!/bin/bash

WATCH_DIR="/home/your_username/Pictures/スクリーンショット"
SCRIPT_TO_RUN="/path/to/screenshot-rename/screen.sh"

# ディレクトリが存在することを確認
if [ ! -d "$WATCH_DIR" ]; then
    echo "監視対象のディレクトリが存在しません: $WATCH_DIR"
    exit 1
fi

# inotify-toolsがインストールされているか確認
if ! command -v inotifywait &> /dev/null; then
    echo "inotify-toolsがインストールされていません。インストールしてください。"
    echo "sudo apt install inotify-tools"
    exit 1
fi

echo "ディレクトリの監視を開始します: $WATCH_DIR"

# ディレクトリを監視し、新しいファイルが作成されたら指定のスクリプトを実行
inotifywait -m -e create -e moved_to "$WATCH_DIR" |
while read -r directory events filename; do
    echo "新しいファイルを検出: $filename"
    "$SCRIPT_TO_RUN" "$WATCH_DIR"
done 