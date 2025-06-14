from pomxml_extractor import parse_pom
from config import POM_FILE


def main():
    try:
        data = parse_pom(pom_path=POM_FILE)
    except RuntimeError as e:
        print(f"Errore: {e}")
        return

    proj = data['project']
    print("📦 Informazioni sul progetto:")
    print(f"  - groupId:    {proj.get('groupId')}")
    print(f"  - artifactId: {proj.get('artifactId')}")
    print(f"  - version:    {proj.get('version')}")
    print("\n📄 Dipendenze rilevate:")
    for d in data['dependencies']:
        print(f"  • {d['groupId']}:{d['artifactId']}:{d['version']}")


if __name__ == "__main__":
    main()
    # asyncio.run(main_v2())
