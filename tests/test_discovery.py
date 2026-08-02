from pathlib import Path

from pyloninsight.discovery import discover_campaign


campaign = discover_campaign(
   Path("tests/data/real/2026-07-13_SOC100")
#  Path("tests/data/minimal/campaign")

)

print()

print(f"Campaign : {campaign.name}")
print(f"Exports  : {len(campaign.exports)}")

print()

for export in campaign.exports:

    print(export.role)

    print(f"    History : {export.files.has_history}")
    print(f"    Events  : {export.files.has_events}")
    print(f"    Scanlog : {export.files.has_scanlog}")

    print()