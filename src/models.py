from dataclasses import dataclass, field


@dataclass
class Translation:
    partofspeech: str  # pos
    chinese: str  # tran_cn
    
    def __str__(self) -> str:
        return f"    - {self.partofspeech}. {self.chinese}"


@dataclass
class Headword:
    content: str  # hwd
    chinese: str  # tran
    
    def __str__(self) -> str:
        return f"{self.content} {self.chinese}"


@dataclass
class RelatedWord:
    headwords: list[Headword]  # Hwds
    partofspeech: str  # Pos
    
    def __str__(self) -> str:
        result = []
        for hwd in self.headwords:
            result.append(f"    - {self.partofspeech}. {hwd}")
        return "\n".join(result)


@dataclass
class Phrase:
    content: str  # p_content
    chinese: str  # p_cn
    
    def __str__(self) -> str:
        return f"    - {self.content} {self.chinese}"


@dataclass
class SynonymItem:
    word: str  # word
    
    def __str__(self) -> str:
        return self.word


@dataclass
class SynonymGroup:
    partofspeech: str  # pos
    synonyms: list[SynonymItem]  # Hwds
    chinese: str  # tran
    
    def __str__(self) -> str:
        synonyms_str = " ".join(str(syn) for syn in self.synonyms)
        return f"    - {self.partofspeech}. {synonyms_str} {self.chinese}"


@dataclass
class Sentence:
    content: str  # s_content
    chinese: str  # s_cn

    def __str__(self) -> str:
        result = ""
        result += f"    - {self.content}\n"
        result += f"      {self.chinese}"
        return result


@dataclass
class Word:
    content: str  # word
    usphone: str  # usphone
    ukphone: str  # ukphone
    usspeech: str  # usspeech
    ukspeech: str  # ukspeech
    translations: list[Translation] = field(default_factory=list)
    related_words: list[RelatedWord] = field(default_factory=list)
    phrases: list[Phrase] = field(default_factory=list)
    synonym_groups: list[SynonymGroup] = field(default_factory=list)
    sentences: list[Sentence] = field(default_factory=list)

    def __str__(self) -> str:
        output = []
        
        # 单词和音标
        output.append(f"\033[1m{self.content}\033[0m")
        output.append(f"美: {self.usphone} | 英: {self.ukphone}")
        output.append("")
        
        # Translations
        if self.translations:
            output.append("\033[1mTranslations:\033[0m")
            for trans in self.translations:
                output.append(str(trans))
            output.append("")
        
        # Related Words
        if self.related_words:
            output.append("\033[1mRelated Words:\033[0m")
            for rel in self.related_words:
                output.append(str(rel))
            output.append("")
        
        # Phrases
        if self.phrases:
            output.append("\033[1mPhrases:\033[0m")
            for phrase in self.phrases:
                output.append(str(phrase))
            output.append("")
        
        # Synonyms
        if self.synonym_groups:
            output.append("\033[1mSynonyms:\033[0m")
            for syn_group in self.synonym_groups:
                output.append(str(syn_group))
            output.append("")
        
        # Sentences
        if self.sentences:
            output.append("\033[1mSentences:\033[0m")
            for sentence in self.sentences:
                output.append(str(sentence))
                output.append("")
        
        return "\n".join(output)