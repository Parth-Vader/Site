import json
from handlers import depends_engine


def index():
    with open('database/depends/packages.json', 'r') as f:
        packages = json.loads(f.read())
    with open('database/depends/last_package', 'r') as f:
        last_package = f.read()

    data = {
        'no_of_packages': len(packages),
        'last_package': last_package,
        }

    return data


def package_view(package):
    with open('database/depends/packages.json', 'r') as f:
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
            with open('database/depends/packages.json', 'w') as f:
                f.write(json.dumps(packages))
            with open('database/depends/last_package', 'w') as f:
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
    with open('database/depends/packages.json', 'r') as f:
        packages = json.loads(f.read())

    del packages[package]

    with open('database/depends/packages.json', 'w') as f:
        f.write(json.dumps(packages))


def list():
    with open('database/depends/packages.json', 'r') as f:
        packages = json.loads(f.read())

    data = {
        'packages': sorted(packages.keys()),
        }

    return data
