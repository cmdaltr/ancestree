# 📋 Release Checklist

Use this checklist when preparing a new release of AncesTree.

---

## Pre-Release

### Code & Testing
- [ ] All tests passing
- [ ] Code reviewed
- [ ] No known critical bugs
- [ ] Version number updated in:
  - [ ] `ancestree.spec`
  - [ ] `package.json` (frontend)
  - [ ] Documentation

### Documentation
- [ ] README.md up to date
- [ ] USER_GUIDE.md reflects current features
- [ ] TECHNICAL_GUIDE.md updated
- [ ] CHANGELOG.md updated (if you have one)
- [ ] All links working

---

## Building Executables

### Windows Build
- [ ] Built on Windows machine (or VM)
- [ ] Run `build_windows.bat`
- [ ] Test `AncesTree.exe` on clean Windows machine
- [ ] Test with Docker Desktop installed
- [ ] Test without Docker Desktop (should show error)
- [ ] No antivirus false positives (check VirusTotal)
- [ ] File size reasonable (~25-35 MB)

### macOS Build
- [ ] Built on Mac machine
- [ ] Run `./build_macos.sh`
- [ ] Test `AncesTree.app` on clean Mac
- [ ] Test `AncesTree.pkg` installation
- [ ] Test on latest macOS version
- [ ] Test on minimum supported macOS version (10.13+)
- [ ] Code signed (if possible)
- [ ] Notarized (if possible)
- [ ] File sizes reasonable (~30-40 MB)

### Linux Build
- [ ] Built on Linux machine (or VM)
- [ ] Run `./build_linux.sh`
- [ ] Test `AncesTree-x86_64.AppImage` on Ubuntu
- [ ] Test on Fedora (optional)
- [ ] Test on other distros (optional)
- [ ] Made executable by default
- [ ] File size reasonable (~35-45 MB)

---

## Testing

### Functional Testing
- [ ] Can start application
- [ ] Docker detection works
- [ ] Browser auto-opens
- [ ] Can register new account
- [ ] Can login
- [ ] Can add family member
- [ ] Can edit family member
- [ ] Can delete family member
- [ ] Can upload photo/document
- [ ] Family tree displays correctly
- [ ] Search functionality works (if API keys configured)

### Platform Testing
- [ ] Tested on Windows 10/11
- [ ] Tested on macOS 12+ (Monterey)
- [ ] Tested on Ubuntu 22.04 LTS
- [ ] Mobile browser tested (responsive design)

### Error Handling
- [ ] Clear error if Docker not installed
- [ ] Clear error if Docker not running
- [ ] Clear error if ports in use
- [ ] Network error handling works
- [ ] Invalid login shows proper message

---

## Release Package

### Files to Include
- [ ] `AncesTree.exe` (Windows)
- [ ] `AncesTree.pkg` (macOS installer)
- [ ] `AncesTree.app.zip` (macOS app bundle, zipped)
- [ ] `AncesTree-x86_64.AppImage` (Linux)
- [ ] `START_HERE.md`
- [ ] `USER_GUIDE.md`
- [ ] `QUICK_START.md`
- [ ] `RELEASE_NOTES.md` (create for this version)
- [ ] `LICENSE` (if you have one)

### File Checksums
Create checksums for verification:
```bash
# SHA256 checksums
sha256sum AncesTree.exe > checksums.txt
sha256sum AncesTree.pkg >> checksums.txt
sha256sum AncesTree-x86_64.AppImage >> checksums.txt
```

- [ ] Checksums file created and included

---

## GitHub Release

### Preparation
- [ ] Tag created: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Tag pushed: `git push origin vX.Y.Z`
- [ ] Release notes written
- [ ] Screenshots updated (if UI changed)

### Release Page
- [ ] Create new release on GitHub
- [ ] Title: `AncesTree vX.Y.Z`
- [ ] Release notes include:
  - [ ] What's new
  - [ ] Bug fixes
  - [ ] Known issues
  - [ ] Installation instructions
  - [ ] Docker Desktop requirement
  - [ ] Platform-specific notes

### Upload Files
Upload to GitHub Release:
- [ ] `AncesTree.exe`
- [ ] `AncesTree.pkg`
- [ ] `AncesTree.app.zip`
- [ ] `AncesTree-x86_64.AppImage`
- [ ] `START_HERE.md`
- [ ] `USER_GUIDE.md`
- [ ] `checksums.txt`
- [ ] Source code (automatic)

### File Descriptions
Add descriptions for each file:
- [ ] Windows: "Windows executable - Just download and run"
- [ ] macOS PKG: "macOS installer - Double-click to install"
- [ ] macOS APP: "macOS application - Unzip and drag to Applications"
- [ ] Linux: "Linux AppImage - Make executable and run"

---

## Post-Release

### Verification
- [ ] Download each file from GitHub
- [ ] Verify checksums match
- [ ] Test each downloaded file
- [ ] Verify download counts work

### Communication
- [ ] Announcement written
- [ ] Social media posts (if applicable)
- [ ] Email to users (if applicable)
- [ ] Update project website (if applicable)

### Monitoring
- [ ] Monitor GitHub issues for bug reports
- [ ] Check download statistics
- [ ] Respond to user feedback
- [ ] Update documentation if issues found

---

## Security

### Before Release
- [ ] No hardcoded secrets in code
- [ ] `.env.example` has no real values
- [ ] Database files excluded from build
- [ ] Dependencies up to date
- [ ] Known vulnerabilities addressed
- [ ] Security scanning completed (optional)

### Signing (If Available)
- [ ] Windows executable signed
- [ ] macOS app signed
- [ ] macOS app notarized
- [ ] Linux AppImage signed (optional)

---

## Version Specific Notes

### vX.Y.Z Release

**Release Date:** YYYY-MM-DD

**Special Notes:**
- (Add any version-specific information here)

**Breaking Changes:**
- (List any breaking changes)

**Migration Notes:**
- (Add migration instructions if needed)

---

## Template: Release Announcement

```markdown
# 🎉 AncesTree vX.Y.Z Released!

We're excited to announce the release of AncesTree vX.Y.Z!

## 🆕 What's New

- Feature 1
- Feature 2
- Feature 3

## 🐛 Bug Fixes

- Fixed issue 1
- Fixed issue 2

## 📥 Download

Download for your platform:
- **Windows**: AncesTree.exe
- **macOS**: AncesTree.pkg
- **Linux**: AncesTree-x86_64.AppImage

**Important**: Docker Desktop is required. Download from https://www.docker.com/products/docker-desktop

## 📖 Documentation

- New user? Read START_HERE.md
- Full user guide: USER_GUIDE.md
- Technical docs: TECHNICAL_GUIDE.md

## 🙏 Thank You

Thank you to everyone who contributed and provided feedback!

Report issues: https://github.com/yourusername/ancestree/issues
```

---

## Emergency Rollback Plan

If critical issues are discovered after release:

1. **Remove the release** (if severe)
   - Mark as pre-release
   - Add warning to release notes

2. **Hot fix process**
   - Create hotfix branch
   - Fix critical issue
   - Fast-track testing
   - Release patch version (X.Y.Z+1)

3. **Communication**
   - Announce issue immediately
   - Provide workaround if available
   - Give timeline for fix
   - Update all affected users

---

## Notes

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Test thoroughly before release
- Document everything
- Keep users informed
- Celebrate successful releases! 🎉

---

**Last Updated:** YYYY-MM-DD
