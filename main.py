
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from settings import Settings
from models import QuestionBank
from exam import ExamSession
from ui.landing import LandingScreen
from ui.customization import CustomizationScreen
from ui.exam_window import ExamScreen
from ui.results import ResultsScreen

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Question Generator Program")
        # Maximized window (platform-friendly)
        try:
            self.root.state('zoomed')
        except Exception:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")
        # Global styles
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', 12))
        # State
        self.settings = Settings(Path('settings.json'))
        self.settings.load()
        self.bank_name = 'N/A'
        self.session: ExamSession = None
        # Screens
        self.container = ttk.Frame(root)
        self.container.pack(fill='both', expand=True)
        self.screens = {}
        for name, cls in [('landing', LandingScreen), ('customization', CustomizationScreen), ('exam', ExamScreen), ('results', ResultsScreen)]:
            frame = cls(self.container, self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.screens[name] = frame
        self.show_screen('landing')

    def show_screen(self, name: str):
        frame = self.screens[name]
        frame.tkraise()
        # Special populate hooks
        if name == 'results':
            frame.populate()
        if name == 'exam':
            try:
                frame.on_show()
            except Exception:
                pass

    def start_exam(self):
        # Load bank, filter by categories, create session
        path = Path(self.settings.data['bank_path'])
        bank = QuestionBank(path)
        valid_count, skipped = bank.load()
        selected = self.settings.data.get('selected_categories')
        if not selected:
            # default: all categories
            selected = bank.categories
        filtered = [q for q in bank.questions if (q.category or 'N/A') in selected]
        num_q = self.settings.data.get('num_questions', 10)
        self.session = ExamSession(filtered, num_q)
        self.session.start()
        self.bank_name = path.name
        self.show_screen('exam')

    def finish_exam(self):
        self.show_screen('results')

    def quit(self):
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
