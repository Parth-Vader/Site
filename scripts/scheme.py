import records

db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")

db.query("CREATE TABLE packages ("
         "package VARCHAR (100), "
         "builtins VARCHAR (100000), "
         "nonbuiltins VARCHAR (100000), "
         "file_type VARCHAR (10), "
         "source VARCHAR (50), "
         "version VARCHAR (10));")
