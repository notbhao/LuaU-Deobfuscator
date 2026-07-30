from pathlib import Path
from colorama import Fore, Style, init

from decoder import Decoder
from replacer import Replacer

init(autoreset=True)


class LuaUDecompiler:

    def __init__(self, path):

        self.path = Path(path)

        self.source = self.path.read_text(
            encoding="utf8",
            errors="ignore"
        )

    def run(self):

        print(Fore.CYAN + "[*] Reading file")

        decoder = Decoder(self.source)

        decoder.parse()

        print(
            Fore.GREEN +
            f"[+] Decoded {len(decoder.strings)} strings"
        )

        replacer = Replacer(
            self.source,
            decoder.strings
        )

        output = replacer.replace()

        out = Path("output.lua")

        out.write_text(
            output,
            encoding="utf8"
        )

        print(
            Fore.GREEN +
            "[+] Saved -> output.lua"
        )


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print("Usage:")
        print("python main.py code.lua")
        exit()

    LuaUDecompiler(
        sys.argv[1]
    ).run()
