from transformers.models.whisper.english_normalizer import BasicTextNormalizer
from text_normalizer.utils import remove_space_before_after_text

EN_BASIC_NORMALIZER = BasicTextNormalizer()

def en_normalizer(text):
    text = text.lower()
    text = EN_BASIC_NORMALIZER(text)
    text = remove_space_before_after_text(text)
    return text

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    text = ' hello world!!!! '
    print(bytes(text, 'utf-8'))
    print(bytes(en_normalizer(text), 'utf-8'))