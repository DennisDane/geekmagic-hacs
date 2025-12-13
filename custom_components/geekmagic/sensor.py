"""Sensor platform for GeekMagic integration.

This module re-exports from entities submodule for Home Assistant platform discovery.
"""

from .entities.sensor import async_setup_entry

__all__ = ["async_setup_entry"]
