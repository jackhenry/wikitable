# wikitable

A simple python package for retrieving cleaned tables from wikipedia articles

## Getting Started

```
from wikitable import wikitable
raw_html = wikitable.get_html('https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body')
tables = wikitable.get_tables(raw_html)
wikitable.to_csv(tables, 'examples/')

```

## Important
Wikipedia encodes all of their pages in UTF-8. If importing these CSVs into excel, make sure you select UTF-8 and not Windows-1252

## Authors

**Jack Henry**  - [jackhenry](https://github.com/jackhenry)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
