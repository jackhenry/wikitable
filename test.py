from wikitable import wikitable

html = wikitable.get_html('https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body')
tables = wikitable.get_tables(html)
wikitable.to_csv(tables, 'C:/Users/Jack/Desktop/')