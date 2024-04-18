def ascii_barchart(
    s, sirka=25, whitespace="~", hranice="", vypln="▒", hodnota=True, titulek=False
):
    """
    Vytvoří ASCII barchart z pandas Series.
    """

    if s.min() < 0:
        return "Neumím udělat graf se zápornými hodnotami :("

    ser = s.copy()
    ser = ser.apply(lambda x: round(x, 0))

    nejvic = ser.max()
    pomer = sirka / nejvic

    nejdelsi = max(len(item) for item in ser.index.to_list())

    grafik = ""

    if titulek:
        grafik += f"{ser.name}\n\n"

    for index, row in ser.items():
        doplnit = nejdelsi - len(index)
        doplnit = doplnit * whitespace
        velikost = int(round(pomer * row, 0))
        mezera = ""
        if velikost > 0:
            mezera = " "
        velikost = velikost * vypln
        cislo = ""
        if hodnota:
            cislo = f"{mezera}{int(round(row, 0))}"
        radek = f"{doplnit}{index} {hranice}{velikost}{cislo}"
        grafik += radek + "  \n"

    return grafik


def irozhlas_graf(
    carovy=[],
    sloupcovy=[],
    vodorovny=[],
    procenta=[],
    skryte=[],
    barvy=[],
    histogram=False,
    max_procenta=100,
    target="",
    titulek="",
    podtitulek="",
    osay=" ",
    osay2=" ",
    osaymin=None,
    osaymax=None,
    kredity=["zdroj dat a autorstvo", "url odkazu"],
    zaokrouhleni=1,
    prvni=True,
    skladany=False,
    naopak=False,
    vzhurunohama=False,
    skrytnuly=False,
):
    """
    Funkce vygeneruje HighCharts graf z pandas Series (jedné nebo více).

    iROZHLAS-friendly barvy:
    - "#b2e061" světle zelená
    - "#7eb0d5" světle modrá
    - "#fd7f6f" světle červená
    - "#bd7ebe" světle fialová
    - "#ffb55a" oranžová
    - "#ffee65" žlutá
    - "#beb9db" levandulová
    - "#fdcce5" skoro černá
    - "#8bd3c7" světle tyrkysová
    """

    import os
    import pandas as pd
    from highcharts_core.chart import Chart
    from highcharts_core.options.series.area import LineSeries
    from highcharts_core.options.series.bar import ColumnSeries
    from highcharts_core.options.series.bar import BarSeries
    from highcharts_core.options.series.histogram import HistogramSeries
    from highcharts_core.options.legend import Legend
    from highcharts_core.options.title import Title
    from highcharts_core.options.subtitle import Subtitle
    from highcharts_core.options.credits import Credits

    nastaveni = {}

    if prvni:
        zdrojaky = f"""<script src="https://code.highcharts.com/highcharts.js"></script><style type="text/css">text{{font-family:"Asap"!important}}.paragraph{{font-family:"Noticia text"!important}}.href{{color:#666;fill:#666}}.highcharts-title{{font-family:"Noticia text"!important;font-weight:700!important;text-align:left!important;left:10px!important}}.highcharts-subtitle{{text-align:left!important;font-size:.95rem!important;left:10px!important;font-family:"Asap"!important}}.highcharts-data-labels text{{font-size:.85rem!important}}.highcharts-axis-labels text{{font-size:.85rem!important}}text.highcharts-plot-line-label{{font-size:.85rem!important;fill:#666}}text.highcharts-plot-band-label{{font-size:.85rem!important;fill:#666}}text.highcharts-credits{{font-size:.75rem!important}}.highcharts-tooltip span{{font-family:"Asap"!important}}.axis-label-on-tick{{fill:#aaa;color:#aaa}}.mock-empty-line{{fill:#fff;color:#fff}}</style>"""
    else:
        zdrojaky = ""

    pred = f"""{zdrojaky}
        <figure id="{target}">
        <div id="container"></div>
        </figure>
        <script>"""

    if len(carovy) > 0:
        categories = carovy[0].index.to_list()
    if len(sloupcovy) > 0:
        categories = sloupcovy[0].index.to_list()
    if len(vodorovny) > 0:
        categories = vodorovny[0].index.to_list()

    categories = [str(x) for x in categories]

    nastaveni["xAxis"] = {"categories": categories, "min": 0}
    nastaveni["yAxis"] = [
        {
            "title": {"text": osay},
            "reversed": vzhurunohama,
            "max": osaymax,
            "min": osaymin,
        }
    ]

    if skladany:
        if len(sloupcovy) > 0:
            nastaveni["plotOptions"] = {"column": {"stacking": "normal"}}
        if len(vodorovny) > 0:
            nastaveni["plotOptions"] = {"bar": {"stacking": "normal"}}
    if histogram:
        nastaveni["plotOptions"] = {
            "column": {
                "pointPadding": 0,
                "borderWidth": 0,
                "groupPadding": 0,
                "shadow": False,
            }
        }

    if len(procenta) > 0:
        osa_procent = {
            "title": {"text": osay2},
            "max": max_procenta,
            "min": 0,
            "labels": {"format": "{value} %"},
        }

        if len(procenta) != len(carovy) + len(sloupcovy):
            osa_procent["opposite"] = True
            druha_osa = 1
            nastaveni["yAxis"].append(osa_procent)
            nastaveni["alignTicks"] = False
        if len(procenta) == len(carovy) + len(sloupcovy):
            nastaveni["yAxis"] = [osa_procent]
            druha_osa = 0

    my_chart = Chart(container=target, options=nastaveni)

    procenta = [p.name for p in procenta]
    skryte = [s.name for s in skryte]

    def vykresleni(serie, typ):
        for s in serie:
            popisek = s.name

            if s.name in skryte:
                viditelnost = False
            else:
                viditelnost = True

            if s.name in procenta:
                s = [round(x * 100, zaokrouhleni) for x in s.fillna(0).to_list()]
                my_chart.add_series(
                    typ(
                        data=s,
                        visible=viditelnost,
                        name=popisek,
                        y_axis=druha_osa,
                        tooltip={"valueSuffix": " %"},
                    )
                )
            else:
                my_chart.add_series(
                    typ(
                        data=s.fillna(0).to_list(),
                        visible=viditelnost,
                        name=popisek,
                        y_axis=0,
                    )
                )

    if len(sloupcovy) > 0:
        vykresleni(sloupcovy, ColumnSeries)
    if len(carovy) > 0:
        vykresleni(carovy, LineSeries)
    if len(vodorovny) > 0:
        vykresleni(vodorovny, BarSeries)

    if len(barvy) > 0:
        my_chart.options.colors = barvy
    else:
        my_chart.options.colors = colors = [
            "#b2e061",  ## světle zelená (light green)
            "#7eb0d5",  ## světle modrá (light blue)
            "#fd7f6f",  ## světle červená (light red)
            "#bd7ebe",  ## světle fialová (light purple)
            "#ffb55a",  ## oranžová (orange)
            "#ffee65",  ## žlutá (yellow)
            "#beb9db",  ## levandulová (lavender)
            "#fdcce5",  ## skoro černá
            "#8bd3c7",  ## světle tyrkysová (light turquoise)
        ]

    if naopak:
        my_chart.options.legend = Legend(reversed=True)

    my_chart.options.title = Title(text=titulek, align="left", margin=30)

    if len(podtitulek) > 0:
        my_chart.options.subtitle = Subtitle(text=podtitulek, align="left")

    my_chart.options.credits = Credits(text=kredity[0], enabled=True, href=kredity[1])

    as_js_literal = my_chart.to_js_literal()

    if skrytnuly == True:
        as_js_literal = as_js_literal.replace("y: 0.0", "y: null")

    code = f"<html><head><title>{titulek}</title></head><body>{pred}{as_js_literal}</script></body></html>"

    if not os.path.exists("grafy"):
        os.mkdir("grafy")

    with open(os.path.join("grafy", target + ".html"), "w+") as f:
        f.write(code)

    with open(os.path.join("grafy", target + ".txt"), "w+") as f:
        f.write(f"{pred}{as_js_literal}</script>")

        print("Graf uložen.")


def irozhlas_tabulka(
    frame,
    titulek="",
    podtitulek="",
    bez_tecky=[],
    na_procenta=[],
    poradi=False,
    bez_zavorek=True,
    apostrofy=True,
):
    """
    Funkce generuje HTML tabulku pro přímé vložení do článku na iROZHLAS.cz z pandas DataFrame.
    """

    import pandas as pd

    df_tabulka = frame.copy()

    def cela(x):
        try:
            x = int(x)
        except:
            x = "–"
        return x

    import re

    if poradi:
        sloupce = df_tabulka.columns.tolist()
        df_tabulka = df_tabulka.reset_index(drop=True)
        df_tabulka[" "] = pd.to_numeric(df_tabulka.index)
        df_tabulka[" "] = df_tabulka[" "].apply(lambda x: str(x + 1) + ".")
        nove_sloupce = [" "]
        for s in sloupce:
            nove_sloupce.append(s)
        df_tabulka = df_tabulka[nove_sloupce]

    sloupcu = len(df_tabulka.columns)

    if len(bez_tecky) > 0:
        for b in bez_tecky:
            df_tabulka[b] = df_tabulka[b].apply(lambda x: cela(x))

    if len(na_procenta) > 0:
        for p in na_procenta:
            df_tabulka[p] = df_tabulka[p].apply(lambda x: "{:.1%}".format(x))
            df_tabulka[p] = (
                df_tabulka[p]
                .astype("string")
                .apply(lambda x: x.replace(".", ",").replace("%", " %"))
            )

    df_tabulka = re.sub("\\n\s*", "", df_tabulka.to_html(index=False))
    df_tabulka = (
        df_tabulka.replace("<th>", '<th class="text-nowrap">')
        .replace("<tbody>", '<tbody class="text-sm">')
        .replace('border="1" ', "")
        .replace(
            'class="dataframe"',
            'class="dataframe table table--responsive table--w100p table--striped-red table--plain"',
        )
        .replace(" , ", ", ")
    )

    if apostrofy == True:
        df_tabulka = df_tabulka.replace("'", "’")

    if len(titulek) > 0:
        df_tabulka = df_tabulka.replace("<thead", f"<caption>{titulek}</caption><thead")

    if len(podtitulek) > 0:
        df_tabulka = df_tabulka.replace(
            "</tbody>",
            f'</tbody><tfoot><tr style="text-align: center;"><td colspan={sloupcu}>{podtitulek}</td></tr></tfoot>',
        )

    if bez_zavorek:
        df_tabulka = re.sub("\([\d]*\)", "", df_tabulka)
        df_tabulka = df_tabulka.replace(" </td>", "</td>")

    return df_tabulka


def notebook2script(jupyter_notebook):
    """A super-simple (and probably highly unreliable) tool for converting Jupyter Notebooks into Python scripts."""

    try:

        import json

        with open(jupyter_notebook, "r", encoding="utf8") as notebook:
            notebook = json.load(notebook)

            code = ""

            for c in notebook["cells"]:
                if c["cell_type"] == "code":
                    code += "\n".join(c["source"]) + "\n\n"

            print(code)

        filename = jupyter_notebook.replace(".ipynb", ".py")

        with open(filename, "w+", encoding="utf-8") as script:
            script.write(code)

        print(f"Sešit {jupyter_notebook} uložen jako skript {script}.")

    except Exception as e:

        print(f"Sešit {jupyter_notebook} se nepodařilo uložit jako skript, neboť: {e}.")


def find_notebooks(folder=".", stop=False):
    """Funkce pro vyhledání Jupyter Notebooks ve složce."""

    import os

    ipynb_files = [file for file in os.listdir(folder) if file.endswith(".ipynb")]

    ipynb_files.sort()

    if stop != False:

        for index, item in enumerate(ipynb_files):

            if stop in item:

                ipynb_files = ipynb_files[: index + 1]

    print(f"""Seznam sešitů: {", ".join(ipynb_files)}""")

    return ipynb_files


def site_crawl(url, pause=0, max_threads=10):
    """
    Funkce procrawluje stránky na doméně. Nalezené odkazy průběžně ukládá do textových souborů, takže její běh lze přerušovat. Tyto seznamy lze následně využít pro stahování obsahu webu nebo jeho části.

    Parametry:
    - url: doména
    - pause: pauza v sekundách mezi jednotlivými požadavky na server (defaultně 0)
    """

    import os
    import time
    import requests
    from datetime import datetime
    from threading import Thread
    from queue import Queue
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup

    def get_domain(http):
        domain = "https://" + http.split("/")[2]
        return domain

    def clean_list(file):
        file.seek(0)
        contents = file.read().splitlines()
        return [line.strip() for line in contents if line.strip()]

    def get_all_links(url, printurl=True):
        not_a_page = {".jpg", ".pdf", ".mp3", ".wav"}
        if printurl:
            print(url)
        urls_on_page = set()
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            link_url = link.get("href")
            if link_url:
                link_url = urljoin(url, link_url)  # Combine base URL with relative URL
                if link_url not in urls_on_page:
                    try:
                        if domain in link_url and link_url[-4:0] not in not_a_page:
                            urls_on_page.add(link_url)
                    except Exception as e:
                        print(f"Error processing URL '{link_url}': {e}")
        return urls_on_page

    def save_everything():
        with open(
            os.path.join(folder, filename_all), "w", encoding="utf-8"
        ) as file_all:
            file_all.write("\n".join(urls_all))
        with open(
            os.path.join(folder, filename_visited), "w", encoding="utf-8"
        ) as file_visited:
            file_visited.write("\n".join(urls_visited))
        with open(
            os.path.join(folder, filename_unvisited), "w", encoding="utf-8"
        ) as file_unvisited:
            file_unvisited.write("\n".join(urls_unvisited))

    session = requests.Session()  # Create session

    queue = Queue()
    for _ in range(max_threads):
        worker = Thread(target=get_all_links, args=(queue,))
        worker.start()

    domain = get_domain(url)

    crawled_domain = domain.replace("https://", "")

    filename_all = crawled_domain + "_all" + ".txt"
    filename_visited = crawled_domain + "_visited" + ".txt"
    filename_unvisited = crawled_domain + "_unvisited" + ".txt"
    folder = f"""crawl_{crawled_domain}"""

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join(folder, filename_all), "a+", encoding="utf-8") as file_all:
        urls_all = clean_list(file_all)
    with open(
        os.path.join(folder, filename_visited), "a+", encoding="utf-8"
    ) as file_visited:
        urls_visited = clean_list(file_visited)
    with open(
        os.path.join(folder, filename_unvisited), "a+", encoding="utf-8"
    ) as file_unvisited:
        urls_unvisited = clean_list(file_unvisited)

    urls_unvisited = list(set(urls_unvisited) - set(urls_visited))

    if url not in urls_unvisited:
        urls_unvisited.append(url)

    urls_all = list(set(urls_all + urls_visited + urls_unvisited))

    while urls_unvisited:

        unvisited = urls_unvisited.pop(0)
        new_links = get_all_links(unvisited, printurl=True)
        urls_visited.append(unvisited)

        for new_link in new_links:
            new_link = new_link.split("#")[0]
            if new_link not in urls_visited and new_link not in urls_unvisited:
                urls_unvisited.append(new_link)
                urls_all.append(new_link)

        no_visited = len(urls_visited)
        no_unvisited = len(urls_unvisited)
        no_all = len(urls_all)
        no_control = no_visited + no_unvisited - no_all

        print(
            f"""{datetime.now().strftime("%H:%M:%S")} / visited: {no_visited} / univisited: {no_unvisited} / total: {no_all} / control: {no_control}"""
        )

        if no_visited % 50 == 0:  # nechceme zdržovat a opotřebovávat paměťovou kartu
            save_everything()

        time.sleep(pause)

    save_everything()

    return urls_all


def site_download(folder, urls, url_filter, pause=0):
    """
    Stáhne seznam URL adres.

    Parametry:
    - folder: název složky, kam se mají uložit stažené soubory
    - urls: seznam URL adres
    - url_filter: jednoduchý filtr, například "/cs/person" v "https://www.filmovyprehled.cz/cs/person/936/marek-daniel"
    """

    import os
    import requests
    import time
    import datetime

    def filename(url):
        return "-".join(url.split("/")[-2:]) + ".html"

    def seznam_souboru(slozka):
        seznam = []
        for file in os.listdir(slozka):
            seznam.append(file)
        return seznam

    print(f"datum: {datetime.date.today()}")

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        pass

    filtered_urls = [url for url in urls if url_filter in url]

    remaining = len(filtered_urls)

    errors = []

    for url in filtered_urls:

        time.sleep(pause)

        try:

            remaining = remaining - 1

            print(f"downloading {url}, {remaining} remaining")

            if filename(url) not in seznam_souboru(folder):

                r = requests.get(url)

                with open(
                    os.path.join(folder, filename(url)), "w+", encoding="utf-8"
                ) as f:
                    f.write(r.text)

        except:

            print(f"CHYBA {url}")
            errors.append(url)

    if len(errors) > 0:

        print("Waiting for 5 minutes before retrying failed downloads.")

        time.sleep(300)

        print(f"Retrying {len(errors)} failed downloads:")

        for url in errors:

            print(f"downloading {url}, {remaining} remaining")

            time.sleep(pause)

            try:
                r = requests.get(url)

                with open(
                    os.path.join(folder, filename(url)), "w+", encoding="utf-8"
                ) as f:
                    f.write(r.text)

            except:
                print(f"URL {url} failed again")
