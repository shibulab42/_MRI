@echo off
chcp 65001 >nul
echo =========================================
echo ホームページ更新ツール
echo =========================================
echo.

:: -------------------------------------------------
:: 1. データ自動変換
:: -------------------------------------------------
echo 1. データの自動変換を実行しています...
python convert_data.py
if %errorlevel% neq 0 (
    echo.
    echo [エラー] データ変換中に問題が発生しました。
    pause
    exit /b %errorlevel%
)
echo 完了しました.

:: -------------------------------------------------
:: 2. GitHub へ変更をアップロード (トークン読み込み)
:: -------------------------------------------------
echo.
echo 2. GitHubへ変更をアップロード(公開)しています...

:: ----- トークンファイルの場所 -----
set "TOKEN_FILE=%~dp0Newtokun20260511.txt"

:: ---- トークンが存在しない場合はエラーで止める ----
if not exist "%TOKEN_FILE%" (
    echo [エラー] トークンファイルが見つかりません: %TOKEN_FILE%
    echo       正しいファイル名・場所を確認してください。
    pause
    exit /b 1
)

:: ---- ファイルからトークンを取得（改行は除去） ----
set /p GITHUB_TOKEN=<"%TOKEN_FILE%"
set "GITHUB_TOKEN=%GITHUB_TOKEN: =%"

:: ---- Git 操作 ----
git add .
git commit -m "Auto‑update website contents via batch file"
git push https://%GITHUB_TOKEN%@github.com/shibulab42/_MRI.git

if %errorlevel% neq 0 (
    echo.
    echo [エラー] サーバーへのアップロードに失敗しました。
    echo   (Git のエラーメッセージは上に表示されています)
    pause
    exit /b %errorlevel%
)

echo.
echo =========================================
echo すべての更新が完了しました！
echo （数分でサイトに反映されます → Ctrl+F5 でリロード）
echo =========================================
pause >nul
