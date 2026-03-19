
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json
from pathlib import Path

ALPHABET = [chr(ord('A') + i) for i in range(26)]

@dataclass
class Question:
    question_id: Optional[int]
    category: Optional[str]
    question: str
    correct_answer: List[str]  # normalized to list of letters (A..)
    choices: List[str]
    reasoning: Optional[str]
    difficulty: Optional[int]
    can_shuffle: bool

    def is_multi(self) -> bool:
        return len(self.correct_answer) > 1

    def difficulty_stars(self) -> str:
        if not isinstance(self.difficulty, int) or not (1 <= self.difficulty <= 5):
            return "N/A"
        return "★" * self.difficulty + "☆" * (5 - self.difficulty)

class ValidationError(Exception):
    pass

class QuestionBank:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.questions: List[Question] = []
        self.categories: List[str] = []

    def load(self) -> Tuple[int, int]:
        if not self.path.exists():
            raise FileNotFoundError(f"Bank not found: {self.path}")
        data = json.loads(Path(self.path).read_text(encoding='utf-8'))
        if not isinstance(data, list):
            raise ValidationError("JSON root must be a list of question objects")
        valid = []
        skipped = 0
        for i, obj in enumerate(data, 1):
            try:
                q = self._validate_and_make(obj)
                valid.append(q)
            except Exception as e:
                skipped += 1
                print(f"[QuestionBank] Skipped item #{i}: {e}")
        self.questions = valid
        self.categories = sorted({q.category or "N/A" for q in self.questions})
        return len(valid), skipped

    def _validate_and_make(self, obj: dict) -> Question:
        qid = obj.get('question_id')
        if qid is not None and not isinstance(qid, int):
            raise ValidationError("question_id must be integer or omitted")
        category = obj.get('category')
        if category is not None and not isinstance(category, str):
            raise ValidationError("category must be string or omitted")
        question = obj.get('question')
        if not isinstance(question, str) or not question.strip():
            raise ValidationError("question must be non-empty string")
        ca = obj.get('correct_answer')
        if isinstance(ca, str):
            ca_list = [ca.strip()]
        elif isinstance(ca, list):
            ca_list = [str(x).strip() for x in ca]
        else:
            raise ValidationError("correct_answer must be a single letter or list of letters")
        for a in ca_list:
            if a not in ALPHABET:
                raise ValidationError("correct_answer items must be single capital letters A..Z")
        choices = obj.get('choices')
        if not isinstance(choices, list) or not (2 <= len(choices) <= 12):
            raise ValidationError("choices must be list with 2..12 items")
        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValidationError("choices items must be non-empty strings")
        reasoning = obj.get('reasoning')
        if reasoning is not None and not isinstance(reasoning, str):
            raise ValidationError("reasoning must be string or omitted")
        difficulty = obj.get('difficulty')
        if difficulty is not None:
            if not isinstance(difficulty, int) or not (1 <= difficulty <= 5):
                raise ValidationError("difficulty must be integer 1..5 or omitted")
        can_shuffle = obj.get('can_shuffle', False)
        if not isinstance(can_shuffle, bool):
            raise ValidationError("can_shuffle must be boolean")
        return Question(
            question_id=qid,
            category=category,
            question=question,
            correct_answer=ca_list,
            choices=choices,
            reasoning=reasoning,
            difficulty=difficulty,
            can_shuffle=can_shuffle,
        )
