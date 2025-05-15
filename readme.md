```Tvoje máma 3000``` je balík funkcí, které opakovaně využívám v datařských projektech.

## Instalace a import

Stačí rozbalit do složky s projektem:

```curl -LkSs https://github.com/michalkasparek/tm3k/archive/main.zip -o repo.zip && unzip repo.zip && mv tm3k-main tm3k && rm repo.zip```

A pak už to čaruje:

```from tm3k import irozhlas_graf``` (nebo jiná funkce)

Prerekvizity se liší funkce od funkce. Ono se to kdyžtak ozve, že něco chybí.

## Jednotlivé funkce

```ascii_barchart.py``` vyrábí z pandas Series ASCII grafy.

```irozhlas_graf``` vyrábí z pandas Series grafy v HighCharts.

```irozhlas_tabulka``` vyrábí z pandas DataFrame tabulky zformátované pro iROZHLAS.cz.

```kristi_promin``` ostyluje grafy v Altairu do samizdatí podoby (```alt.themes.register('irozhlas', kristi_promin)``` + ```alt.themes.enable('irozhlas')```).

```me_to_neurazi``` uloží altairový graf do SVG s kredity vpravo dole.

```notebook2script``` konvertuje Jupyter Notebooks na spustitelné skripty (velmi nedoporučuji používat v seriózních projektech)

```find_notebooks``` najde ve složce všechny Jupyter Notebooks.

```site_crawl``` prochází doménu a ukládá interní odkazy do textových souborů.

```site_dl``` postahuje seznam odkazů.