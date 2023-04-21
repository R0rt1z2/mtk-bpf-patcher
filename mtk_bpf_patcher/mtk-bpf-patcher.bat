@echo off
setlocal EnableDelayedExpansion

chcp 65001 2>nul >nul

:: Save the original current path
set "original_path=%CD%"

:: Location should be where the main.py file is located
:: This will be automatically updated via Install script
cd "C:\Program Files\Python*\Scripts\mtk_bpf_patcher\mtk_bpf_patcher" 2>nul >nul

if exist main.py (
    set "abs_args="
    set "arg_count=0"
    :arg_loop
    if not "%~1"=="" (
        set /A "arg_count+=1"
        if !arg_count! LEQ 2 (
            for %%A in ("%original_path%\%~1") do set "abs_arg=%%~fA"
        ) else (
            set "abs_arg=%~1"
        )
        set "abs_args=!abs_args! "!abs_arg!""
        shift
        goto arg_loop
    )
    python main.py !abs_args!
	pause
	exit
) else (
    powershell write-host -fore Red mtk-bpf-patcher not found!
)

pause
