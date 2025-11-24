# Area Light Groups for Home Assistant

Creates light groups and entities for each group, based on the area lights are in.

## Installation

Create a folder called `area_light_groups` in your Home Assistant `custom_components` directory and include these files.

## Configuration

After installation, add the integration through the Home Assistant UI:
1. Go to Settings -> Devices & Services
2. Click "+ Add Integration"
3. Search for "Area Light Groups"
4. Configure the options:
   - **Include empty areas**: Whether to create groups for areas with no lights
   - **Prefix**: The prefix to use for entity names (default: `area_`)

## Usage

Once configured, the integration will create a light entity for each area in your Home Assistant setup. For example, if you have a "Living Room" area with lights, it will create an entity named `light.area_living_room`.

These area light groups behave like regular light entities and can be:
- Controlled through the UI
- Used in automations
- Controlled via voice assistants
- Integrated with other Home Assistant features

## Automation Examples

For examples of how to safely use Area Light Groups in automations, especially with MQTT triggers and template conditions, see [AUTOMATION_EXAMPLES.md](AUTOMATION_EXAMPLES.md).

**Important**: When using templates that access trigger payloads, always use safe attribute access patterns (see the automation examples) to avoid template errors.
