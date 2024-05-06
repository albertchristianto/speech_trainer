import opencc

from common.text_normalizer.cn_tn import TextNorm

CONVERTER = opencc.OpenCC('s2tw.json')

ZH_BASIC_NORMALIZER = TextNorm(to_banjiao = False, to_upper = False, to_lower = False,
        remove_fillers = False, remove_erhua = False, check_chars = False,
        remove_space = True, cc_mode = '')

def zh_normalizer(text):
    text = ZH_BASIC_NORMALIZER(text)
    text = CONVERTER.convert(text)
    text = text.strip()
    return text