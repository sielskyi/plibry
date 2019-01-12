# @file wordsdict.py
# @brief Dictionary of all words.
# @author Sielskyi Leonid (sielskyi)
#

# Description
#
# Words values:
# 0x00 - 0x1FFFFFFF     - Integer values
# 0x20000000            - Empty word
# 0x20000002            - Start of text
# 0x20000003            - End of text
#
# 0x200000NN, NN - ASCII symbol value   - separate ASCII symbol
#
# 0x20NNNNNN, NNNNNN - UTF-8 symbol value   - separate UTF-8 symbol
#
# 0x30000000 - 0x30FFFFFF   - Decimal values starting with '0' that not exist in range 0x00 - 0x1FFFFFFF
# ..            ..
# 0x39000000 - 0x39FFFFFF   - Decimal values starting with '9' that not exist in range 0x00 - 0x1FFFFFFF
#
# 0x41000000 - 0x41FFFFFF   - Words starts with 'A'
# 0x42000000 - 0x42FFFFFF   - Words starts with 'B'
# ..            ..
# 0x5A000000 - 0x5AFFFFFF   - Words starts with 'Z'
#
# 0x61000000 - 0x61FFFFFF   - Words starts with 'a'
# 0x62000000 - 0x62FFFFFF   - Words starts with 'b'
# ..            ..
# 0x7A000000 - 0x7AFFFFFF   - Words starts with 'z'
# ..            ..
# 0x0000NNNNNN000000 - 0x0000NNNNNNFFFFFF   - Words starts with symbol with UTF-8 code 0xNNNNNN
#

import os
import re

_WORDS_PER_TYPE_MAX = 0x01000000
_INTEGER_MIN = 0
_INTEGER_MAX = 0x1FFFFFFF
_WORD_SYMB_START = 0x20000000
_WORD_EMPTY = 0x20000000
_WORD_TEXT_START = 0x20000002
_WORD_TEXT_END = 0x20000003
_WORD_IN_FILE_START = 0x21000000

_WORDS_DICT_DATA_DIR = '../data/wordsdict'


class WordsDict:

    def get_word_index(self, string, lang=''):
        assert isinstance(string, str), "Parameter \'string\' is not a string"
        assert isinstance(lang, str), "Parameter \'lang\' is not a string"
        assert (len(string) > 0), "Parameter \'string\' is empty"

        recomp = re.compile(r'\s')          # pattern for all blank symbols
        if recomp.search(string):           # check if string contain blank symbols
            return _WORD_EMPTY

        index = self._get_first_index(string)
        if index >= _WORD_IN_FILE_START:
            filepath = self._get_file_path(string)
            if filepath != '':
                index = self._get_index_from_file(filepath, string, lang)
                if index == _WORD_EMPTY:
                    index = self._get_new_index_set_to_file(filepath, string, lang)
            else:
                index = _WORD_EMPTY
        return index

    def check_word(self, string, lang=''):
        assert isinstance(string, str), "Parameter \'string\' is not a string"
        assert isinstance(lang, str), "Parameter \'lang\' is not a string"
        assert (len(string) > 0), "Parameter \'string\' is empty"

        recomp = re.compile(r'\s')          # pattern for all blank symbols
        if recomp.match(string):            # check if string contain blank symbols
            return _WORD_EMPTY

        index = self._get_first_index(string)
        if index >= _WORD_IN_FILE_START:
            filepath = self._get_file_path(string)
            if filepath != '':
                index = self._get_index_from_file(filepath, string, lang)
            else:
                index = _WORD_EMPTY
        return index

    def format_words(self, string):
        """Format every word and separate them by newline"""

        assert isinstance(string, str), "Parameter \'string\' is not a string"

        recomp = re.compile(r'\s')  # pattern for all space symbols
        string = recomp.sub('\n', string)  # replace by new line
        recomp = re.compile(r'(^\d+$)', flags=re.MULTILINE)  # pattern for only digits words
        string = recomp.sub('', string)
        recomp = re.compile(r'(^_+)|(_+$)',
                            flags=re.MULTILINE)  # pattern for underscore symbols in begin and end of the word
        string = recomp.sub('', string)
        #recomp = re.compile(r'(^\W+)|(\W+$)',
        #                    flags=re.MULTILINE)  # pattern for nonword symbols in begin and end of the word
        #string = recomp.sub('\n', string)
        string = string.replace('.', '')
        string = string.replace('\n\n', '\n')

        pattern = r"(^\d\w+$)|(^\d\w*\'\w+$)|(^\d\w*-\w+$)|(^\d\w*-\w+$)|(^\d\w*%$)"
        recomp = re.compile(pattern, flags=re.MULTILINE)
        dstrlist = recomp.findall(string)
        string = recomp.sub('', string)
        pattern = r"(^#\d\w+$)|(^#\d\w*\'\w+$)|(^#\d\w*-\w+$)|(^#\d\w*-\w+$)"
        recomp = re.compile(pattern, flags=re.MULTILINE)
        nstrlist = recomp.findall(string)
        string = recomp.sub('', string)
        pattern = r"(^\w+$)|(^\w+-\w+$)|(^\w+\'\w+$)|(^\w+\'\w+\'\w+$)|(^\w+-\w+-\w+$)|(^\w+&\w+$)"
        recomp = re.compile(pattern, flags=re.MULTILINE)
        wstrlist = recomp.findall(string)

        resstr = ''
        if len(wstrlist) != 0:
            resstr = resstr + '\n'.join(str(''.join(st)) for st in wstrlist) + '\n'
        if len(dstrlist) != 0:
            resstr = resstr + '\n'.join(str(''.join(st)) for st in dstrlist) + '\n'
        if len(nstrlist) != 0:
            resstr = resstr + '\n'.join(str(''.join(st)) for st in nstrlist) + '\n'

        return resstr

    def _get_new_index_set_to_file(self, filepath, string, lang):
        index = self._get_first_index(string)
        maxindex = index + _WORDS_PER_TYPE_MAX
        try:
            with open(filepath, 'r', encoding='utf-8') as rfile:
                while True:
                    line = rfile.readline()
                    if line == '':
                        index += 1
                        break
                    try:
                        start = line.index('\t') + 1
                        start = line.index('\t', start) + 1
                        end = line.index('\n')
                        idx = int(line[start:end])
                        if (idx > index) and (idx < maxindex):
                            index = idx
                    except:
                        pass
        except:
            pass
        if index < maxindex:
            line = string + '\t' + lang + '\t' + str(index) + '\n'
            with open(filepath, 'a+', encoding='utf-8') as wfile:
                wfile.write(line)
        else:
            index = _WORD_EMPTY     # words number overflow
        return index

    def _get_index_from_file(self, filepath, string, lang):
        index = _WORD_EMPTY
        try:
            with open(filepath, 'r', encoding='utf-8') as rfile:
                lenstring = len(string)
                lenlang = len(lang)
                while True:
                    line = rfile.readline()
                    if (len(line) > lenstring) and (line[lenstring] == '\t'):
                        if string == line[0:lenstring]:
                            end = lenstring
                            try:
                                if lang != '':
                                    start = line.index(lang, end) + lenlang
                                else:
                                    start = line.index('\t', end) + 1
                                start = line.index('\t', start) + 1
                                end = line.index('\n')
                                index = int(line[start:end])
                                break
                            except:
                                pass
                    else:
                        if line == '':
                            break
        except:
            pass
        return index

    def _get_file_path(self, string):
        fp = ''
        fch = string[0]
        if (len(string) > 1) and (fch > ' '):
            indx = ord(fch)
            fch = hex(indx)

            if indx <= 0xFF:
                fdir = '0xff/'
            else:
                i = 0x0FFF
                fdir = 'XX/'
                while i <= 0xFFFFFF:
                    if indx <= i:
                        fdir = hex(i) + '/'
                        break
                    i += 0x1000

            fp = _WORDS_DICT_DATA_DIR + '/wd_'
            fp += fdir
            try:
                os.mkdir(fp)
            except FileExistsError:
                pass

            fp += 'wd_' + fch + '.csv'
        return fp

    def _get_first_index(self, string):
        index = _WORD_EMPTY
        fch = string[0]

        if fch > ' ':
            if string.isalnum():
                val = int(string)
                if val <= _INTEGER_MAX:
                    index = val
                    fch = ''

            if fch != '':
                index = ord(fch)
                if len(string) > 1:
                    index = index * _WORDS_PER_TYPE_MAX
                else:
                    index = index + _WORD_SYMB_START

        return index
