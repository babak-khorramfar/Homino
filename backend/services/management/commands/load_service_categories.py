from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import ServiceCategory


class Command(BaseCommand):
    help = "Load technical service categories with icons"

    def handle(self, *args, **options):
        self.stdout.write("⏳ Creating service categories...")

        def create_category(title, parent=None, icon=None):
            base_slug = slugify(title)
            slug = base_slug
            index = 1
            while ServiceCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{index}"
                index += 1

            obj, created = ServiceCategory.objects.get_or_create(
                title=title, parent=parent, defaults={"slug": slug, "icon": icon}
            )
            return obj

        category_data = [
            (
                "Electricity",
                "fa-bolt",
                [
                    "Wiring",
                    "Switches and Fuses",
                    "Solar Panel",
                    "Lighting",
                    "Power Troubleshooting",
                ],
            ),
            (
                "Plumbing",
                "fa-faucet",
                [
                    "Drain Replacement",
                    "Toilet and Flush Tank",
                    "Pipe Descaling",
                    "Appliance Plumbing",
                    "Odor Removal",
                ],
            ),
            (
                "Cooling",
                "fa-snowflake",
                [
                    "AC Installation",
                    "Evaporative Cooler Service",
                    "Pump or Belt Replacement",
                    "Ventilation",
                ],
            ),
            (
                "Heating",
                "fa-fire",
                [
                    "Heater or Fireplace",
                    "Smart Thermostat",
                    "Radiator Insulation",
                    "Boiler Pressure",
                ],
            ),
            (
                "Minor Repairs",
                "fa-tools",
                [
                    "Lock and Hinge Repair",
                    "Door/Window Alignment",
                    "Install Bathroom Fixtures",
                ],
            ),
            (
                "Doors & Shutters",
                "fa-door-closed",
                ["Shutter Motor", "Electric Glass Door"],
            ),
            ("Safety", "fa-shield-alt", ["Fire Alarm", "Extinguisher Refill"]),
            (
                "Digital Equipment",
                "fa-plug",
                ["Central Antenna", "Home Network", "Alarm System"],
            ),
            (
                "Other Services",
                "fa-cogs",
                [
                    "Remote Control Setup",
                    "Building Maintenance",
                    "Office Support",
                    "Electric Curtains",
                ],
            ),
        ]

        for parent_title, icon, children in category_data:
            parent = create_category(parent_title, icon=icon)
            for child in children:
                create_category(child, parent=parent)

        self.stdout.write("✅ Service categories created successfully.")
