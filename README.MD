# Symbiont – Hybrid Binary & Symbol Encoder

### still just Night consept 


**Tagline:** "Where binary meets symbols, phrases hide in plain sight."

## OVERVIEW
Symbiont is a hybrid text encoding tool that converts messages into a combination of:
- 8-bit binary letters
- Symbolic phrases and words
- Repetition indicators for repeated letters and words
- Dedicated space symbols (\)

It is designed for obfuscation, experimentation, and cryptography education, offering a unique, fully reversible encoding system.

## WHY THIS APPROACH
Traditional encoding methods such as ASCII, Base64, or simple binary are predictable and easily decoded.
Symbiont introduces additional layers of complexity to make encoded messages harder to interpret without the program:

1.  **Phrase substitution** – Common words and phrases are replaced with symbols (!, @:, etc.), breaking predictable patterns.
2.  **Inside-word detection** – Phrases appearing inside other words are also encoded, further obfuscating familiar sequences.
3.  **Repetition symbols** – Repeated letters and words are replaced with dedicated symbols (+ * ^ % $ for letters, : ; , ~ for words), adding another layer of complexity.
4.  **Hybrid encoding blocks** – Binary and symbols are separated in blocks, making manual decoding challenging.
5.  **Customizable future extensions** – Reserved symbol mapping can expand to include Czech symbols or additional phrase mappings, ensuring scalability.

## WHY NOT USE ONLY BINARY OR ONLY SYMBOLS
-   **Binary only:** predictable; repeated letters/words are obvious.
-   **Symbols only:** may run out of unique symbols and can become ambiguous for longer texts.
-   **Symbiont hybrid approach:** combines binary for letters not part of mapped phrases and symbols for phrases/repetitions, ensuring uniqueness, obfuscation, and reversibility.

## KEY FEATURES
1.  **Hybrid Encoding** – Combines letters in binary with symbol-based phrase mapping.
2.  **Phrase Detection Inside Words** – Phrases are recognized even when embedded in other words.
3.  **Repetition Handling** – Special symbols indicate repeated letters and repeated words.
4.  **Clear Block Separation** – Binary and symbols are separated for deterministic decoding.
5.  **Customizable** – Supports adding new phrases, words, or symbols (including future Czech symbols).
6.  **Interactive** – Encode or decode messages easily through a console interface.

## USAGE
**Interactive Mode:**

1.  **Encode a message:**
    ```
    Type 'encode' or 'decode': encode
    Enter your message: ishmish
    ```
    **Output:**
    ```
    +! 01101101 +! \
    ```

2.  **Decode a message:**
    ```
    Type 'encode' or 'decode': decode
    Enter your message: +! 01101101 +! \
    ```
    **Output:**
    ```
    ishmish
    ```

    -   `+!` → phrase "ish"
    -   `01101101` → letter "m"
    -   `\` → space

## SYMBOL LEGEND
**Phrases / Words → Symbols:**
-   "i" → "!"
-   "i am" → "!:"
-   "we" → "^"
-   "we are" → "^~"
-   "ish" → "+!"
-   ...

**Repeated letters →** `+ * ^ % $`
**Repeated words →** `, : ; ' ~`
**Space →** `\`

## LIMITATIONS / CONSIDERATIONS
-   **Not standard encryption:** Symbiont is obfuscation, not cryptographically secure.
-   **Symbol exhaustion:** If too many phrases are added, English symbols may run out; Czech symbols can be added in future versions.
-   **Message length:** Messages may expand due to binary encoding and repetition symbols.
-   **Manual decoding difficulty:** While reversible with the program, manual decoding is extremely difficult by design.

## FUTURE EXTENSIONS
-   Add Czech symbols for additional phrases when English symbols run out.
-   Support longer phrases or sentence-level mappings.
-   Introduce randomized symbols for repeated words to increase obfuscation.
-   Multi-language support for symbols and phrases.

## INSTALLATION
1.  Ensure Python 3.x is installed.
2.  Download `symbiont.py` (the main script).
3.  Run using:
    ```bash
    python symbiont.py
    ```
