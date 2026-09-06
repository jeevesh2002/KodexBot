import unittest
from collections.abc import Coroutine
from typing import Any

import bot


def _run_immediate(coroutine: Coroutine[Any, Any, Any]) -> None:
    """Drive handlers whose mocked awaits complete without an event loop."""

    try:
        yielded = coroutine.send(None)
    except StopIteration:
        return
    coroutine.close()
    raise AssertionError(f"handler unexpectedly suspended with {yielded!r}")


class _Author:
    def __init__(self, *, is_bot: bool = False) -> None:
        self.bot = is_bot


class _Channel:
    def __init__(self) -> None:
        self.messages: list[str] = []

    async def send(self, content: str) -> None:
        self.messages.append(content)


class _Message:
    def __init__(self, content: str, *, is_bot: bool = False) -> None:
        self.content = content
        self.author = _Author(is_bot=is_bot)
        self.channel = _Channel()


class BotCompatibilityTests(unittest.TestCase):
    def test_client_enables_message_content_intent(self) -> None:
        self.assertTrue(bot.client.intents.message_content)

    def test_bot_messages_are_ignored(self) -> None:
        message = _Message("spam 2 hello", is_bot=True)

        _run_immediate(bot.on_message(message))

        self.assertEqual(message.channel.messages, [])

    def test_spam_limit_is_preserved(self) -> None:
        message = _Message("spam 101 hello")

        _run_immediate(bot.on_message(message))

        self.assertEqual(message.channel.messages, ["Uh Uh max spam limit is capped at 100"])

    def test_spam_command_sends_requested_messages(self) -> None:
        message = _Message("spam 2 hello world")

        _run_immediate(bot.on_message(message))

        self.assertEqual(
            message.channel.messages,
            ["['hello', 'world']", "['hello', 'world']", "Succesfully spammed 2 times"],
        )


if __name__ == "__main__":
    unittest.main()
