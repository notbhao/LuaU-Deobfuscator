from decoder import Decoder
from replacer import Replacer

with open("code.lua","r",encoding="utf8") as f:
    source = f.read()

decoder = Decoder(source)
decoder.parse()

print(f"Decoded {len(decoder.strings)} strings")

replacer = Replacer(
    source,
    decoder.strings
)

output = replacer.replace()

print(f"Replaced {replacer.replaced} calls")

with open("output.lua","w",encoding="utf8") as f:
    f.write(output)

print("Saved output.lua")
