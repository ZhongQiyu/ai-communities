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
