import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "area_light_groups"

class AreaLightGroupsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Area Light Groups."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.critical("Config Flow: async_step_user called with input: %s", user_input)
        
        if user_input is not None:
            _LOGGER.critical("Config Flow: Creating entry with data: %s", user_input)
            return self.async_create_entry(
                title="Area Light Groups",
                data=user_input
            )

        _LOGGER.critical("Config Flow: Showing configuration form")
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional("include_empty_areas", default=False): bool,
                vol.Optional("prefix", default="area_"): str,
            })
        )