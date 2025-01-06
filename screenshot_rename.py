#!/usr/bin/env python3
import sys
import os
import re

import base64
import openai

def suppress_output():
    class DummyFile:
        def write(self, x): pass
        def flush(self): pass
    return DummyFile()

def sanitize_filename(filename: str) -> str:
    """ファイル名に使えない文字を除外する"""
    sanitized = re.sub(r'[\\/:*?"<>|]+', '_', filename)
    sanitized = sanitized.strip().strip('.')
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized

def extract_datetime_from_filename(filename):
    """元のファイル名から日時情報を抽出"""
    pattern = r'Screenshot from (\d{4})-(\d{2})-(\d{2})\s?(\d{2})-(\d{2})-(\d{2})\.png'
    match = re.match(pattern, filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return f"{year}-{month}-{day}T{hour}_{minute}_{second}"
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python screenshot_rename.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    original_filename = os.path.basename(image_path)
    print(f"元のファイル名: {original_filename}")

    try:
        # まず日時情報を抽出
        datetime_str = extract_datetime_from_filename(original_filename)
        if not datetime_str:
            #print("警告: ファイル名から日時情報を抽出できませんでした")
            return

        # 以下、画像認識の処理
        original_stderr = sys.stderr
        original_stdout = sys.stdout
        sys.stderr = suppress_output()
        sys.stdout = suppress_output()

        # 出力を元に戻す
        sys.stderr = original_stderr
        sys.stdout = original_stdout

        # 画像をbase64エンコード
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Vision APIで画像説明を生成
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at generating descriptive filenames for images. 
                    Always output one CamelCase label starting with 'Cap_' that best describes the image content.
                    Follow these rules:
                    - Start with 'Cap_'
                    - Use CamelCase format
                    - Keep it concise but descriptive
                    - No explanation, just the label
                    - Examples: Cap_PyEnvTerminal, Cap_CookingWebPage, Cap_MarioGame, Cap_Xpost, Cap_JpnAnimeYouTube"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Generate a descriptive filename for this image."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=100
        )
        output = response.choices[0].message.content
        description = output.strip()
        safe_description = sanitize_filename(description)

        # 新しいファイル名（日時_説明.png の形式）
        new_file_name = f"{datetime_str}_{safe_description}.png"
        new_file_path = os.path.join(os.path.dirname(image_path), new_file_name)

        os.rename(image_path, new_file_path)
        print(f"新しいファイル名: {new_file_name}")

    except Exception as e:
        if sys.stderr != original_stderr:
            sys.stderr = original_stderr
        if sys.stdout != original_stdout:
            sys.stdout = original_stdout
        print(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
