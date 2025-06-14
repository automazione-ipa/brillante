import xml.etree.ElementTree as ET
import json

def parse_pom(pom_path):
    tree = ET.parse(pom_path)
    root = tree.getroot()

    # Define namespace
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

    # Extract project information
    artifact_id = root.find('m:artifactId', ns).text
    version = root.find('m:version', ns).text
    group_id = root.find('m:groupId', ns).text
    packaging = root.find('m:packaging', ns).text if root.find('m:packaging', ns) is not None else "jar"

    project_info = {
        'groupId': group_id,
        'artifactId': artifact_id,
        'version': version,
        'packaging': packaging
    }

    # Extract dependencies
    dependencies = []
    for dep in root.findall('.//m:dependency', ns):
        dep_info = {
            'groupId': dep.find('m:groupId', ns).text,
            'artifactId': dep.find('m:artifactId', ns).text,
            'version': dep.find('m:version', ns).text if dep.find('m:version', ns) is not None else "",
            'scope': dep.find('m:scope', ns).text if dep.find('m:scope', ns) is not None else "compile"
        }
        dependencies.append(dep_info)

    return {
        'project': project_info,
        'dependencies': dependencies
    }
