@echo off
chcp 65001 >nul
echo =========================================
echo ホームページ更新ツール
echo =========================================
echo.

echo 1. データの自動変換を実行しています...
python convert_data.py
if %errorlevel% neq 0 (
    echo.
    echo [エラー] データの変換中にSyntaxErrorなどが発生しました！
    echo news.txt や profile.txt 内に「意図しないダブルクオーテーション(")」などがないか確認してください。
    pause
    exit /b %errorlevel%
)
echo 完了しました。

echo.
echo 2. GitHubへ変更をアップロード(公開)しています...
git add .
git commit -m "Auto-update website contents via batch file"
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [エラー] サーバーへのアップロードに失敗しました。
    pause
    exit /b %errorlevel%
)

echo.
echo =========================================
echo すべての更新が完了しました！
echo 通常1〜3分程度で実際のホームページアドレスに反映されます。
echo （ブラウザで「Ctrl + F5」の強制リロードをしてください）
echo =========================================
echo 任意のキーを押して画面を閉じてください...
pause >nul
