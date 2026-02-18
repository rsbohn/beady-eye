# Contributing to beady-eye

Thank you for your interest in contributing to beady-eye! This document provides guidelines and information for contributors.

## Project Status

beady-eye is currently in early development (proof of concept stage). We're working towards an MVP (Minimum Viable Product). See [MVP_PLAN.md](MVP_PLAN.md) for the complete roadmap.

## How to Contribute

### Reporting Issues
- Check if the issue already exists
- Provide clear description and steps to reproduce
- Include browser and version information
- Add screenshots if applicable

### Suggesting Features
- Check the [MVP_PLAN.md](MVP_PLAN.md) first - your feature might already be planned
- Open an issue with the label "enhancement"
- Describe the use case and expected behavior
- Explain how it aligns with displayio concepts

### Submitting Code

#### Before You Start
1. Check [MVP_PLAN.md](MVP_PLAN.md) for planned features
2. Open an issue to discuss significant changes
3. Fork the repository
4. Create a feature branch

#### Development Guidelines

**Code Style**
- Use clear, descriptive variable names
- Follow existing code patterns
- Add comments for complex logic
- Keep functions small and focused

**API Design**
- Follow displayio naming conventions where applicable
- Keep the API simple and intuitive
- Maintain consistency with existing features
- Document all public APIs

**Testing**
- Add tests for new features (once test framework is set up)
- Ensure existing examples still work
- Test in multiple browsers

#### Pull Request Process
1. Update documentation for your changes
2. Add/update examples if relevant
3. Ensure code follows project style
4. Test in at least 2 modern browsers
5. Provide clear PR description
6. Link related issues

## Development Setup

Currently, the project has no build system. Simply:
1. Clone the repository
2. Open `index.html` in a browser
3. Make your changes
4. Test by refreshing the browser

A proper build system will be added in Phase 1 of the MVP.

## Priority Areas

For MVP, we're prioritizing:
1. **Core shapes** - Circle, Line, Polygon (Phase 1)
2. **Text support** - Label implementation (Phase 2)
3. **Color management** - RGB, hex, palettes (Phase 2)
4. **Documentation** - API docs, examples (Ongoing)

See [MVP_PLAN.md](MVP_PLAN.md) for complete priorities.

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Questions?

Open an issue with your question, or reach out to the maintainer.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Future CONTRIBUTORS.md file
- Release notes for significant contributions

Thank you for helping make beady-eye better!
