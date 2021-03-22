import asyncio
from pymine.net.packets.login.login import LoginSuccess
from pymine.net.packets.play.player import PlayJoinGame

from pymine.api.events import PacketEvent, ServerStartEvent, ServerStopEvent
from pymine.types.abc import AbstractWorldGenerator, AbstractPlugin

from pymine.data.states import STATES


class Register:
    def __init__(self) -> None:
        self._generators = {}  # world generators {name: object}

        # handshaking, login, play, status
        # (state, state, state, state)
        # {packet_id: {plugin_quali_name: event_object}}
        self._on_packet = ({}, {}, {}, {})

        # other/generic events, {plugin_quali_name: event_object}
        self._on_server_start = {}
        self._on_server_stop = {}

    def add_world_generator(self, name: str):
        def deco(cls):
            if not issubclass(cls, AbstractWorldGenerator):
                raise ValueError(f"Decorated class must be a subclass of AbstractWorldGenerator")

            self._generators[name] = cls

            return cls

        return deco

    def on_packet(self, state: str, packet_id: int):
        state_id = STATES.encode(state)

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function.")

            if hasattr(func, "__self__"):  # is a method of a class, so prob in a plugin class cog
                return PacketEvent(func, state_id, packet_id)

            # If we're here, this is probably a packet handler under logic/handle, so we need to account for that
            try:
                self._on_packet[state_id][packet_id][f"{func.__module__}.{func.__qualname__}"] = func
            except KeyError:
                self._on_packet[state_id][packet_id] = {f"{func.__module__}.{func.__qualname__}": func}

            return func

        return deco

    def on_login_success(self, func):
        return PacketEvent(func, STATES.encode("login"), LoginSuccess.id)

    def on_join(self, func):
        return PacketEvent(func, STATES.encode("play"), PlayJoinGame.id)

    def on_server_start(self, func):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Decorated object must be a coroutine function.")

        return ServerStartEvent(func)

    def on_server_stop(self, func):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Decorated object must be a coroutine function.")

        return ServerStopEvent(func)
