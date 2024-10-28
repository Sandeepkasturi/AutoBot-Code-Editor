import sys
import subprocess
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QPushButton, QTextBrowser, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
    QProgressBar, QTextEdit, QTabWidget
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerJava
from google.generativeai import configure, GenerativeModel
from PyQt5.QtCore import QThread, pyqtSignal

# Replace with your actual API Key
configure(api_key="YOUR_API_KEY")
model = GenerativeModel('gemini-pro')


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    result_ready = pyqtSignal(str, str)

    def __init__(self, language, code, filename):
        super().__init__()
        self.language = language
        self.code = code
        self.filename = filename

    def run(self):
        try:
            with open(self.filename, "w", encoding='utf-8') as f:
                f.write(self.code)

            self.update_progress.emit(50)  # Update progress to 50%

            if self.language == "Python":
                result = subprocess.run(
                    ["python3", self.filename],
                    capture_output=True,
                    text=True,
                    timeout=20
                )
            elif self.language == "Java":
                compile_result = subprocess.run(
                    ["javac", self.filename],
                    capture_output=True,
                    text=True
                )
                if compile_result.stderr:  # Compilation error
                    self.result_ready.emit("", compile_result.stderr)
                    return

                class_name = self.filename.replace(".java", "")
                result = subprocess.run(
                    ["java", class_name],
                    capture_output=True,
                    text=True
                )

            self.result_ready.emit(result.stdout, result.stderr)
        except Exception as e:
            self.result_ready.emit("", f"An unexpected error occurred: {e}")


class CodeCompilerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set application icon
        self.setWindowIcon(QIcon('code.png'))  # Update with your icon path

        # Window setup
        self.setWindowTitle("Autobot Code Compiler")
        self.setGeometry(100, 100, 1500, 900)

        # Apply Night Owl theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #011627;  /* Dark background */
                font-family: 'Courier New';  /* Consistent font */
            }
            QLabel {
                color: #d6deeb;  /* Light text color */
                font-size: 14px;  /* Font size */
                margin: 5px;  /* Margin for spacing */
            }
            QComboBox {
                background-color: #011627;  /* Dark background for combo box */
                color: #d6deeb;  /* Light text color */
                border: 1px solid #5f7e97;  /* Border color */
                border-radius: 8px;  /* Rounded corners */
                padding: 5px;  /* Padding for better spacing */
                font-size: 14px;  /* Font size */
            }
            QComboBox::drop-down {
                border: none;  /* No border for dropdown */
            }
            QPushButton {
                background-color: #82aaff;  /* Button background */
                color: #011627;  /* Button text color */
                border-radius: 12px;  /* Rounded corners */
                padding: 10px;  /* Padding for better spacing */
                font-size: 16px;  /* Larger font size */
                font-weight: bold;  /* Bold text */
                transition: background-color 0.3s;  /* Smooth transition for hover effect */
            }
            QPushButton:hover {
                background-color: #7e57c2;  /* Change color on hover */
            }
            QProgressBar {
                background-color: #011627;  /* Dark background */
                border: 1px solid #5f7e97;  /* Border color */
                border-radius: 10px;  /* Rounded corners */
                text-align: center;  /* Centered text */
                height: 20px;  /* Height of progress bar */
            }
            QProgressBar::chunk {
                background-color: #82aaff;  /* Chunk color */
                border-radius: 10px;  /* Rounded corners for chunk */
            }
            QTextEdit {
                background-color: #011627;  /* Dark background */
                color: #d6deeb;  /* Light text color */
                border: 1px solid #5f7e97;  /* Border color */
                border-radius: 8px;  /* Rounded corners */
                padding: 10px;  /* Padding for better spacing */
            }
            QTextBrowser {
                background-color: #011627;  /* Dark background */
                color: #d6deeb;  /* Light text color */
                border: 1px solid #5f7e97;  /* Border color */
                border-radius: 8px;  /* Rounded corners */
                padding: 10px;  /* Padding for better spacing */
            }
        """)

        # Tab widget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Create Compiler Tab
        self.compiler_tab = QWidget()
        self.create_compiler_tab()

        # Create AI Code Generator Tab
        self.ai_code_generator_tab = QWidget()
        self.create_ai_code_generator_tab()

        # Add tabs to the TabWidget
        self.tab_widget.addTab(self.compiler_tab, "Code Compiler")
        self.tab_widget.addTab(self.ai_code_generator_tab, "AI CODE GENERATOR")

    def create_compiler_tab(self):
        # Language selection dropdown
        self.language_selector = QComboBox(self)
        self.language_selector.addItems(["Python", "Java"])
        self.language_selector.currentIndexChanged.connect(self.on_language_change)

        # Code editor using QScintilla
        self.code_editor = QsciScintilla(self)
        self.code_editor.setLexer(QsciLexerPython())
        self.code_editor.setText("print('Hello, World!')")  # Sample Python code
        self.code_editor.setFont(QFont('Courier New', 15))
        self.code_editor.setStyleSheet("background-color: #011627; color: #d6deeb;")  # Dark theme

        # Output display
        self.output_display = QTextBrowser(self)
        self.output_display.setFont(QFont('Courier', 15))

        # Compile and run button
        self.run_button = QPushButton("Compile and Run Code", self)
        self.run_button.clicked.connect(self.run_code)

        # AI ask button
        self.ask_ai_button = QPushButton("Ask AI", self)
        self.ask_ai_button.clicked.connect(self.ask_ai)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Layout for left side (code editor)
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Choose Language:"))
        left_layout.addWidget(self.language_selector)
        left_layout.addWidget(QLabel("Code Editor:"))
        left_layout.addWidget(self.code_editor)
        left_layout.addWidget(self.run_button)
        left_layout.addWidget(self.ask_ai_button)

        # Layout for right side (output display)
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Output:"))
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.output_display)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        self.compiler_tab.setLayout(main_layout)

    def create_ai_code_generator_tab(self):
        # AI Code Generator components
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")

        # Buttons
        self.ai_generate_button = QPushButton("Ask AI")
        self.copy_code_button = QPushButton("Copy Code")
        self.insert_code_button = QPushButton("Insert Code")

        # Connect buttons to their actions
        self.ai_generate_button.clicked.connect(self.generate_code_from_prompt)
        self.copy_code_button.clicked.connect(self.copy_code)
        self.insert_code_button.clicked.connect(self.insert_code)

        # Generated AI code display
        self.generated_code_display = QTextBrowser()
        self.generated_code_display.setFont(QFont('Times of Roman', 15))

        # Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("AI Code Generator:"))
        left_layout.addWidget(self.prompt_input)
        left_layout.addWidget(self.ai_generate_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Generated Code:"))
        right_layout.addWidget(self.generated_code_display)
        right_layout.addWidget(self.copy_code_button)
        right_layout.addWidget(self.insert_code_button)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        self.ai_code_generator_tab.setLayout(main_layout)

    def on_language_change(self):
        language = self.language_selector.currentText()
        if language == "Python":
            self.code_editor.setLexer(QsciLexerPython())
            self.code_editor.setText("""# A simple python code to print Hello World

print("Hello world!")""")
        else:
            self.code_editor.setLexer(QsciLexerJava())
            self.code_editor.setText("""// A Java Program to print Hello World

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}""")

    def generate_code_from_prompt(self):
        prompt = self.prompt_input.toPlainText()
        # Check for prohibited delimiters
        prohibited_delimiters = ["```java", "```python", "'''", "```"]

        if any(delimiter in prompt for delimiter in prohibited_delimiters):
            self.generated_code_display.setHtml(
                "<font color='red'>Error: Prohibited delimiters detected. Please remove them from your prompt.</font>")
            return

        if prompt:
            try:
                response = model.generate_content(prompt)
                self.generated_code_display.setHtml(f"<pre>{response.text}</pre>")
            except Exception as e:
                self.generated_code_display.setHtml(f"<font color='red'>Error: {e}</font>")

    def copy_code(self):
        QApplication.clipboard().setText(self.generated_code_display.toPlainText())

    def insert_code(self):
        generated_code = self.generated_code_display.toPlainText()
        # Remove prohibited delimiters
        prohibited_delimiters = ["```java", "```python", "'''", "```"]
        for delimiter in prohibited_delimiters:
            generated_code = generated_code.replace(delimiter, "")
        # Insert sanitized code into the code editor
        self.code_editor.setText(generated_code)

    def run_code(self):
        code = self.code_editor.text()
        language = self.language_selector.currentText()

        # Determine the filename based on the language and the class name in the code
        if language == "Python":
            filename = "main.py"
        else:  # For Java
            class_name = self.extract_class_name(code)
            if class_name:
                filename = f"{class_name}.java"
            else:
                self.output_display.setPlainText("Error: No public class found in Java code.")
                return

        # Create a worker thread to compile and run the code
        self.worker = WorkerThread(language, code, filename)
        self.worker.update_progress.connect(self.update_progress)
        self.worker.result_ready.connect(self.display_result)
        self.worker.start()  # Start the thread

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_result(self, output, error):
        self.output_display.setPlainText(f"Output:\n{output}\n\nErrors:\n{error}")
        self.progress_bar.setValue(100)  # Set progress to complete

    def extract_class_name(self, code):
        match = re.search(r'public\s+class\s+(\w+)', code)
        return match.group(1) if match else None

    def ask_ai(self):
        code = self.code_editor.text()
        custom_prompt = f"I have written the following code in {self.language_selector.currentText()}:\n\n{code}\n\nCan you provide Expected output same as traditional compilers and at the end code explanation?"

        try:
            response = model.generate_content(custom_prompt)
            formatted_response = f"<strong>AI Response:</strong><br><pre>{response.text}</pre>"
            self.output_display.setHtml(formatted_response)
        except Exception as e:
            self.output_display.setHtml(f"<font color='red'>Error: {e}</font>")


def main():
    app = QApplication(sys.argv)
    window = CodeCompilerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
