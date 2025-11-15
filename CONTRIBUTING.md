# Contributing to Haptique Extender Integration

First off, thank you for considering contributing to the Haptique Extender integration! It's people like you that make this integration better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a simple principle: **Be respectful and constructive**.

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**

- **Clear title** - Summarize the problem in the title
- **Detailed description** - Explain the problem in detail
- **Steps to reproduce** - List exact steps to reproduce the issue
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Environment details**:
  - Home Assistant version
  - Integration version
  - Haptique Extender firmware version
  - Browser (if UI-related)
- **Logs** - Include relevant logs with debug logging enabled
- **Screenshots** - If applicable

**Example:**
```markdown
## Bug: Learning mode timeout not working

**Description:**
The learning mode does not timeout after 30 seconds as expected.

**Steps to Reproduce:**
1. Call service `haptique_extender.learn_ir_command`
2. Do not press any remote button
3. Wait for 30 seconds
4. Learning mode remains active

**Expected:** Learning mode should timeout and fire `haptique_learning_timeout` event

**Actual:** Learning mode stays active indefinitely

**Environment:**
- HA: 2024.1.0
- Integration: 1.2.0
- Firmware: v2.1.0

**Logs:**
```
[log excerpt here]
```
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, include:**

- **Clear title** - Describe the enhancement
- **Detailed description** - Explain the feature
- **Use case** - Why would this be useful?
- **Proposed implementation** - How might this work?
- **Alternatives considered** - Other solutions you've thought about
- **Additional context** - Screenshots, mockups, examples

### Pull Requests

Pull requests are the best way to propose changes to the codebase.

**Good pull requests:**

- Address a single concern
- Include tests when adding new functionality
- Update documentation as needed
- Follow the coding style
- Include clear commit messages

## Development Setup

### Prerequisites

- Python 3.11 or later
- Home Assistant development environment
- Git
- Text editor or IDE (VS Code recommended)

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/haptique_extender.git
   cd haptique_extender
   ```

2. **Create a development branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up Home Assistant development environment:**
   
   **Option A: Using Home Assistant Core in venv**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install homeassistant
   ```

   **Option B: Using existing Home Assistant installation**
   - Link your development folder to custom_components
   ```bash
   ln -s /path/to/haptique_extender /config/custom_components/haptique_extender
   ```

4. **Install development dependencies:**
   ```bash
   pip install -r requirements_dev.txt  # If file exists
   ```

5. **Enable debug logging:**
   Add to your `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.haptique_extender: debug
   ```

### Testing Your Changes

1. **Restart Home Assistant** after making changes
2. **Check logs** for errors
3. **Test manually** with your Haptique Extender device
4. **Verify all functionality**:
   - Device discovery
   - Learning IR codes
   - Sending commands
   - Database operations
   - Notifications

### Project Structure

```
haptique_extender/
├── __init__.py              # Integration setup and services
├── manifest.json            # Integration metadata
├── config_flow.py           # Configuration UI flow
├── const.py                 # Constants and configuration
├── coordinator.py           # Data update coordinator
├── sensor.py                # Sensor platform
├── binary_sensor.py         # Binary sensor platform
├── switch.py                # Switch platform
├── ir_database.py           # IR command database manager
├── firmware_storage.py      # Firmware storage API helper
├── services.yaml            # Service definitions
├── strings.json             # UI strings (English)
└── translations/
    └── en.json              # Translation strings
```

## Coding Guidelines

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and Home Assistant coding standards.

**Key points:**

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter)
- Use type hints for function arguments and returns
- Use docstrings for all public functions and classes
- Import order: standard library, third-party, local imports

**Example:**
```python
"""Module docstring."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class ExampleEntity(Entity):
    """Example entity class."""

    def __init__(self, hass: HomeAssistant, name: str) -> None:
        """Initialize the entity.
        
        Args:
            hass: Home Assistant instance.
            name: Entity name.
        """
        self._hass = hass
        self._name = name
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Logging

Use appropriate log levels:

```python
_LOGGER.debug("Detailed information for debugging")
_LOGGER.info("General informational messages")
_LOGGER.warning("Warning messages for potential issues")
_LOGGER.error("Error messages for failures")
_LOGGER.exception("Error with traceback")
```

### Error Handling

Always handle exceptions appropriately:

```python
try:
    result = await self._request("GET", endpoint)
except aiohttp.ClientError as err:
    _LOGGER.error("Connection failed: %s", err)
    raise UpdateFailed(f"Request failed: {err}") from err
except Exception as err:
    _LOGGER.exception("Unexpected error: %s", err)
    raise
```

### Async/Await

- Use `async`/`await` for I/O operations
- Don't block the event loop
- Use `asyncio.create_task()` for background tasks

```python
async def async_method(self) -> dict[str, Any]:
    """Async method example."""
    result = await self.session.get(url)
    return await result.json()
```

### Type Hints

Always use type hints:

```python
def process_data(
    data: dict[str, Any],
    device_id: str,
    timeout: int = 30
) -> bool:
    """Process data with type hints."""
    ...
```

### Documentation

- Add docstrings to all public functions
- Use Google-style docstrings
- Include Args, Returns, Raises sections

```python
def send_command(
    self,
    device_id: str,
    command: str
) -> bool:
    """Send an IR command to a device.
    
    Args:
        device_id: The unique device identifier.
        command: The command name to send.
        
    Returns:
        True if command sent successfully, False otherwise.
        
    Raises:
        ValueError: If device_id or command is invalid.
    """
    ...
```

## Submitting Changes

### Commit Messages

Write clear, concise commit messages:

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example:**
```
feat: Add RF command support

- Implement RF code learning
- Add RF transmission service
- Update database schema for RF codes

Closes #123
```

### Pull Request Process

1. **Update documentation** if needed
2. **Test thoroughly** on your local setup
3. **Update CHANGELOG.md** with your changes
4. **Create the pull request**:
   - Use a clear title
   - Describe what changed and why
   - Reference any related issues
   - Include screenshots if UI changes

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested the changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Changes tested locally

## Related Issues
Closes #123
```

### Code Review

All submissions require review. Reviewers will check:

- Code quality and style
- Functionality and logic
- Error handling
- Documentation
- Test coverage

Be patient and responsive to feedback.

## Development Tips

### Useful Commands

**Restart Home Assistant:**
```bash
ha core restart
```

**Check logs in real-time:**
```bash
tail -f /config/home-assistant.log
```

**Validate configuration:**
```bash
ha core check
```

### Testing Checklist

Before submitting a PR, verify:

- [ ] Integration loads without errors
- [ ] Device discovery works
- [ ] Configuration flow works
- [ ] All entities are created
- [ ] Services work as expected
- [ ] Database operations work
- [ ] Notifications appear correctly
- [ ] No errors in logs
- [ ] Documentation is updated

### Common Pitfalls

1. **Blocking I/O**: Never use blocking I/O in async functions
2. **Error handling**: Always handle exceptions appropriately
3. **State updates**: Use `async_write_ha_state()` to update entity states
4. **Coordinator**: Use coordinator for data updates, not individual entities
5. **Translations**: Keep strings in `strings.json` and `translations/en.json`

## Release Process

Releases are managed by maintainers:

1. Version bump in `manifest.json`
2. Update `CHANGELOG.md`
3. Create GitHub release
4. Tag with version number

## Questions?

- Check existing issues and discussions
- Ask in [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
- Refer to [Home Assistant Developer Docs](https://developers.home-assistant.io/)

## Recognition

Contributors will be:
- Listed in release notes
- Mentioned in README credits
- Appreciated by the community!

---

Thank you for contributing to Haptique Extender! 🎉
