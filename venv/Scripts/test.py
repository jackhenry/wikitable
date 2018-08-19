from wikitable import wikitable

url = 'https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body'

html = wikitable.get_html(url)
tables = wikitable.get_tables(html)
wikitable.to_csv(tables, 'C:/Users/Malone/Desktop/')