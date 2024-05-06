from transformers.models.whisper.english_normalizer import EnglishTextNormalizer

EN_BASIC_NORMALIZER = EnglishTextNormalizer()

def en_normalizer(text):
    text = text.lower()
    text = EN_BASIC_NORMALIZER(text)
    text = text.strip()
    return text

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    text = ' hello world!!!! '
    print(bytes(text, 'utf-8'))
    print(bytes(en_normalizer(text), 'utf-8'))