# ---------------------------
# Symbiont BINARY+HEX + SYMBOLS ENCODER/DECODER (Unified repeat map)
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

# Unified repeat map for letters, words, phrases
repeat_map = {
    2: ":",
    3: ";",
    4: "::",
    5: "::'"
}

# Caps Lock / uppercase symbol
caps_symbol = "^*?"

# ---------------------------
# Generate split_symbols avoiding phrase_map symbols
# ---------------------------
used_symbols = set()
for sym in phrase_map.values():
    used_symbols.update(sym)

potential_symbols = list("!@#$%^&*~?+=|<>/")  # punctuation pool
split_symbols_clean = [s for s in potential_symbols if s not in used_symbols]

# Allow combinations of 1 or 2 symbols for variety
split_symbols = split_symbols_clean + [s1+s2 for s1 in split_symbols_clean for s2 in split_symbols_clean]

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
# Get repeat symbol for any element
# ---------------------------
def get_repeat_symbol(count):
    if count <= 1:
        return ''
    if count in repeat_map:
        return repeat_map[count]
    # For counts > 5, append extra apostrophes
    return repeat_map[5] + "'"*(count-5)

# ---------------------------
# Encode a single word or phrase
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

            letter = word[i]
            letter_encoded = encode_letter(letter, letter_index, mode)
            if letter.isupper():
                letter_encoded = caps_symbol + letter_encoded

            encoded.append(letter_encoded)
            if repeat_count > 1:
                encoded.append(get_repeat_symbol(repeat_count))

            i += repeat_count
            letter_index += 1
            mode = 'hex' if mode == 'bin' else 'bin'

    return ' '.join(encoded), letter_index, mode

# ---------------------------
# Encode full text with repeated words/phrases
# ---------------------------
def encode_text(message):
    words = message.split(' ')
    encoded_words = []
    letter_index = 0
    mode = 'bin'

    prev_encoded = ''
    repeat_count = 1

    for word in words:
        encoded_word, letter_index, mode = encode_word(word, letter_index, mode)

        # Check for repeated element (word or phrase)
        if encoded_word == prev_encoded:
            repeat_count += 1
        else:
            if repeat_count > 1:
                encoded_words[-1] += get_repeat_symbol(repeat_count)
            repeat_count = 1
            encoded_words.append(encoded_word)
            prev_encoded = encoded_word

    # handle final repeats
    if repeat_count > 1:
        encoded_words[-1] += get_repeat_symbol(repeat_count)

    return f" {space_symbol} ".join(encoded_words)

# ---------------------------
# Decode text
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
        caps_next = False

        for block in blocks:
            if not block:
                continue

            # Phrase check
            matched_phrase = None
            for phrase, sym in sorted(phrase_map.items(), key=lambda x: -len(x[1])):
                if block.startswith(sym):
                    matched_phrase = phrase
                    break
            if matched_phrase:
                decoded_word += matched_phrase
                last_char = matched_phrase[-1]
                continue

            # Check repeated-letter symbols
            for rep_count, sym in repeat_map.items():
                if block.endswith(sym):
                    clean_block = block[:-len(sym)]
                    repeat_times = rep_count
                    break
            else:
                clean_block = block
                repeat_times = 1

            # Caps Lock
            if clean_block.startswith(caps_symbol):
                caps_next = True
                clean_block = clean_block[len(caps_symbol):]

            # Remove split symbols
            clean_block2 = ''.join(c for c in clean_block if c not in ''.join(split_symbols_clean))

            # Binary or hex
            if len(clean_block2) == 8 and all(c in '01' for c in clean_block2):
                decoded_char = chr(int(clean_block2, 2))
            elif len(clean_block2) == 2 and all(c in '0123456789ABCDEF' for c in clean_block2):
                decoded_char = chr(int(clean_block2, 16))
            else:
                decoded_char = clean_block2

            if caps_next:
                decoded_char = decoded_char.upper()
                caps_next = False

            decoded_word += decoded_char * repeat_times
            last_char = decoded_char

        decoded_words.append(decoded_word)

    return ' '.join(decoded_words)

# ---------------------------
# Interactive menu
# ---------------------------
def main():
    print("Symbiont: Hybrid Binary+Hex + Symbols Encoder/Decoder (Unified repeat)")
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
            # Uncomment for clipboard support
            # try:
            #     pyperclip.copy(encoded)
            #     print("(Copied to clipboard!)")
            # except Exception:
            #     pass
        else:
            decoded = decode_text(user_input)
            print("\nDecoded message:\n", decoded)

        print("---------------------------\n")

if __name__ == "__main__":
    main()
