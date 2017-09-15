# Commands used to query the papers database using ubuntu linux

The command `sqlite3 database.sqlite` loads the content of database.sqlite file and opens an interactive shell where information can be queried.<br/>

The command `.schema [TABLE]` describes the column names in a table.<\br>

To obtain the different event types we run the following command `select distinct event_type from papers;`

To obtain the different event types with their respective frequency we run the following command `select event_type 'Event', count(event_type) 'Frequency' from papers group by event_type;`

To obtain the number of papers missing an abstract we run the following command `select abstract, count(abstract) 'Frequency' from papers where abstract = 'Abstract Missing';`

To select info from a table and save it into a file follow the instructions from this webpage: http://www.sqlitetutorial.net/sqlite-export-csv/
