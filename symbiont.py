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
    "ee" : "[[",
    "me" : "^^["
}

# Space symbol
space_symbol = "\\"

# Repetition symbols
word_repeats = [',', ':', ';', "'", '~']
letter_repeats = ['+', '*', '^', '%', '$']

# Track used symbols to avoid repetition in phrase_map
used_symbols = set(phrase_map.values())

# ---------------------------
# Encode a single letter → 8-bit binary
# ---------------------------
def encode_letter(letter):
    return f"{ord(letter.lower()):08b}"

# ---------------------------
# Encode word with repeated letters inside
# ---------------------------
def encode_word(word):
    encoded = []
    i = 0
    while i < len(word):
        repeat_count = 1
        while i + repeat_count < len(word) and word[i] == word[i + repeat_count]:
            repeat_count += 1
        # Add binary for letter
        encoded.append(encode_letter(word[i]))
        # Repetition symbol if letters repeat
        if repeat_count > 1:
            symbol_index = min(repeat_count - 1, len(letter_repeats)-1)
            encoded.append(letter_repeats[symbol_index])
        i += repeat_count
    return ' '.join(encoded)

# ---------------------------
# Encode word with phrases inside + binary + proper separation
# ---------------------------
def encode_text(message):
    encoded = []
    words = message.lower().split(' ')
    word_count = {}

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
                # Phrase matched → add symbol as a separate block
                temp_blocks.append(matched_sym)
                i += len(matched_phrase)
            else:
                # No phrase → encode letter as binary
                repeat_count = 1
                while i + repeat_count < len(word) and word[i] == word[i + repeat_count]:
                    repeat_count += 1
                temp_blocks.append(encode_letter(word[i]))
                if repeat_count > 1:
                    symbol_index = min(repeat_count - 1, len(letter_repeats)-1)
                    temp_blocks.append(letter_repeats[symbol_index])
                i += repeat_count

        # Add blocks for this word and append space symbol
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
            if all(c in '01' for c in part):
                decoded_word += chr(int(part,2))
            elif part in letter_repeats:
                decoded_word += decoded_word[-1]*(letter_repeats.index(part)+1)
            else:
                decoded_word += part
            i += 1
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)

# ---------------------------
# Interactive menu
# ---------------------------
def main():
    print("Hybrid Binary + Symbols Encoder/Decoder (Phrases inside words)")
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
