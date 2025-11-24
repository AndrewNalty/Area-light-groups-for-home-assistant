# Automation Examples for Area Light Groups

This document provides examples of how to safely use Area Light Groups with Home Assistant automations.

## Safe Template Usage

When working with triggers that provide JSON payloads (such as MQTT triggers), it's important to safely access attributes that might not always be present.

### ❌ Incorrect - Unsafe Template

This template will cause errors if `payload_json` doesn't have an `action` key:

```yaml
trigger:
  - platform: mqtt
    topic: zigbee2mqtt/your_device/action
condition:
  - condition: template
    value_template: >-
      {{('hold' in trigger.payload_json.action) or 
        ('release' in trigger.payload_json.action) or 
        'press' in trigger.payload_json.action}}
```

**Problem**: This assumes `trigger.payload_json.action` always exists, which causes a template error when it doesn't.

### ✅ Correct - Safe Template with .get()

Use the `.get()` method with a default value to safely access potentially missing keys:

```yaml
trigger:
  - platform: mqtt
    topic: zigbee2mqtt/your_device/action
condition:
  - condition: template
    value_template: >-
      {% set action = trigger.payload_json.get('action', '') %}
      {{ 'hold' in action or 'release' in action or 'press' in action }}
```

### ✅ Alternative - Check Key Existence First

Another safe approach is to check if the key exists before accessing it:

```yaml
trigger:
  - platform: mqtt
    topic: zigbee2mqtt/your_device/action
condition:
  - condition: template
    value_template: >-
      {{ 'action' in trigger.payload_json and 
         ('hold' in trigger.payload_json.action or 
          'release' in trigger.payload_json.action or 
          'press' in trigger.payload_json.action) }}
```

### ✅ Most Robust - Multiple Safety Checks

For maximum safety, combine both approaches:

```yaml
trigger:
  - platform: mqtt
    topic: zigbee2mqtt/your_device/action
condition:
  - condition: template
    value_template: >-
      {% if trigger.payload_json is defined and 'action' in trigger.payload_json %}
        {% set action = trigger.payload_json.action %}
        {{ 'hold' in action or 'release' in action or 'press' in action }}
      {% else %}
        false
      {% endif %}
```

## Example: Control Area Lights with MQTT Button

Here's a complete example showing how to control area lights using an MQTT button device:

```yaml
automation:
  - alias: "Control Living Room Lights with Button"
    description: "Control area_living_room lights with button press types"
    trigger:
      - platform: mqtt
        topic: zigbee2mqtt/living_room_button/action
    condition:
      - condition: template
        value_template: >-
          {% set action = trigger.payload_json.get('action', '') %}
          {{ action in ['on', 'off', 'brightness_up', 'brightness_down'] }}
    action:
      - choose:
          - conditions:
              - condition: template
                value_template: >-
                  {{ trigger.payload_json.get('action') == 'on' }}
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.area_living_room
          - conditions:
              - condition: template
                value_template: >-
                  {{ trigger.payload_json.get('action') == 'off' }}
            sequence:
              - service: light.turn_off
                target:
                  entity_id: light.area_living_room
          - conditions:
              - condition: template
                value_template: >-
                  {{ trigger.payload_json.get('action') == 'brightness_up' }}
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.area_living_room
                data:
                  brightness_step_pct: 10
          - conditions:
              - condition: template
                value_template: >-
                  {{ trigger.payload_json.get('action') == 'brightness_down' }}
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.area_living_room
                data:
                  brightness_step_pct: -10
```

## Best Practices

1. **Always use `.get()` with default values** when accessing dictionary keys that might not exist
2. **Check for existence** with `'key' in dict` before accessing nested attributes
3. **Use `is defined`** to check if a variable exists in the template context
4. **Provide meaningful defaults** that make sense for your use case
5. **Test your templates** with both valid and invalid payloads to ensure robustness

## Common Patterns

### Checking Multiple Possible Actions

```yaml
value_template: >-
  {% set action = trigger.payload_json.get('action', '') %}
  {{ action in ['hold', 'release', 'press', 'single', 'double', 'triple'] }}
```

### Handling Different Payload Structures

```yaml
value_template: >-
  {% if 'action' in trigger.payload_json %}
    {{ trigger.payload_json.action }}
  {% elif 'command' in trigger.payload_json %}
    {{ trigger.payload_json.command }}
  {% else %}
    ''
  {% endif %}
```

### Combining Multiple Conditions Safely

```yaml
value_template: >-
  {% set payload = trigger.payload_json | default({}) %}
  {% set action = payload.get('action', '') %}
  {% set battery = payload.get('battery', 100) | int %}
  {{ action == 'on' and battery > 20 }}
```

## Troubleshooting

If you encounter template errors like:
- `'dict object' has no attribute 'action'`
- `UndefinedError: 'trigger' is undefined`
- `'NoneType' object has no attribute 'get'`

Make sure you're:
1. Using `.get()` method for dictionary access
2. Checking if variables are defined before using them
3. Providing appropriate default values
4. Testing your templates with various trigger conditions

## Additional Resources

- [Home Assistant Template Documentation](https://www.home-assistant.io/docs/configuration/templating/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [MQTT Trigger Documentation](https://www.home-assistant.io/docs/automation/trigger/#mqtt-trigger)
