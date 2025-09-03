# ---------------------------
# Symbiont BINARY+HEX + SYMBOLS ENCODER/DECODER (fixed decoder + repeated letters)
# ---------------------------

# import pyperclip  # Uncomment if clipboard support is needed

# Reserved phrases → English symbols
phrase_map = {
    "i": "!",
    "i am": "!:]]",
    "we": "^",
    "we are": "^~",
    "you": "&*",
    "you are": "&~",
    "they are": "~@",
    "the": "*:",
    "ish": "+!",
    "ee": "[[",
    "me": "^^[",
    "war": "§&ř"
}

# Space symbol
space_symbol = "-"

# Repetition symbols for consecutive letters
letter_repeats = [';', '::', ';;;', '::::', ';;;;']  # 2,3,4,... repetitions

# Split symbols for binary/hex
split_symbols = ["!", "@", "#", "$", "%", "&"]

# ---------------------------
# Encode a single letter → binary/hex + symbols
# ---------------------------
def encode_letter(letter, index=0, mode='bin'):
    symbol = split_symbols[index % len(split_symbols)]
    ascii_val = ord(letter.lower())

    if mode == 'bin':
        binary = f"{ascii_val:08b}"
        return symbol.join([binary[i:i+2] for i in range(0, 8, 2)])
    elif mode == 'hex':
        hexa = f"{ascii_val:02X}"
        return symbol.join([hexa[i] for i in range(2)])

# ---------------------------
# Encode word
# ---------------------------
def encode_word(word, start_index=0, start_mode='bin'):
    encoded = []
    i = 0
    letter_index = start_index
    mode = start_mode

    while i < len(word):
        # Check for phrase matches
        matched_phrase = None
        for phrase, sym in sorted(phrase_map.items(), key=lambda x: -len(x[0])):
            if word[i:i+len(phrase)] == phrase:
                matched_phrase = (phrase, sym)
                break

        if matched_phrase:
            encoded.append(matched_phrase[1])
            i += len(matched_phrase[0])
        else:
            # Handle repeated letters
            repeat_count = 1
            while i + repeat_count < len(word) and word[i] == word[i + repeat_count]:
                repeat_count += 1

            encoded.append(encode_letter(word[i], letter_index, mode))

            if repeat_count > 1:
                symbol_index = min(repeat_count - 2, len(letter_repeats)-1)
                encoded.append(letter_repeats[symbol_index])
            i += repeat_count
            letter_index += 1
            mode = 'hex' if mode == 'bin' else 'bin'

    return ' '.join(encoded), letter_index, mode

# ---------------------------
# Encode text
# ---------------------------
def encode_text(message):
    words = message.lower().split(' ')
    encoded_words = []
    letter_index = 0
    mode = 'bin'

    for word in words:
        encoded_word, letter_index, mode = encode_word(word, letter_index, mode)
        encoded_words.append(encoded_word + ' ' + space_symbol)

    return ' '.join(encoded_words).strip()

# ---------------------------
# Decode text (fixed + repeated letters)
# ---------------------------
def decode_text(encoded_message):
    decoded_words = []
    tokens = encoded_message.split(space_symbol)

    for token in tokens:
        token = token.strip()
        if not token:
            continue

        decoded_word = ''
        last_char = ''
        blocks = token.split(' ')

        for block in blocks:
            if not block:
                continue

            # Phrase symbols
            matched_phrase = None
            for phrase, sym in sorted(phrase_map.items(), key=lambda x: -len(x[1])):
                if block == sym:
                    matched_phrase = phrase
                    break
            if matched_phrase:
                decoded_word += matched_phrase
                last_char = matched_phrase[-1]
                continue

            # Repeated letters
            if block in letter_repeats:
                if last_char:
                    repeat_count = letter_repeats.index(block) + 2  # +2 because first repeat is not in symbol
                    decoded_word += last_char * (repeat_count)
                continue

            # Remove split symbols
            clean_block = ''.join(c for c in block if c not in split_symbols)

            # Binary detection (8 bits)
            if len(clean_block) == 8 and all(c in '01' for c in clean_block):
                decoded_char = chr(int(clean_block, 2))
            # Hex detection (2 digits)
            elif len(clean_block) == 2 and all(c in '0123456789ABCDEF' for c in clean_block):
                decoded_char = chr(int(clean_block, 16))
            else:
                decoded_char = clean_block

            decoded_word += decoded_char
            last_char = decoded_char

        decoded_words.append(decoded_word)

    return ' '.join(decoded_words)

# ---------------------------
# Interactive menu
# ---------------------------
def main():
    print("Symbiont: Hybrid Binary+Hex + Symbols Encoder/Decoder (with repeated letters)")
    print("Type 'exit' to quit.\n")

    while True:
        choice = input("Type 'encode' or 'decode': ").strip().lower()
        if choice == 'exit':
            break
        if choice not in ['encode', 'decode']:
            print("Invalid choice.\n")
            continue

        user_input = input("Enter your message: ").strip()
        if user_input.lower() == 'exit':
            break

        if choice == 'encode':
            encoded = encode_text(user_input)
            print("\nEncoded message:\n", encoded)
            # Uncomment to copy to clipboard
            # try:
            #     pyperclip.copy(encoded)
            #     print("(Encoded message copied to clipboard!)")
            # except Exception:
            #     pass
        else:
            decoded = decode_text(user_input)
            print("\nDecoded message:\n", decoded)

        print("---------------------------\n")


if __name__ == "__main__":
    main()
