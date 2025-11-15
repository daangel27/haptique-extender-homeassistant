# Documentation Index - Haptique Extender Integration

This document provides an overview of all available documentation for the Haptique Extender Home Assistant integration.

## 📚 Documentation Structure

### Essential Reading (Start Here!)

1. **[README.md](README.md)** - Main documentation
   - Overview and features
   - Complete usage guide
   - Service reference
   - Troubleshooting
   - **Read this first!**

2. **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
   - Step-by-step setup
   - Quick tutorial
   - Essential commands
   - Common examples
   - **Perfect for beginners!**

3. **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
   - Multiple installation methods
   - Package file setup
   - Configuration details
   - Verification steps
   - **For complete setup instructions**

### Reference Documentation

4. **[FAQ.md](FAQ.md)** - Frequently Asked Questions
   - Common questions and answers
   - Organized by topic
   - Troubleshooting tips
   - Advanced usage examples
   - **Check here if you have questions!**

5. **[CHANGELOG.md](CHANGELOG.md)** - Version history
   - What's new in each version
   - Breaking changes
   - Bug fixes
   - Future roadmap
   - **See what's changed**

### Contributing & Community

6. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
   - How to contribute
   - Development setup
   - Coding standards
   - Pull request process
   - **For developers and contributors**

7. **[LICENSE](LICENSE)** - MIT License
   - Usage terms
   - Distribution rights
   - Liability disclaimers

### GitHub Templates

8. **[.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)**
   - Template for reporting bugs
   - Ensures consistent bug reports

9. **[.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)**
   - Template for suggesting features
   - Helps structure feature proposals

10. **[.github/pull_request_template.md](.github/pull_request_template.md)**
    - Template for pull requests
    - Ensures consistent PR submissions

### Configuration Files

11. **[.gitignore](.gitignore)**
    - Git ignore rules
    - Prevents committing sensitive data

## 🗺️ Documentation Flowchart

```
START
  │
  ├─── New User? ──────────► QUICK_START.md ──► README.md
  │
  ├─── Installing? ────────► INSTALLATION.md ──► QUICK_START.md
  │
  ├─── Have Question? ─────► FAQ.md ──► README.md (Troubleshooting)
  │
  ├─── Want to Contribute? ► CONTRIBUTING.md ──► CHANGELOG.md
  │
  ├─── Found a Bug? ───────► FAQ.md ──► .github/ISSUE_TEMPLATE/bug_report.md
  │
  └─── Feature Idea? ──────► .github/ISSUE_TEMPLATE/feature_request.md
```

## 📖 Reading Guide by User Type

### For First-Time Users
1. [QUICK_START.md](QUICK_START.md) - Get running in 5 minutes
2. [README.md](README.md) - Learn all features
3. [FAQ.md](FAQ.md) - Common questions

### For Installing the Integration
1. [INSTALLATION.md](INSTALLATION.md) - Complete installation guide
2. [README.md](README.md#configuration) - Configuration details
3. [QUICK_START.md](QUICK_START.md) - Quick verification

### For Troubleshooting Issues
1. [FAQ.md](FAQ.md#troubleshooting) - Common problems
2. [README.md](README.md#troubleshooting) - Detailed troubleshooting
3. [bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md) - Report if unresolved

### For Advanced Users
1. [README.md](README.md#services) - All services
2. [FAQ.md](FAQ.md#advanced-usage) - Advanced examples
3. [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup

### For Contributors
1. [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
2. [README.md](README.md#credits) - Project structure
3. [CHANGELOG.md](CHANGELOG.md) - Version history

## 📝 Quick Reference by Topic

### Installation & Setup
- Installation methods: [INSTALLATION.md](INSTALLATION.md#installation-methods)
- Package files: [INSTALLATION.md](INSTALLATION.md#package-files-setup)
- Getting token: [QUICK_START.md](QUICK_START.md#step-2-get-your-token-1-minute)
- First configuration: [README.md](README.md#configuration)

### Learning IR Commands
- Quick tutorial: [QUICK_START.md](QUICK_START.md#learn-your-first-command-30-seconds)
- Detailed guide: [README.md](README.md#learning-ir-commands)
- Troubleshooting: [FAQ.md](FAQ.md#ir-learning)

### Sending Commands
- Quick example: [QUICK_START.md](QUICK_START.md#send-your-first-command-10-seconds)
- Service reference: [README.md](README.md#ir-sending-services)
- Advanced usage: [FAQ.md](FAQ.md#command-sending)

### Database Management
- Overview: [README.md](README.md#database-management-services)
- Backup guide: [FAQ.md](FAQ.md#should-i-backup-the-database)
- Organization tips: [FAQ.md](FAQ.md#how-many-commands-can-i-store)

### Automations & Scripts
- Examples: [QUICK_START.md](QUICK_START.md#quick-examples)
- Advanced: [FAQ.md](FAQ.md#advanced-usage)
- Voice control: [FAQ.md](FAQ.md#can-i-integrate-with-voice-assistants)

### Troubleshooting
- Common issues: [FAQ.md](FAQ.md#troubleshooting)
- Debug logging: [README.md](README.md#logs-and-debugging)
- Connection issues: [FAQ.md](FAQ.md#device--connection)

## 🔍 Search by Keyword

### Authentication
- Getting token: [QUICK_START.md](QUICK_START.md#step-2-get-your-token-1-minute)
- Token issues: [FAQ.md](FAQ.md#how-do-i-get-the-authentication-token)

### Database
- Location: [FAQ.md](FAQ.md#where-is-the-ir-command-database-stored)
- Backup: [FAQ.md](FAQ.md#should-i-backup-the-database)
- Manual editing: [FAQ.md](FAQ.md#can-i-edit-the-database-manually)

### Debugging
- Enable logging: [FAQ.md](FAQ.md#how-do-i-enable-debug-logging)
- View logs: [README.md](README.md#logs-and-debugging)
- Common errors: [FAQ.md](FAQ.md#troubleshooting)

### Discovery
- Auto-discovery: [README.md](README.md#automatic-discovery-recommended)
- Manual setup: [INSTALLATION.md](INSTALLATION.md#option-2-manual-configuration)
- Issues: [FAQ.md](FAQ.md#why-isnt-my-device-auto-discovered)

### Entities
- List of entities: [README.md](README.md#entities-created)
- Entity naming: [FAQ.md](FAQ.md#entity-names-dont-match-the-examples-why)

### Learning Mode
- How to use: [QUICK_START.md](QUICK_START.md#learn-your-first-command-30-seconds)
- Troubleshooting: [FAQ.md](FAQ.md#why-isnt-my-ir-code-being-captured)
- Timeout settings: [FAQ.md](FAQ.md#how-long-does-learning-mode-stay-active)

### Notifications
- Setup: [INSTALLATION.md](INSTALLATION.md#4-configure-notifications-optional)
- Not appearing: [FAQ.md](FAQ.md#notifications-arent-appearing-why)

### Packages
- What they are: [FAQ.md](FAQ.md#do-i-need-to-install-package-files)
- Installation: [INSTALLATION.md](INSTALLATION.md#package-files-setup)
- Not loading: [FAQ.md](FAQ.md#package-files-not-loading)

### Services
- Quick reference: [QUICK_START.md](QUICK_START.md#essential-services-quick-reference)
- Complete list: [README.md](README.md#services)
- Examples: [FAQ.md](FAQ.md#advanced-usage)

## 📞 Getting Help

### Self-Help Resources
1. Check [FAQ.md](FAQ.md) first
2. Search [README.md](README.md) for your topic
3. Review [INSTALLATION.md](INSTALLATION.md) if setup issue
4. Enable debug logging and check logs

### Community Support
1. Browse [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
2. Search [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
3. Post a question in Discussions (not Issues)

### Reporting Problems
1. Check if already reported in Issues
2. Follow [bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md) template
3. Include logs with debug enabled
4. Be specific and detailed

### Suggesting Features
1. Check if already suggested in Issues
2. Follow [feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md) template
3. Explain use case clearly
4. Consider contributing implementation

## 🎯 Documentation Priorities

### Must Read
- ⭐⭐⭐ [README.md](README.md)
- ⭐⭐⭐ [QUICK_START.md](QUICK_START.md)

### Should Read
- ⭐⭐ [INSTALLATION.md](INSTALLATION.md)
- ⭐⭐ [FAQ.md](FAQ.md)

### Reference When Needed
- ⭐ [CHANGELOG.md](CHANGELOG.md)
- ⭐ [CONTRIBUTING.md](CONTRIBUTING.md)

## 📦 Complete File List

```
Documentation/
├── README.md                           # Main documentation (START HERE)
├── QUICK_START.md                      # 5-minute getting started guide
├── INSTALLATION.md                     # Detailed installation guide
├── FAQ.md                             # Frequently asked questions
├── CHANGELOG.md                        # Version history
├── CONTRIBUTING.md                     # Contribution guidelines
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── DOCUMENTATION_INDEX.md             # This file
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md              # Bug report template
    │   └── feature_request.md         # Feature request template
    └── pull_request_template.md       # Pull request template
```

## 🔄 Keeping Documentation Updated

This documentation is maintained alongside the integration code. When contributing:

1. Update relevant documentation files
2. Keep examples current
3. Add new sections as needed
4. Update CHANGELOG.md
5. Test all examples

## 📧 Feedback

Help us improve the documentation! If you find:
- Errors or typos
- Unclear explanations
- Missing information
- Broken links

Please open an issue or submit a pull request.

## 🌟 Contributing to Documentation

Documentation improvements are always welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to submit changes
- Documentation standards
- Review process

---

**Last Updated:** 2025  
**Documentation Version:** 1.2.0  
**Integration Version:** 1.2.0

**Thank you for using Haptique Extender!** 🎉
