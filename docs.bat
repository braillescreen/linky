@echo off
mkdir addon\doc\en 2>nul
pandoc readme.md -o addon\doc\en\readme.html --standalone --metadata title="Linky"