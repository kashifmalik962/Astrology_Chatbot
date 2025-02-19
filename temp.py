# "cn you tel me about kundli"

from symspellpy import SymSpell, Verbosity

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load a dictionary
dictionary_path = "frequency_dictionary_en_82_765.txt"  # Download from SymSpell GitHub
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Input text
text = "Ths is a smple txt with spellng mistaks."

# Correct each word
words = text.split()
corrected_words = [
    sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)[0].term
    if sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
    else word
    for word in words
]

# Join corrected words into a sentence
corrected_text = " ".join(corrected_words)

print("Original Text:", text)
print("Corrected Text:", corrected_text)
