"""Small local commands for validating the foundation."""

import argparse
import json
from dataclasses import asdict

from arvectum_data.acquisition.security import UnsafeURL

from dealforge.adapters.data_platform import DataPlatformDiscovery
from dealforge.settings import Settings


def main() -> int:
    parser = argparse.ArgumentParser(prog="dealforge")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health", help="Display local config and SDK connector health")
    discover = sub.add_parser("discover-url", help="Validate/discover a publicly accessible URL")
    discover.add_argument("url")
    args = parser.parse_args()

    if args.command == "health":
        cfg = Settings()
        payload = {
            "service": "dealforge",
            "bind": f"{cfg.host}:{cfg.port}",
            "connector": DataPlatformDiscovery().connector_health(),
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0

    try:
        items = DataPlatformDiscovery().discover_url(args.url)
    except UnsafeURL as exc:
        parser.exit(2, f"Rejected unsafe URL: {exc}\n")
    print(json.dumps([asdict(item) for item in items], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
