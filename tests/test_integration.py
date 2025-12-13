"""Integration tests for GeekMagic."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.geekmagic import async_setup_entry, async_unload_entry
from custom_components.geekmagic.const import DOMAIN


class TestIntegrationSetup:
    """Test integration setup and teardown."""

    @pytest.fixture
    def mock_hass(self):
        """Create mock Home Assistant."""
        hass = MagicMock()
        hass.data = {}
        hass.services = MagicMock()
        hass.services.has_service.return_value = False
        hass.services.async_register = MagicMock()
        hass.config_entries = MagicMock()
        hass.config_entries.async_forward_entry_setups = AsyncMock()
        return hass

    @pytest.fixture
    def mock_entry(self):
        """Create mock config entry."""
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
        entry.data = {"host": "192.168.1.100", "name": "Test Display"}
        entry.options = {}
        entry.add_update_listener = MagicMock(return_value=MagicMock())
        entry.async_on_unload = MagicMock()
        return entry

    @pytest.mark.asyncio
    async def test_setup_entry_connection_failure(self, mock_hass, mock_entry):
        """Test setup handles connection failure gracefully."""
        with patch("custom_components.geekmagic.async_get_clientsession") as mock_session:
            mock_session.return_value = MagicMock()

            with patch("custom_components.geekmagic.GeekMagicDevice") as mock_device_class:
                mock_device = MagicMock()
                mock_device.test_connection = AsyncMock(return_value=False)
                mock_device_class.return_value = mock_device

                result = await async_setup_entry(mock_hass, mock_entry)

                assert result is False
                mock_device.test_connection.assert_called_once()

    @pytest.mark.asyncio
    async def test_setup_entry_success(self, mock_hass, mock_entry):
        """Test successful setup creates coordinator and registers services."""
        with patch("custom_components.geekmagic.async_get_clientsession") as mock_session:
            mock_session.return_value = MagicMock()

            with patch("custom_components.geekmagic.GeekMagicDevice") as mock_device_class:
                mock_device = MagicMock()
                mock_device.test_connection = AsyncMock(return_value=True)
                mock_device_class.return_value = mock_device

                with patch(
                    "custom_components.geekmagic.GeekMagicCoordinator"
                ) as mock_coordinator_class:
                    mock_coordinator = MagicMock()
                    mock_coordinator.async_config_entry_first_refresh = AsyncMock()
                    mock_coordinator_class.return_value = mock_coordinator

                    result = await async_setup_entry(mock_hass, mock_entry)

                    assert result is True
                    assert DOMAIN in mock_hass.data
                    assert mock_entry.entry_id in mock_hass.data[DOMAIN]


class TestIntegrationUnload:
    """Test integration unload."""

    @pytest.fixture
    def mock_hass_with_data(self):
        """Create mock Home Assistant with existing data."""
        hass = MagicMock()
        hass.data = {DOMAIN: {"test_entry_123": MagicMock()}}
        hass.config_entries = MagicMock()
        hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
        return hass

    @pytest.fixture
    def mock_entry(self):
        """Create mock config entry."""
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
        entry.data = {"host": "192.168.1.100", "name": "Test Display"}
        return entry

    @pytest.mark.asyncio
    async def test_unload_entry_success(self, mock_hass_with_data, mock_entry):
        """Test successful unload removes coordinator."""
        result = await async_unload_entry(mock_hass_with_data, mock_entry)

        assert result is True
        assert mock_entry.entry_id not in mock_hass_with_data.data[DOMAIN]

    @pytest.mark.asyncio
    async def test_unload_entry_failure(self, mock_hass_with_data, mock_entry):
        """Test failed unload keeps coordinator."""
        mock_hass_with_data.config_entries.async_unload_platforms = AsyncMock(return_value=False)

        result = await async_unload_entry(mock_hass_with_data, mock_entry)

        assert result is False
        # Coordinator should still be present on failure
        assert mock_entry.entry_id in mock_hass_with_data.data[DOMAIN]


class TestServiceRegistration:
    """Test service registration."""

    @pytest.fixture
    def mock_hass(self):
        """Create mock Home Assistant."""
        hass = MagicMock()
        hass.data = {DOMAIN: {}}
        hass.services = MagicMock()
        hass.services.has_service.return_value = False
        hass.services.async_register = MagicMock()
        return hass

    @pytest.mark.asyncio
    async def test_services_registered(self, mock_hass):
        """Test all services are registered."""
        from custom_components.geekmagic import async_setup_services

        await async_setup_services(mock_hass)

        # Check that services were registered
        assert mock_hass.services.async_register.call_count == 5
        service_names = [call[0][1] for call in mock_hass.services.async_register.call_args_list]
        assert "refresh" in service_names
        assert "brightness" in service_names
        assert "set_screen" in service_names
        assert "next_screen" in service_names
        assert "previous_screen" in service_names

    @pytest.mark.asyncio
    async def test_services_not_duplicated(self, mock_hass):
        """Test services are not registered twice."""
        from custom_components.geekmagic import async_setup_services

        # First call registers services
        await async_setup_services(mock_hass)
        first_count = mock_hass.services.async_register.call_count

        # Second call should skip registration
        mock_hass.services.has_service.return_value = True
        await async_setup_services(mock_hass)
        second_count = mock_hass.services.async_register.call_count

        # Count should not increase
        assert first_count == second_count
