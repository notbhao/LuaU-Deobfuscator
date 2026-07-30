import re


class Replacer:

    def __init__(self, source: str, strings: list[str]):
        self.source = source
        self.strings = strings

        # __s_KnHWMv1GbLZ(123)
        self.pattern = re.compile(
            r"__s_KnHWMv1GbLZ\s*\(\s*(\d+)\s*\)"
        )

        self.replaced = 0

    @staticmethod
    def escape_lua(text: str) -> str:
        """
        Escapes a Python string so it is valid inside
        a Lua double quoted string.
        """

        return (
            text
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )

    def _replace(self, match):

        index = int(match.group(1))

        if index < 1 or index > len(self.strings):
            return match.group(0)

        self.replaced += 1

        value = self.escape_lua(
            self.strings[index - 1]
        )

        return f'"{value}"'

    def replace(self):

        return self.pattern.sub(
            self._replace,
            self.source
        )
