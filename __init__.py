import logging
import sys
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

print("area_light_groups: Loading module", file=sys.stderr)
_LOGGER = logging.getLogger(__name__)
_LOGGER.critical("area_light_groups: Logger initialized")

DOMAIN = "area_light_groups"
PLATFORMS = [Platform.LIGHT]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Area Light Groups component."""
    _LOGGER.critical("Area Light Groups: async_setup called with config: %s", config)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Area Light Groups from a config entry."""
    _LOGGER.critical("Area Light Groups: async_setup_entry called for entry: %s", entry.entry_id)
    
    try:
        _LOGGER.critical("Area Light Groups: Starting platform setup")
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        _LOGGER.critical("Area Light Groups: Platform setup completed successfully")
        return True
    except Exception as e:
        _LOGGER.critical("Area Light Groups: Platform setup failed with exception: %s", str(e), exc_info=True)
        # Raise the exception to make it visible in HA logs
        raise

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.critical("Area Light Groups: async_unload_entry called")
    try:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        _LOGGER.critical("Area Light Groups: Unload successful: %s", unload_ok)
        return unload_ok
    except Exception as e:
        _LOGGER.critical("Area Light Groups: Unload failed with exception: %s", str(e), exc_info=True)
        raise