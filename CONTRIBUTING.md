# Contributing to Debt Empire v2.0

Thank you for your interest in contributing!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/muddusurendranehru/debt-empire.git
   cd debt-empire
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Development:**
   ```bash
   # Use the one-click startup script
   ./local-run.sh  # Linux/Mac
   # OR
   local-run.bat    # Windows
   ```

## Safety Rules

Please follow these safety rules when contributing:

1. **VALIDATE:** Always validate CSV columns before processing
2. **NO ASSUME:** Never assume missing data - ask for confirmation
3. **SLOW:** Verify each step with approval prompts
4. **ERRORS:** Use try/except + logging + STOP on errors
5. **FACTS:** Only cite actual files, no assumptions
6. **NO SEND:** Generate drafts only (user handles sending)
7. **2 Servers:** Frontend (3000) | Backend (8000)

## Code Style

- Follow PEP 8 for Python code
- Use TypeScript/ESLint for JavaScript
- Add docstrings to all functions
- Include error handling

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Questions?

Open an issue for questions or suggestions.
