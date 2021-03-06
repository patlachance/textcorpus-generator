import re
import logging

PHRASE_PARTS_REGEX = re.compile('\(.*?\)+|[^[\s]+')  # ("\\(.*?\\)+|[^\\[\\s]+")

EXPAND_SLOT_REGEX = re.compile('\(.*\|.*\)')  # ("\\(.*\\|.*\\)")

SINGLE_WORD_INSIDE_EXPAND_SLOT_REGEX = re.compile('\(([\w-]+)\)')  # ("\\(([\\w-]+)\\)")

WORDS_INSIDE_EXPAND_SLOT_REGEX = re.compile('([^|()]+)')  # ("[^|()]+")


def expand(template: str) -> str:
    """
    Expand a template to generate a sentence
    :param template: A string that represents a template
    :return: A true sentence that follow the template pattern
    """
    logger = logging.getLogger(__name__)
    logger.debug("Expanding string {sentence} ...".format(sentence=template))
    phrases = []

    # single word inside expand slot
    phrase = re.sub(SINGLE_WORD_INSIDE_EXPAND_SLOT_REGEX, '\\1', template)
    parts = PHRASE_PARTS_REGEX.findall(phrase)
    index = 0

    for part in parts:
        words = WORDS_INSIDE_EXPAND_SLOT_REGEX.findall(part)

        if not EXPAND_SLOT_REGEX.search(part) is None:
            for word in words:
                copy = parts
                copy[index] = word
                phrases.append(' '.join(copy))

                # remove word, ie.( | foo)
                if len(words) == 1:
                    copy = parts
                    del copy[index]
                    phrases.append(' '.join(copy))

            break
        index += 1

    if len(phrases) <= 0:
        phrases.append(phrase)

    # To Iterate is Human, to Recurse, Divine
    iterate = []
    for string in phrases:
        if EXPAND_SLOT_REGEX.search(string) is None:
            iterate.append(string)
        else:
            iterate.extend(expand(string))

    return iterate
