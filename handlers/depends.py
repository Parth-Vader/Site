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
    with open(DATABASE_DIR + 'depends/packages.json', 'r') as f:
        packages = json.loads(f.read())

    analysis_exists = False
    data = {'package_name': package}
    try:
        if package in packages:
            analysis_exists = True
            p = packages[package]
        else:
            analysis = depends_engine.main(package)
            p = {}
            p["builtins"] = " ".join(analysis["builtins"].keys())
            p["nonbuiltins"] = " ".join(analysis["nonbuiltins"].keys())
            p["version"] = analysis["info"]["version"]
            p["file_type"] = analysis["info"]["file_type"]
            p["source"] = analysis["info"]["source"]
            packages[package] = p
            with open(DATABASE_DIR + 'depends/packages.json', 'w') as f:
                f.write(json.dumps(packages))
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
    with open(DATABASE_DIR + 'depends/packages.json', 'r') as f:
        packages = json.loads(f.read())

    del packages[package]

    with open(DATABASE_DIR + 'depends/packages.json', 'w') as f:
        f.write(json.dumps(packages))


def list():
    with open(DATABASE_DIR + 'depends/packages.json', 'r') as f:
        packages = json.loads(f.read())

    data = {
        'packages': sorted(packages.keys()),
    }

    return data
