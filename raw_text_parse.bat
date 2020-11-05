@echo off

for %%I in (%*) do (
echo %%I
python "%~dp0\pyscripts\parse_raw_text.py" %%I
echo.
)
