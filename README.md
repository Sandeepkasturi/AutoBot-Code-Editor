# Autobot Code Compiler

Autobot Code Compiler is a PyQt5-based application designed to compile and run Python and Java code within a customized Night Owl-themed GUI. It also integrates with Google Generative AI for additional assistance in generating code or explaining the code logic.

## Features
- **Python and Java Compiler**: Compile and execute Python and Java code with a click.
- **Code Editor with Night Owl Theme**: A custom-themed QScintilla-based editor with syntax highlighting.
- **AI Integration**: Google Generative AI integration allows you to generate, evaluate, or ask questions about code directly within the application.
- **Dynamic Output Display**: View both compilation output and AI responses in a structured format.
- **Progress Tracking**: Real-time progress updates while running or compiling code.

## Installation

1. **Clone the Repository** (or download the code directly):
   
   git clone https://github.com/sandeepkasturi/autobot-Code-Editor/.git
   cd autobot-code-editor
   
2. **Install Dependencies**:
   Install all necessary Python packages from the `requirements.txt` file using pip:

   pip install -r requirements.txt
   
4. **Set up API Key**:
   Update the API key for Google Generative AI in the code:
      # Replace with your actual API Key
   configure(api_key="YOUR_GOOGLE_API_KEY")
   

5. **Run the Application**:
   Start the application by running:
   
   python app.py
   

## Usage

1. Select the programming language (Python or Java) from the dropdown.
2. Write or paste your code into the editor.
3. Click "Compile and Run Code" to execute and see the output on the right.
4. To leverage the AI-powered code generator, switch to the AI Code Generator tab, enter a prompt, and click "Ask AI."
5. Use "Copy Code" or "Insert Code" for generated code directly within your code editor.

## Dependencies

- **PyQt5**: GUI toolkit for the application's front-end components.
- **QsciScintilla**: Provides syntax highlighting for the Python and Java code editor.
- **google-generativeai**: Accesses the Google Generative AI API to provide real-time code generation and explanations.

## License

This project is licensed under the GNU License. Feel free to customize and distribute!

## Troubleshooting

- Ensure your internet connection is stable for AI generation.
- For Java compilation, ensure `javac` and `java` commands are accessible in your environment variables (PATH).


### Notes:
Make sure you replace `"YOUR_GOOGLE_API_KEY"` in the 'app.py' with the actual API key. 


### Download the Executable GUI file from here: [https://drive.google.com/file/d/1YnUoEwKhf0chT73OTl2V6L_00yVlHLmU/view?usp=sharing()]
