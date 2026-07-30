import re


class Decoder:
    """
    Decodes encrypted LuaU string tables like:

    local __s_xxxxx = {
        {{170,158,166},47},
        {{135,145,196},61},
        ...
    }
    """

    TABLE_PATTERN = re.compile(
        r"local\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{(.*?)\}\s*;",
        re.DOTALL,
    )

    ENTRY_PATTERN = re.compile(
        r"\{\{([\d,\s]+)\},(\d+)\}"
    )

    def __init__(self, source: str):
        self.source = source

        self.table_name = None
        self.strings = []

    @staticmethod
    def decode(values, key):
        return "".join(
            chr((v - key - (i + 1) * 7) % 256)
            for i, v in enumerate(values)
        )

    def parse(self):

        match = self.TABLE_PATTERN.search(self.source)

        if not match:
            raise RuntimeError("Encrypted string table not found.")

        self.table_name = match.group(1)

        table_text = match.group(2)

        self.strings.clear()

        for entry in self.ENTRY_PATTERN.finditer(table_text):

            values = [
                int(x.strip())
                for x in entry.group(1).split(",")
            ]

            key = int(entry.group(2))

            self.strings.append(
                self.decode(values, key)
            )

        return self.strings

    def get(self, index: int):

        if index < 1 or index > len(self.strings):
            raise IndexError(index)

        return self.strings[index - 1]
