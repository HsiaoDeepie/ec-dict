#!/usr/bin/env python3
import sys
import json
import requests
from playsound3 import playsound
import tempfile
import os
from models import Word, Translation, Headword, RelatedWord, Phrase, SynonymGroup, SynonymItem, Sentence
from log_utils import Logger


class DictionaryCLI:
    def __init__(self):
        self.api_url = "https://v2.xxapi.cn/api/englishwords"
        self.logger = Logger()
    
    def parse_response(self, json_data):
        """解析API响应数据为Word对象"""
        data = json_data.get("data", {})
        
        # 创建Word对象
        word_obj = Word(
            content=data.get("word", ""),
            usphone=data.get("usphone", ""),
            ukphone=data.get("ukphone", ""),
            usspeech=data.get("usspeech", ""),
            ukspeech=data.get("ukspeech", "")
        )
        
        # 解析translations
        translations = data.get("translations", [])
        for trans in translations:
            translation = Translation(
                partofspeech=trans.get("pos", ""),
                chinese=trans.get("tran_cn", "")
            )
            word_obj.translations.append(translation)
        
        # 解析related words
        rel_words = data.get("relWords", [])
        for rel in rel_words:
            headwords = []
            hwds_list = rel.get("Hwds", [])
            for hwd in hwds_list:
                headword = Headword(
                    content=hwd.get("hwd", ""),
                    chinese=hwd.get("tran", "")
                )
                headwords.append(headword)
            
            related_word = RelatedWord(
                headwords=headwords,
                partofspeech=rel.get("Pos", "")
            )
            word_obj.related_words.append(related_word)
        
        # 解析phrases
        phrases = data.get("phrases", [])
        for phrase in phrases:
            phrase_obj = Phrase(
                content=phrase.get("p_content", ""),
                chinese=phrase.get("p_cn", "")
            )
            word_obj.phrases.append(phrase_obj)
        
        # 解析synonyms
        synonyms = data.get("synonyms", [])
        for syn in synonyms:
            synonym_items = []
            hwds_list = syn.get("Hwds", [])
            for hwd in hwds_list:
                synonym_item = SynonymItem(
                    word=hwd.get("word", "")
                )
                synonym_items.append(synonym_item)
            
            synonym_group = SynonymGroup(
                partofspeech=syn.get("pos", ""),
                synonyms=synonym_items,
                chinese=syn.get("tran", "")
            )
            word_obj.synonym_groups.append(synonym_group)
        
        # 解析sentences
        sentences = data.get("sentences", [])
        for sentence in sentences:
            sentence_obj = Sentence(
                content=sentence.get("s_content", ""),
                chinese=sentence.get("s_cn", "")
            )
            word_obj.sentences.append(sentence_obj)
        
        return word_obj
    
    def query_word(self, word):
        """查询单词"""
        try:
            response = requests.get(f"{self.api_url}?word={word}")
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 200:
                error_msg = data.get('msg', '未找到该单词')
                print(f"错误: {error_msg}")
                return None
            
            # 解析为Word对象
            word_obj = self.parse_response(data)
            
            # 保存原始JSON数据
            home = os.path.expanduser("~")
            os.makedirs(f"{home}/.dict", exist_ok=True)
            os.makedirs(f"{home}/.dict/words", exist_ok=True)
            with open(f"{home}/.dict/words/{word}.json", "w", encoding="utf-8") as f:
                json.dump(data.get("data", {}), f, ensure_ascii=False, indent=2)
            
            return word_obj
        except requests.exceptions.RequestException as e:
            error_msg = f"NetworkError: when connect {self.api_url}\n\n{e}"
            self.logger.log_error(error_msg)
            print(f"dict: {error_msg}")
            return None
        except json.JSONDecodeError:
            error_msg = f"Error: Failed to parse response from {self.api_url}"
            self.logger.log_error(error_msg)
            print(f"dict: {error_msg}")
            return None
        except Exception as e:
            error_msg = f"Error parsing data: {e}"
            self.logger.log_error(error_msg)
            print(f"dict: {error_msg}")
            return None
    
    def play_audio(self, audio_url):
        """播放美式发音"""
        try:
            # 下载音频到临时文件
            response = requests.get(audio_url)
            response.raise_for_status()
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # 播放音频
            playsound(temp_path)
            
            # 删除临时文件
            os.unlink(temp_path)
            
        except Exception as e:
            error_msg = f"Error: Can't play sounds, {e}"
            self.logger.log_error(error_msg)
            print(f"dict: {error_msg}")
    
    def run(self, word):
        """运行主逻辑"""
        # 记录查询的单词到info.log
        self.logger.log_info(f"Query: {word}")
        
        # 查询单词
        word_obj = self.query_word(word)
        if not word_obj:
            return
        
        # 播放美式发音
        if word_obj.usspeech:
            self.play_audio(word_obj.usspeech)
        
        # 输出结果
        print(word_obj)


def main():
    if len(sys.argv) != 2:
        print("dict: error: Word is required")
        print("Try 'dict --help' for more information.")
        sys.exit(1)
    if sys.argv[1] in ("--help"):
        print("Usage: dict [WORD]")
        sys.exit(0)
    if sys.argv[1] in ("--version"):
        print("dict version 1.0.0\n")
        print("Written by Hsiao Deepie.")
        sys.exit(0)
    
    word = sys.argv[1].lower()
    cli = DictionaryCLI()
    cli.run(word)


if __name__ == "__main__":
    main()