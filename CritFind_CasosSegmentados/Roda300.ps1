$arquivos =  Get-ChildItem ".\Casos" -Filter *.txt
Write-Output $arquivos
foreach($caso in $arquivos)
{
    Copy-Item $caso.FullName -Destination .\Caso.txt
    .\critfind300b1000m5k.exe
    $saida = $caso.BaseName+".csv"
    Copy-Item .\Saida.csv -Destination .\Casos\$saida
}