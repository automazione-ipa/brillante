import json

POM_FILE = '../pom.xml'
TXT_REPORT = 'alerts.txt'
RECIPIENTS = ['alessandrobrillante78@gmail.com', 'lucasalzone@gmail.com']
NVD_URL = 'https://nvd.nist.gov/vuln/search'

# Maven Constants
MAVEN = 'http://maven.apache.org/POM/4.0.0'
MVN_GROUP_ID = 'mvn:groupId'
MVN_ARTIFACT_ID = 'mvn:artifactId'
MVN_VERSION = 'mvn:version'
MVN_PARENT = 'mvn:parent'
MVN_DEP = './/mvn:dependency'


def write_alerts(alerts):
    with open(TXT_REPORT, 'w') as f:
        f.write('\n'.join(alerts))


def write_pom_json(result, json_path="pom_info.json"):
    """Save result to JSON file"""
    with open(json_path, "w") as f:
        json.dump(result, f, indent=4)
    return result, json_path
