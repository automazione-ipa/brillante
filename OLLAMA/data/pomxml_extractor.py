import xml.etree.ElementTree as ET
from config import POM_FILE, MAVEN, MVN_GROUP_ID, MVN_ARTIFACT_ID, MVN_VERSION, MVN_DEP, MVN_PARENT


def parse_pom(pom=POM_FILE):
    """
    Analizza pom.xml, ritorna dict con:
      - project: {'groupId','artifactId','version'}
      - dependencies: [ {groupId, artifactId, version}, ... ]
    """
    ns = {'mvn': MAVEN}
    try:
        tree = ET.parse(pom)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        raise RuntimeError(f"Errore parsing '{pom}': {e}")

    # Estrai info progetto (eventuale parent fallback)
    proj = {}
    parent = root.find(MVN_PARENT, ns)
    for tag in ('groupId', 'artifactId', 'version'):
        el = root.find(
            f"mvn:{tag}", ns
        ) or (
            parent.find(f"mvn:{tag}", ns) if parent is not None else None
        )
        proj[tag] = el.text if el is not None else None

    # Estrai dipendenze
    deps = []
    for dep in root.findall(MVN_DEP, ns):
        gid = dep.find(MVN_GROUP_ID, ns)
        aid = dep.find(MVN_ARTIFACT_ID, ns)
        ver = dep.find(MVN_VERSION, ns)
        deps.append({
            'groupId': gid.text.strip() if gid is not None else '',
            'artifactId': aid.text.strip() if aid is not None else '',
            'version': ver.text.strip() if ver is not None else '',
        })

    return {'project': proj, 'dependencies': deps}
