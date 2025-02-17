"""Provides device actions for Button."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.device_automation import async_validate_entity_schema
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_TYPE,
)
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_registry as er
from homeassistant.helpers.typing import ConfigType, TemplateVarsType

from .const import DOMAIN, SERVICE_PRESS

ACTION_TYPES = {"press"}

_ACTION_SCHEMA = cv.DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(ACTION_TYPES),
        vol.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
    }
)


async def async_validate_action_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return async_validate_entity_schema(hass, config, _ACTION_SCHEMA)


async def async_get_actions(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device actions for button devices."""
    registry = er.async_get(hass)
    return [
        {
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_ENTITY_ID: entry.id,
            CONF_TYPE: "press",
        }
        for entry in er.async_entries_for_device(registry, device_id)
        if entry.domain == DOMAIN
    ]


async def async_call_action_from_config(
    hass: HomeAssistant,
    config: ConfigType,
    variables: TemplateVarsType,
    context: Context | None,
) -> None:
    """Execute a device action."""
    await hass.services.async_call(
        DOMAIN,
        SERVICE_PRESS,
        {
            ATTR_ENTITY_ID: config[CONF_ENTITY_ID],
        },
        blocking=True,
        context=context,
    )
