# ---------------------------
# Symbiont BINARY + SYMBOLS ENCODER/DECODER
# ---------------------------

# Reserved sequences / words → English symbols
sequence_map = {
    "ch": "@",
    "ck": "<}",
    "sh": "#",
    "th": "$",
    "ph": "%",
    "wh": "§"
}

# Reserved phrases → English symbols
phrase_map = {
    "i": "!",
    "i am": "!:",
    "we": "^",
    "we are": "^~",
    "you": "&*",
    "you are": "&~",
    "they are": "~@",
    "the": "*:",
    "ish": "+!",
    "ee": "[[",
    "me": "^^[",
    "war" : "§&ř"
}

# Space symbol
space_symbol = "\\"

# Repetition symbols
word_repeats = [',', ':', ';', "'", '~']
letter_repeats = ['+', '*', '^', '%', '$']

# Split symbols for binary (rotating, no Czech for now)
split_symbols = ["!", "@", "#", "$", "%", "&"]

# Track used symbols to avoid repetition in phrase_map
used_symbols = set(phrase_map.values())

# ---------------------------
# Encode a single letter → 4bits + symbol + 4bits
# ---------------------------
def encode_letter(letter, index=0):
    binary = f"{ord(letter.lower()):08b}"
    symbol = split_symbols[index % len(split_symbols)]
    return binary[:4] + symbol + binary[4:]

# ---------------------------
# Encode word with repeated letters inside
# ---------------------------
def encode_word(word, start_index=0):
    encoded = []
    i = 0
    letter_index = start_index
    while i < len(word):
        repeat_count = 1
        while i + repeat_count < len(word) and word[i] == word[i + repeat_count]:
            repeat_count += 1
        # Add binary for letter (split into 4+symbol+4)
        encoded.append(encode_letter(word[i], letter_index))
        letter_index += 1
        # Repetition symbol if letters repeat
        if repeat_count > 1:
            symbol_index = min(repeat_count - 1, len(letter_repeats) - 1)
            encoded.append(letter_repeats[symbol_index])
        i += repeat_count
    return ' '.join(encoded), letter_index

# ---------------------------
# Encode word with phrases inside + binary + proper separation
# ---------------------------
def encode_text(message):
    encoded = []
    words = message.lower().split(' ')
    letter_index = 0

    for word in words:
        temp_blocks = []
        i = 0
        while i < len(word):
            matched_phrase = None
            matched_sym = None
            # Check phrases inside word
            for phrase, sym in sorted(phrase_map.items(), key=lambda x: -len(x[0])):
                if word[i:i+len(phrase)] == phrase:
                    matched_phrase = phrase
                    matched_sym = sym
                    break
            if matched_phrase:
                temp_blocks.append(matched_sym)
                i += len(matched_phrase)
            else:
                # No phrase → encode letter with split binary
                repeat_count = 1
                while i + repeat_count < len(word) and word[i] == word[i + repeat_count]:
                    repeat_count += 1
                temp_blocks.append(encode_letter(word[i], letter_index))
                letter_index += 1
                if repeat_count > 1:
                    symbol_index = min(repeat_count - 1, len(letter_repeats)-1)
                    temp_blocks.append(letter_repeats[symbol_index])
                i += repeat_count

        encoded.append(' '.join(temp_blocks) + ' ' + space_symbol)

    return ' '.join(encoded).strip()

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

        # Check phrases
        matched = False
        for phrase, sym in phrase_map.items():
            if sym in token:
                decoded_words.append(phrase)
                matched = True
                break
        if matched:
            continue

        # Decode binary + repeated letters
        decoded_word = ''
        parts = token.split(' ')
        i = 0
        while i < len(parts):
            part = parts[i]
            # Handle split binary (4bits+symbol+4bits)
            for sym in split_symbols:
                if sym in part:
                    part = part.replace(sym, "")
                    break
            if all(c in '01' for c in part) and len(part) == 8:
                decoded_word += chr(int(part, 2))
            elif part in letter_repeats:
                decoded_word += decoded_word[-1] * (letter_repeats.index(part) + 1)
            else:
                decoded_word += part
            i += 1
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)

# ---------------------------
# Interactive menu
# ---------------------------
def main():
    print("Symbiont: Hybrid Binary + Symbols Encoder/Decoder (with 4+symbol+4 binary split)")
    print("Type 'exit' to quit.\n")
    while True:
        choice = input("Type 'encode' or 'decode': ").strip().lower()
        if choice == 'exit':
            break
        if choice not in ['encode','decode']:
            print("Invalid choice.\n")
            continue
        user_input = input("Enter your message: ").strip()
        if user_input.lower() == 'exit':
            break
        if choice == 'encode':
            print("\nEncoded message:\n", encode_text(user_input))
        else:
            print("\nDecoded message:\n", decode_text(user_input))
        print("---------------------------\n")

if __name__ == "__main__":
    main()
