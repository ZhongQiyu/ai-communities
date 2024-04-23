@echo off
setlocal enabledelayedexpansion

for %%i in ("%cd%") do set "folder_name=%%~nxi"

git init
git remote remove origin
git remote add origin git@atomgit.com:xway-1/%folder_name%.git

echo upload.bat > .gitignore
git add .
git commit -m "Initial commit"
git push -u origin master

start cmd /c del %0

@echo off
setlocal enabledelayedexpansion

:: 获取当前目录名称
for %%i in ("%cd%") do set "folder_name=%%~nxi"

:: 初始化git仓库并设置远程仓库
git init
git remote remove origin
git remote add origin git@atomgit.com:xway-1/%folder_name%.git

:: 生成默认提交信息
set filename="Auto-commit on %date:~0,4%-%date:~5,2%-%date:~8,2% at %time:~0,2%:%time:~3,2%"
set "filename=%filename: =0%"

:: 用户交互输入提交信息
set /p "content=请输入提交说明(回车则默认 '%filename%')："
if "!content!"=="" set "content=%filename%"

:: 用户交互输入分支名
set "branch=master"
set /p "branch=请输入提交分支(回车则默认master)："

:: 添加.gitignore规则
echo upload.bat > .gitignore

:: 添加、提交更改到仓库
git add .
git commit -m "%content%"
git push -u origin %branch%

:: 删除这个批处理文件，取消下面一行注释来启用
:: start cmd /c del %0

pause
endlocal
