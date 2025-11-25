import logging
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ATTR_RGB_COLOR,
    ATTR_RGBW_COLOR,
    ATTR_RGBWW_COLOR,
    ATTR_TRANSITION,
    ATTR_WHITE,
    ATTR_XY_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er, area_registry as ar, device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up area light groups."""
    _LOGGER.critical("Setting up Area Light Groups platform")
    
    entity_reg = er.async_get(hass)
    device_reg = dr.async_get(hass)
    area_reg = ar.async_get(hass)
    
    include_empty = config_entry.data.get("include_empty_areas", False)
    prefix = config_entry.data.get("prefix", "area_")
    
    _LOGGER.critical(
        "Configuration: include_empty_areas=%s, prefix=%s",
        include_empty,
        prefix
    )
    
    # Log all areas
    _LOGGER.critical("Found %d area(s) in registry", len(area_reg.areas))
    for area in area_reg.areas.values():
        _LOGGER.critical("Area found: %s (ID: %s)", area.name, area.id)

    # Get all light entities
    light_entities = {
        entity_id: entity
        for entity_id, entity in entity_reg.entities.items()
        if entity_id.startswith("light.") and not entity.disabled
    }
    
    _LOGGER.critical("Found %d light entities", len(light_entities))
    
    # Create a mapping of areas to their light entities
    area_lights = {area.id: [] for area in area_reg.areas.values()}
    
    for entity_id, entity in light_entities.items():
        # Get device_id from entity
        device_id = entity.device_id
        if device_id:
            # Get device from device registry
            device = device_reg.async_get(device_id)
            if device and device.area_id:
                _LOGGER.critical(
                    "Light: %s, Device: %s, Area ID: %s",
                    entity_id,
                    device_id,
                    device.area_id
                )
                area_lights[device.area_id].append(entity_id)
    
    # Create groups for each area
    groups = []
    
    for area in area_reg.areas.values():
        area_light_entities = area_lights.get(area.id, [])
        
        _LOGGER.critical(
            "Area '%s' (ID: %s) has %d light(s): %s",
            area.name,
            area.id,
            len(area_light_entities),
            area_light_entities
        )
        
        if area_light_entities or include_empty:
            groups.append(
                AreaLightGroup(
                    hass,
                    area.name,
                    area.id,
                    area_light_entities,
                    prefix
                )
            )
            _LOGGER.critical(
                "Created light group for area '%s' with %d light(s)",
                area.name,
                len(area_light_entities)
            )
        else:
            _LOGGER.critical(
                "Skipping area '%s' (no lights and include_empty_areas=False)",
                area.name
            )
    
    _LOGGER.critical("Created %d area light group(s)", len(groups))
    async_add_entities(groups)


class AreaLightGroup(LightEntity):
    """Representation of a light group tied to an area."""

    def __init__(self, hass, name, area_id, light_entities, prefix):
        """Initialize the area light group."""
        self.hass = hass
        self._name = f"{prefix}{name}"
        self._area_id = area_id
        self._light_entities = light_entities
        self._is_on = False
        self._brightness = None

    @property
    def name(self):
        """Return the name of the light group.""" 
        return self._name

    @property
    def is_on(self):
        """Return if the light group is on.""" 
        return self._is_on

    @property
    def brightness(self):
        """Return the brightness of the light group.""" 
        return self._brightness

    @property
    def supported_color_modes(self):
        """Return the supported color modes for the group."""
        # Assuming the lights in the group support brightness control.
        # This can be updated based on your target lights' capabilities.
        return {ColorMode.BRIGHTNESS}

    @property
    def color_mode(self):
        """Return the current color mode of the group."""
        # Assuming the group works in brightness mode only.
        # This can be expanded based on the group setup.
        return ColorMode.BRIGHTNESS

    async def async_turn_on(self, **kwargs):
        """Turn on all lights in the group.""" 
        _LOGGER.debug("Turning on light group %s", self._name)
        self._is_on = True
        for light in self._light_entities:
            await self.hass.services.async_call(
                "light", "turn_on", {"entity_id": light, **kwargs}
            )

    async def async_turn_off(self, **kwargs):
        """Turn off all lights in the group.""" 
        _LOGGER.debug("Turning off light group %s", self._name)
        self._is_on = False
        for light in self._light_entities:
            await self.hass.services.async_call(
                "light", "turn_off", {"entity_id": light, **kwargs}
            )

    async def async_update(self):
        """Fetch state of the group.""" 
        _LOGGER.debug("Updating state for light group %s", self._name)
        states = [
            self.hass.states.get(entity_id) for entity_id in self._light_entities
        ]
        self._is_on = any(state.state == STATE_ON for state in states)
        brightness_values = [
            state.attributes.get(ATTR_BRIGHTNESS) 
            for state in states 
            if state and state.attributes.get(ATTR_BRIGHTNESS) is not None
        ]
        self._brightness = max(brightness_values) if brightness_values else None