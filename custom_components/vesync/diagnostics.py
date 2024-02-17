"""Provides diagnostics for VeSync."""
from __future__ import annotations
import logging

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .common import is_humidifier
from .const import DOMAIN

TO_REDACT = {"cid", "uuid", "mac_id"}
_LOGGER = logging.getLogger(__name__)

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    devices = {}
    _LOGGER.warning(
        "Configuring with the following data: %s",
        data,
    )
    for type in ["fans", "outlets", "switches", "bulbs"]:
        for d in data["manager"]._dev_list[type]:
            t = "humidifier" if is_humidifier(d.device_type) else type
            devices = {
                **devices,
                **{t: [{k: v for k, v in d.__dict__.items() if k != "manager"}]},
            }

    for type in ["fans", "outlets", "switches", "bulbs"]:
        for d in data["manager"]._dev_list[type]:
            t = "humidifier" if is_humidifier(d.device_type) else type
            devices = {
                **devices,
                **{t: [{k: v for k, v in d.__dict__.items() if k != "manager"}]},
            }
    return async_redact_data(devices, TO_REDACT)
