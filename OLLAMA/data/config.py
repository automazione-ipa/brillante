"""Modulo di configurazione e caricamento file in memoria."""

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

