"""Support for Overkiz locks."""

from __future__ import annotations

from typing import Any

from pyoverkiz.enums import OverkizCommand, OverkizCommandParam, OverkizState

from homeassistant.components.lock import LockEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import OverkizDataConfigEntry
from .entity import OverkizEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OverkizDataConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Overkiz locks from a config entry."""
    data = entry.runtime_data

    async_add_entities(
        OverkizLock(device.device_url, data.coordinator)
        for device in data.platforms[Platform.LOCK]
    )


class OverkizLock(OverkizEntity, LockEntity):
    """Representation of an Overkiz Lock."""

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock method."""
        await self.executor.async_execute_command(OverkizCommand.LOCK)

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock method."""
        await self.executor.async_execute_command(OverkizCommand.UNLOCK)

    @property
    def is_locked(self) -> bool | None:
        """Return a boolean for the state of the lock."""
        return (
            self.executor.select_state(OverkizState.CORE_LOCKED_UNLOCKED)
            == OverkizCommandParam.LOCKED
        )
