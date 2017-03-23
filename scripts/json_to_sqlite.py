import json
import records

db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")

r = json.loads(open('/home/hunter/orkohunter.net/database/depends/packages.json', 'r').read())

query = "INSERT INTO packages (package, builtins, nonbuiltins, file_type, source, version) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"

index = 0
for package_name in r:
    index += 1
    builtins = r[package_name]['builtins']
    nonbuiltins = r[package_name]['nonbuiltins']
    file_type = r[package_name]['file_type']
    source = r[package_name]['source']
    version = r[package_name]['version']
    escape_characters = ['\'', '"', '\n', '\\']
    for char in escape_characters:
        builtins = builtins.replace(char, "")
        nonbuiltins = nonbuiltins.replace(char, "")
        file_type = file_type.replace(char, "")
        source = source.replace(char, "")
        version = version.replace(char, "")
    query_formatted = query.format(json.dumps(package_name), json.dumps(builtins), json.dumps(nonbuiltins), json.dumps(file_type), json.dumps(source), json.dumps(version))
    db.query(query_formatted)
