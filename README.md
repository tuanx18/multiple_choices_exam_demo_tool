
# Question Generator Program (Python, Tkinter)

A full-screen, responsive quiz/exam application that uses JSON question banks to generate multiple-choice quizzes. It includes:

- **Screen 1: Landing Window** – Start Exam, Customization/Settings, Quit
- **Screen 2: Exam Window** – One question per screen, timer, navigation (Previous/Next), bottom actions (Back to main menu, Pause/Resume, Submit), tooltips, keyboard navigation (←/→)
- **Screen 3: Customization/Settings** – Choose JSON bank, select categories, number of questions, pass percentage; settings are persisted to `settings.json`
- **Results Screen** – Summary (score, pass/fail, time), per-question reasoning, and basic metrics

## How to run

1. Ensure you have Python 3.8+.
2. From a terminal in the project folder:

```bash
python3 main.py
```

## JSON Bank Schema & Validation
Each question block must pass validation:
```json
{
  "question_id": 1234,                    // Integer (autonumber acceptable)
  "category": "technology",              // String
  "question": "What is X?",             // String
  "correct_answer": ["A", "C"],         // String single letter OR list of single-letter strings
  "choices": ["X is 123", "X is 234"], // List of 2..12 strings
  "reasoning": "Because X",             // String
  "difficulty": 5,                        // Integer 1..5
  "can_shuffle": true                     // Boolean
}
```
Blank attributes are displayed as **N/A** in the UI. Invalid questions are skipped with a warning.

## Keyboard Shortcuts
- **Left Arrow**: Previous question
- **Right Arrow**: Next question

## Files
- `main.py` – application entry point
- `models.py` – data classes & validation
- `exam.py` – exam session management
- `settings.py` – settings persistence
- `ui/landing.py`, `ui/exam_window.py`, `ui/customization.py`, `ui/results.py` – UI screens
- `ui/widgets.py` – common widgets (tooltips, scrollable frame)
- `assets/sample_banks/tech.json` – sample bank

## Notes
- Maximized window by default; fonts ≥ ~15px.
- All buttons have tooltips.
- Submit confirmation warns about unanswered questions.
- Choices are shuffled if `can_shuffle` is `true` and the correct answers are remapped accordingly.

## Screenshots

1. Landing Interface

<img width="713" height="501" alt="image" src="https://github.com/user-attachments/assets/2bd01d3f-99dc-4710-ba65-807eca8cb3b3" />

2.  Customization

<img width="1692" height="825" alt="image" src="https://github.com/user-attachments/assets/bc95742f-cc27-40bd-90ba-a5b8e2ec8404" />

3. Sample questions

<img width="1617" height="922" alt="image" src="https://github.com/user-attachments/assets/3376b717-8ab3-4e0d-9900-27b06097a6f3" />

4. Exam Results

<img width="1642" height="930" alt="image" src="https://github.com/user-attachments/assets/113136ab-ef0b-43c6-8929-467a39496112" />

## HAVE FUN LEARNING!

