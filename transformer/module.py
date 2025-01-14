from googletrans import Translator

def translator(str, dest:str='vi'):
    translator = Translator()
    result = translator.translate(str, dest=dest)
    return result.text