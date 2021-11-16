from nltk.tokenize import word_tokenize
from employme.items import Knowledge
from employme.me import MESSAGES
from typing import List
from loguru import logger as log


class KnowledgeInterpreter:
    """Interprets personal opinion/experience messages from text or knowledge data sets"""
    def skills_from_text(self, text) -> List[str]:
        if not text:
            return []
        text = text.lower()
        tokens = [Knowledge.normalize_skill(skill) for skill in word_tokenize(text)]
        found_singles = [t for t in tokens if t in MESSAGES]
        found_multiples = []
        for key in MESSAGES.keys():
            if len(key.split(' ')) < 2:
                continue
            if key in text:
                found_multiples.append(key)
        return list(dict.fromkeys(found_singles + found_multiples).keys())

    def interpret(self, knowledge: List[Knowledge]):
        """interpret collection of knowledge with person's personality"""
        seen = set()
        for kn in knowledge:
            skills_from_description = self.skills_from_text(kn.description)
            log.info(f"found skill in description: {skills_from_description}")
            for skill in kn.skills + skills_from_description:
                if skill in seen:
                    continue
                message = MESSAGES.get(skill)
                if not message:
                    continue
                yield f"{skill}: {message}"
                seen.add(skill)
