# Screenshot Rename Tool

## 概要
このツールは指定されたスクリーンショットフォルダを監視し、新しい画像が追加されたときに自動的に処理を実行するスクリプトです。

## 機能
- 指定フォルダの監視（inotifywaitを使用）
- 新規ファイル検出時の自動処理実行
- システム起動時の自動実行（systemdサービス）
- 
## ファイル名の命名規則

### 監視対象のスクリーンショットファイル
スクリーンショットツールで作成されるファイルは以下の形式に従います：

- Screenshot from YYYY-MM-DD HH-MM-SS.png
  - 例：Screenshot from 2025-01-06 23-10-00.png

### 注意事項
- ファイル形式は.png形式のみ対応しています
- ファイル名に含まれる日時は、スクリーンショット作成時の時刻です
- 手動でファイル名を変更した場合、処理が実行されない可能性があります

### 処理後のファイル名
処理後のファイルは以下の形式で保存されます：

- {リネーム前のファイル名に付与されたいた日時}_Cap_{画像の説明}.png
  - 例：2025-01-06T23_10_00_Cap_ScreenshotFileNamingGuidelines.png

このファイル名の規則は`screen.sh`内で設定されています。
必要に応じて、`screen.sh`内のファイル名変換ロジックを修正してください。

## 必要要件
- Ubuntu 24.04 LTS (他のLinuxディストリビューションでも動作する可能性があります)
- inotify-tools
- bash
- OpenAI API Key

## インストール方法

1. 必要なパッケージのインストール:
```bash
sudo apt install inotify-tools
```

2. スクリプトのダウンロード:
```bash
git clone https://github.com/Tomatio13/screenshot-rename.git
cd screenshot-rename
```
3. スクリプトに実行権限を付与:
```bash
chmod +x watch_screenshots.sh
```
4. 仮想環境の作成と必要なパッケージのインストール:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 設定方法

### 1. フォルダパスの設定
`watch_screenshots.sh`の以下の変数を環境に合わせて変更してください：
```bash
WATCH_DIR="/home/your_username/Pictures/スクリーンショット"  # 監視するフォルダパス
SCRIPT_TO_RUN="/path/to/screenshot-rename/screen.sh"                # 実行するスクリプトのパス
```
`screen.sh`の以下の変数を環境に合わせて変更してください：
```bash
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
cd /path/to/screenshot-rename
LOG_FILE="/path/to/screenshot-rename/rename_log.txt"
```

### 2. 自動起動の設定（オプション）

1. systemdサービスファイルの作成:
```bash
sudo nano /etc/systemd/system/screenshot-watcher.service
```

2. 以下の内容を貼り付け、パスとユーザー名を適切に変更:
```ini
[Unit]
Description=Screenshot Directory Watcher
After=network.target

[Service]
Type=simple
User=your_username
ExecStart=/path/to/watch_screenshots.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

3. サービスの有効化と起動:
```bash
sudo systemctl enable screenshot-watcher
sudo systemctl start screenshot-watcher
```

## 使用方法

### 手動実行
```bash
./watch_screenshots.sh
```

### バックグラウンド実行
```bash
./watch_screenshots.sh &
```

### ログの確認（systemd使用時）
```bash
journalctl -u screenshot-watcher
```

## トラブルシューティング

### スクリプトが実行されない場合
1. フォルダのパーミッションを確認
```bash
ls -l /home/your_username/Pictures/スクリーンショット
```

2. inotifywaitが正しく動作しているか確認
```bash
inotifywait -m /home/your_username/Pictures/スクリーンショット
```

### サービスが起動しない場合
1. サービスのステータスを確認
```bash
sudo systemctl status screenshot-watcher
```

2. ログを確認
```bash
journalctl -u screenshot-watcher -n 50
```

## ライセンス
MIT

