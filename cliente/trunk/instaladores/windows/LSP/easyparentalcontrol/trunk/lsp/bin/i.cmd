instlsp.exe -f
@if "%1" == "" goto end
md temp\v%1
copy easyparentalcontrolfirewall.dll  temp\v%1\easyparentalcontrolfirewall.dll
instlsp.exe -i -a -n "v%1" -d "E:\Proyecto Kerberus\cliente\trunk\instaladores\windows\LSP\easyparentalcontrol\trunk\lsp\bin\temp\v%1\easyparentalcontrolfirewall.dll" 
:end