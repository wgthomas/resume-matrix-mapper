# Contributing to Resume-to-Matrix Mapper

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](../../issues) section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git fork https://github.com/YOUR_USERNAME/resume-matrix-mapper.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python test_skill.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Brief description of what you added"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what you changed and why
   - Reference any related issues
   - Wait for review

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Documentation

- Update README.md if you change functionality
- Add examples for new features
- Keep SKILL.md in sync with code changes
- Update references/ if you add new patterns

### Testing

- Run `python test_skill.py` before submitting
- Add tests for new features
- Ensure existing tests still pass

### Commit Messages

Use clear, descriptive commit messages:

```
Add: Description of what was added
Fix: Description of what was fixed
Update: Description of what was updated
Remove: Description of what was removed
Refactor: Description of refactoring
Docs: Description of documentation changes
```

## Areas for Contribution

### High Priority

- [ ] Add support for PDF resumes
- [ ] Improve date parsing for international formats
- [ ] Add more domain-specific matching patterns
- [ ] Enhance error handling and user feedback

### Nice to Have

- [ ] Web interface for testing
- [ ] Integration with popular ATS systems
- [ ] Batch processing improvements
- [ ] Additional output formats

### Documentation

- [ ] Video tutorials
- [ ] More examples for different industries
- [ ] Troubleshooting guide expansion
- [ ] API documentation

## Questions?

- Check [SKILL.md](SKILL.md) for technical details
- Review [references/](references/) for patterns and examples
- Ask questions in the [Discussions](../../discussions) section
- Open an issue if you need clarification

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best outcome for the project
- Help others learn and grow

Thank you for contributing! 🎉
