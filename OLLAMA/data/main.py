from pomxml_extractor import parse_pom
from config import POM_FILE, write_pom_json


def main():
    try:
        data = parse_pom(pom_path=POM_FILE)
    except RuntimeError as e:
        print(f"❌ Errore: {e}")
        return

    _, json_path = write_pom_json(data)

    proj = data['project']
    print("📦 Informazioni sul progetto:")
    print(f"  - groupId:    {proj.get('groupId')}")
    print(f"  - artifactId: {proj.get('artifactId')}")
    print(f"  - version:    {proj.get('version')}")
    print(f"📁 File JSON salvato in: {json_path}")

    print("\n📄 Dipendenze rilevate:")
    for d in data['dependencies']:
        print(f"  • {d['groupId']}:{d['artifactId']}:{d['version']}")


if __name__ == "__main__":
    main()
