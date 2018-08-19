import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class wikitable:

    def get_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print(http_error)
        return response.content


    def get_tables(html):
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()

        tables = soup.find_all('table', {'class': ['wikitable', 'sortable']})

        table_list = []
        table_num = 1
        for table in tables:

            body = table.find('tbody')
            rows = body.find_all('tr')

            col_len = len(rows[0].find_all(['td','th']))
            row_len = len(rows)

            table_df = pd.DataFrame(columns=np.arange(col_len), index=np.arange(row_len), dtype=str)

            r = 0
            for row in rows:

                #headers = row.find_all('th')
                #for header in headers:
                #    header.name = 'td'

                entries = row.find_all(['td','th'])
                if len(entries) <= col_len:
                    entries_len = len(entries)
                else:
                    entries_len = col_len

                c = 0
                for index in range(0, entries_len):

                    current_cell_null = pd.isnull(table_df.iloc[r, c])

                    if current_cell_null:
                        attrs = entries[index].attrs
                        if 'colspan' in attrs:
                            colspan = int(attrs['colspan'])
                            for stretch in range(0, colspan):
                                table_df.iloc[r, c] = entries[index].text.strip()
                                c += 1
                        elif 'rowspan' in attrs:
                            rowspan = int(attrs['rowspan'])
                            for stretch in range(0, rowspan):
                                # print('Stretching rows:' + str(stretch))
                                table_df.iloc[r + stretch, c] = entries[index].text.strip()

                        else:
                            if c < entries_len:
                                table_df.iloc[r, c] = entries[index].text.strip()
                                c += 1

                r += 1
            table_list.append(table_df)
        return(table_list)

    def to_csv(table_list, root_path):
        table_num = 1
        for table in table_list:
            table.to_csv(root_path + 'table' + str(table_num) + '.csv', index=False, header=False)
            table_num += 1