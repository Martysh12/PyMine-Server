# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Contains packets related to items."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayUseItem",
    "PlayEditBook",
    "PlayPickItem",
    "PlayNameItem",
    "PlayHeldItemChangeServerBound",
    "PlayHeldItemChangeClientBound",
    "PlayCollectItem",
)


class PlayUseItem(Packet):
    """Sent by the client when the use item key is pressed. (Client -> Server)

    :param int hand: The hand used for the animation. main hand (0) or offhand (1).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar hand:
    """

    id = 0x2F
    to = 0

    def __init__(self, hand: int) -> None:
        super().__init__()

        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUseItem:
        return cls(buf.upack_varint())


class PlayEditBook(Packet):
    """Used by the client to edit a book. (Client -> Server)

    :param dict new_book: The new slot/data for the book.
    :param bool is_signing: Whether the player is signing the book or just saving a draft.
    :param int hand: The hand used. Either main hand (0) or offhand (1).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar new_book:
    :ivar is_signing:
    :ivar hand:
    """

    id = 0x0C
    to = 0

    def __init__(self, new_book: dict, is_signing: bool, hand: int) -> None:
        super().__init__()

        self.new_book = new_book
        self.is_signing = is_signing
        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayEditBook:
        return cls(buf.unpack_slot(), buf.unpack("?"), buf.unpack_varint())


class PlayPickItem(Packet):
    """Used to swap out an empty space on the hotbar with the item in the given inventory slot. (Client -> Server)

    :param int slot_to_use: The slot to use.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar slot_to_use:
    """

    id = 0x18
    to = 0

    def __init__(self, slot_to_use: int) -> None:
        super().__init__()

        self.slot_to_use = slot_to_use

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPickItem:
        return cls(buf.unpack_varint())


class PlayNameItem(Packet):
    """Used by the client when renaming something in an anvil. (Client -> Server)

    :param str item_name: The new name of the item.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar item_name:
    """

    id = 0x20
    to = 0

    def __init__(self, item_name: str) -> None:
        super().__init__()

        self.item_name = item_name

    @classmethod
    def decode(cls, buf: Buffer) -> PlayNameItem:
        return cls(buf.unpack_string())


class PlayHeldItemChangeServerBound(Packet):
    """Sent when the player selects a new slot. (Client -> Server)

    :param int slot: The new selected slot.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar slot:
    """

    id = 0x25
    to = 0

    def __init__(self, slot: int) -> None:
        super().__init__()

        self.slot = slot

    @classmethod
    def decode(cls, buf: Buffer) -> PlayHeldItemChangeServerBound:
        return cls(buf.unpack("h"))


class PlayHeldItemChangeClientBound(Packet):
    """Sent to change the player's slot selection. (Server -> Client)

    :param int slot: The slot which the player has selected (0–8).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar slot:
    """

    id = 0x3F
    to = 1

    def __init__(self, slot: int) -> None:
        super().__init__()

        self.slot = slot

    def encode(self) -> bytes:
        return Buffer.pack("b", self.slot)


class PlayCollectItem(Packet):
    """Sent by the server when someone picks up an item lying on the ground. (Server -> Client)

    :param int collected_eid: The Entity ID of the entity that gets collected.
    :param int collector_eid: The Entity ID of the entity that collects.
    :param int item_count: 1 for XP orbs, otherwise the number of items in the stack.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar collected_eid:
    :ivar collector_eid:
    :ivar item_count:
    """

    id = 0x55
    to = 1

    def __init__(self, collected_eid: int, collector_eid: int, item_count: int) -> None:
        super().__init__()

        self.collected_eid = collected_eid
        self.collector_eid = collector_eid
        self.item_count = item_count

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.collected_eid)
            + Buffer.pack_varint(self.collector_eid)
            + Buffer.pack_varint(self.item_count)
        )
