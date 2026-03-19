
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import random
import time
from models import Question, ALPHABET

@dataclass
class PreparedQuestion:
    original: Question
    display_choices: List[Tuple[str, str]]  # [(letter, text)]
    correct_display_letters: List[str]

    def is_multi(self) -> bool:
        return self.original.is_multi()

class ExamSession:
    def __init__(self, questions: List[Question], num_questions: int):
        if num_questions > len(questions):
            num_questions = len(questions)
        sampled = random.sample(questions, num_questions)
        self.questions: List[PreparedQuestion] = [self._prepare(q) for q in sampled]
        self.current_index: int = 0
        self.answers: Dict[int, List[str]] = {i: [] for i in range(len(self.questions))}
        self._start_monotonic: Optional[float] = None
        self._paused_accum: float = 0.0
        self._pause_started: Optional[float] = None

    def start(self):
        self._start_monotonic = time.monotonic()

    def pause(self):
        if self._pause_started is None:
            self._pause_started = time.monotonic()

    def resume(self):
        if self._pause_started is not None:
            self._paused_accum += time.monotonic() - self._pause_started
            self._pause_started = None

    def is_paused(self) -> bool:
        return self._pause_started is not None

    def elapsed(self) -> float:
        if self._start_monotonic is None:
            return 0.0
        now = time.monotonic()
        if self._pause_started is not None:
            return (self._pause_started - self._start_monotonic) - self._paused_accum
        return (now - self._start_monotonic) - self._paused_accum

    def _prepare(self, q: Question) -> PreparedQuestion:
        # Assign letters AFTER optional shuffle and map correct answers accordingly
        indexed = list(enumerate(q.choices))  # [(orig_idx, text)]
        if q.can_shuffle:
            random.shuffle(indexed)
        pairs: List[Tuple[str, str]] = []
        correct_display: List[str] = []
        correct_orig_letters = set(q.correct_answer)  # letters from original order
        # Map original index -> original letter
        orig_index_to_letter = {i: ALPHABET[i] for i in range(len(q.choices))}
        for new_i, (orig_i, text) in enumerate(indexed):
            new_letter = ALPHABET[new_i]
            pairs.append((new_letter, text))
            if orig_index_to_letter.get(orig_i) in correct_orig_letters:
                correct_display.append(new_letter)
        return PreparedQuestion(
            original=q,
            display_choices=pairs,
            correct_display_letters=sorted(correct_display),
        )

    def set_answer(self, index: int, letters: List[str]):
        self.answers[index] = sorted(list(set(letters)))

    def is_answered(self, index: int) -> bool:
        return len(self.answers.get(index, [])) > 0

    def score(self) -> Tuple[int, int]:
        correct = 0
        total = len(self.questions)
        for i, pq in enumerate(self.questions):
            chosen = set(self.answers.get(i, []))
            actual = set(pq.correct_display_letters)
            if chosen == actual:
                correct += 1
        return correct, total

    def per_category_stats(self) -> Dict[str, Tuple[int, int]]:
        stats: Dict[str, Tuple[int, int]] = {}
        for i, pq in enumerate(self.questions):
            cat = pq.original.category or 'N/A'
            chosen = set(self.answers.get(i, []))
            actual = set(pq.correct_display_letters)
            c, t = stats.get(cat, (0, 0))
            if chosen == actual:
                c += 1
            t += 1
            stats[cat] = (c, t)
        return stats
