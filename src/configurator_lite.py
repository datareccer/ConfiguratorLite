import json
import yaml
from pathlib import Path
from rich import print
import click
from jsonschema import validate, ValidationError
import datetime

APP_NAME = "Configurator Lite"
APP_VERSION = "1.1.0"
BUILD_DATE = "2025-12-17"

BASE_DIR = Path(__file__).parent.parent
SCHEMA_PATH = BASE_DIR / "schemas" / "config.schema.json"
LITE_SCHEMA_PATH = BASE_DIR / "schemas" / "lite.schema.json"
DIST_DIR = BASE_DIR / "dist"


# -------------------------
# Schema Loading & Validation
# -------------------------

def load_schema(path: Path):
    return json.loads(path.read_text())


def validate_with_schema(data, schema_path):
    try:
        validate(instance=data, schema=load_schema(schema_path))
    except ValidationError as e:
        print("[red]Configuration validation failed:[/red]")
        print(e.message)
        raise SystemExit(1)


def enforce_lite_contract(data):
    schema = load_schema(LITE_SCHEMA_PATH)

    for key, rule in schema.items():
        if key not in data:
            die(f"Missing required key: {key}")

        if rule == "string" and not isinstance(data[key], str):
            die(f"{key} must be a string")

        if rule == "boolean" and not isinstance(data[key], bool):
            die(f"{key} must be a boolean")

        if isinstance(rule, list) and data[key] not in rule:
            die(f"{key} must be one of {rule}")


def die(msg):
    print(f"[red]ERROR:[/red] {msg}")
    raise SystemExit(1)


# -------------------------
# CLI
# -------------------------

@click.command()
@click.argument("config", required=False)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.option("--init", is_flag=True, help="Create a default config.yaml")
def run(config, version, init):
    if version:
        print(f"{APP_NAME} v{APP_VERSION} ({BUILD_DATE})")
        return

    if init:
        default = {
            "name": "example",
            "mode": "lite",
            "enabled": True
        }
        Path("config.yaml").write_text(yaml.dump(default))
        print("[green]Created config.yaml[/green]")
        return

    if not config:
        print("[yellow]No config file provided[/yellow]")
        return

    p = Path(config)
    if not p.exists():
        die("Config file not found")

    if p.suffix in [".yml", ".yaml"]:
        data = yaml.safe_load(p.read_text())
    elif p.suffix == ".json":
        data = json.loads(p.read_text())
    else:
        die("Unsupported config format")

    # Base schema validation
    validate_with_schema(data, SCHEMA_PATH)

    # Lite contract enforcement
    enforce_lite_contract(data)

    print(f"[cyan]{APP_NAME} v{APP_VERSION}[/cyan]")
    print("[green]Configurator Lite Output[/green]")
    print(data)

    # -------------------------
    # Bundle Output
    # -------------------------

    DIST_DIR.mkdir(exist_ok=True)

    bundle = {
        "tool": APP_NAME,
        "version": APP_VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "config": data
    }

    bundle_path = DIST_DIR / f"bundle-{data.get('name','unnamed')}.json"
    bundle_path.write_text(json.dumps(bundle, indent=2))

    print(f"[green]Bundle written to[/green] {bundle_path}")


if __name__ == "__main__":
    run()
