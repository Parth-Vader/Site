import json
import os
import records
from handlers import depends_engine

DATABASE_DIR = os.path.expanduser('~') + '/orkohunter.net/database/'


def index():
    db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")
    rows = db.query('SELECT * FROM packages')
    with open(DATABASE_DIR + 'depends/last_package', 'r') as f:
        last_package = f.read()

    data = {
        'no_of_packages': len(rows.all()),
        'last_package': last_package,
    }

    return data


def package_view(package):
    db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")
    rows = db.query("SELECT * FROM packages WHERE package='{}'".format(package))

    analysis_exists = False
    data = {'package_name': package}
    try:
        if len(rows.all()) == 1:
            analysis_exists = True
            p = rows[0]
        else:
            analysis = depends_engine.main(package)
            p = {}
            p["builtins"] = " ".join(analysis["builtins"].keys())
            p["nonbuiltins"] = " ".join(analysis["nonbuiltins"].keys())
            p["version"] = analysis["info"]["version"]
            p["file_type"] = analysis["info"]["file_type"]
            p["source"] = analysis["info"]["source"]

            query = "INSERT INTO packages (package, builtins, nonbuiltins, file_type, source, version) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"
            query_formatted = query.format(json.dumps(package), json.dumps(p['builtins']), json.dumps(p['nonbuiltins']), json.dumps(p['file_type']), json.dumps(p['source']), json.dumps(p['version']))
            query_formatted = query_formatted.replace("\"", "")
            db.query(query_formatted)
            with open(DATABASE_DIR + 'depends/last_package', 'w') as f:
                f.write(package)
            analysis_exists = True

        data['builtins'] = p["builtins"].split()
        data['nonbuiltins'] = p["nonbuiltins"].split()
        data['version'] = p["version"]
        data['file_type'] = p["file_type"]
        data['source'] = p["source"]
    except Exception as e:
        data['reason'] = e

    return analysis_exists, data


def package_refresh(package):
    db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")
    db.query("DELETE FROM packages WHERE package='{}'".format(package))


def list():
    db = records.Database("sqlite:////home/hunter/orkohunter.net/database/depends/packages.db")
    rows = db.query('SELECT * FROM packages ORDER BY package')

    data = {
        'packages': [r.package for r in rows.all()],
    }

    return data
