import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class wikitable:
    
    #function that makes a request to wikipedia and returns the raw html of the page
    def get_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print(http_error)
        return response.content

    #Function containing algorithm that extracts the tables and stores them in dataframes
    def get_tables(html):
        
        #list of dataframes containing the tables. This is what the function returns.
        table_list = []
        
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()
        
        #tables will have the class attribute of wikitable and/or sortable
        tables = soup.find_all('table', {'class': ['wikitable', 'sortable']})
        
        #beginning of algorithm. Go through every table extracted.
        for table in tables:
            
            #grab the table body and each row in the body.
            body = table.find('tbody')
            rows = body.find_all('tr')
            
            #col_len is the amount of columns in the first row.
            #row_len is amount of rows.
            #these values are used to dictate the shape of each dataframe representing each table.
            col_len = len(rows[0].find_all(['td','th'])
            row_len = len(rows)
            
            #the dataframe that will hold all the values of the table.
            #algorithm will index this dataframe like a 2d array
            table_df = pd.DataFrame(columns=np.arange(col_len), index=np.arange(row_len), dtype=str)

            r = 0 #counter for rows processed
            #iterate through every row of table
            for row in rows:
                
                #extract the actual data from the tables. the data will be wrapped in <td> or <th>
                entries = row.find_all(['td','th'])
                #ensure that row length stays below column length of dataframe. this prevents indexing errors.
                if len(entries) <= col_len:
                    entries_len = len(entries)
                else:
                    entries_len = col_len
                #counter for columns processed
                c = 0
                #This for loop goes through all data located in the row and assigns it to its respective
                #location in the dataframe. 
                for index in range(0, entries_len):

                    current_cell_null = pd.isnull(table_df.iloc[r, c])
                    #Check if cell in dataframe has already been written to. (when data is spanned across rows)
                    if current_cell_null:
                        attrs = entries[index].attrs
                        #colspan means that data extends across multiple columns
                        if 'colspan' in attrs:
                            colspan = int(attrs['colspan'])
                            #iterate for every column the data spans
                            for stretch in range(0, colspan):
                                table_df.iloc[r, c] = entries[index].text.strip()
                                c += 1
                        #rowspan indicates that the data extends across multiple rows. similar to colspan except with rows.
                        elif 'rowspan' in attrs:
                            rowspan = int(attrs['rowspan'])
                            for stretch in range(0, rowspan):
                                # print('Stretching rows:' + str(stretch))
                                table_df.iloc[r + stretch, c] = entries[index].text.strip()
                        #data does not span across rows or columns. write to its respective cell and then iterate to next column
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
