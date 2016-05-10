pyinstaller --workpath=%TEMP%/pyinst ^
            --distpath=%CD%/exe ^
            --onefile --noconsole ^
            --icon=temp_icon.ico  ^
            --name=tempViewer  ^
            --version-file=version-file.txt main.py