# 🔄 CI/CD Pipeline - GitHub Actions

**Complete guide to Ancestree's automated build and deployment system**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Workflow Files](#workflow-files)
4. [Triggering Builds](#triggering-builds)
5. [Build Process](#build-process)
6. [Artifacts and Releases](#artifacts-and-releases)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)
10. [Cost and Limits](#cost-and-limits)

---

## 🎯 Overview

Ancestree uses **GitHub Actions** for continuous integration and continuous deployment (CI/CD), automatically building executables for Windows, macOS, and Linux in the cloud.

### What It Does

✅ **Automated Builds**: Creates executables for all platforms on every release
✅ **Parallel Execution**: Builds all platforms simultaneously for speed
✅ **Artifact Storage**: Saves executables for 90 days
✅ **Release Creation**: Automatically creates GitHub Releases with executables
✅ **Quality Assurance**: Consistent build environment every time
✅ **Zero Configuration**: Works out of the box - no setup required

### Benefits

| Traditional Approach | GitHub Actions CI/CD |
|---------------------|----------------------|
| Need 3 different machines | One command from any machine |
| Manual builds (hours) | Automatic builds (15 minutes) |
| Inconsistent environments | Identical environment every time |
| Human error possible | Fully automated |
| Expensive infrastructure | Free for public repos |

---

## 🏗️ Pipeline Architecture

### High-Level Flow

```
Developer Action          GitHub Actions                   Output
─────────────────        ──────────────────               ────────

git tag v1.0.0    ──►    Trigger Workflow
git push origin
                         ┌─────────────────┐
                         │  Build Windows  │ ──►  Ancestree.exe
                         │  (windows-latest)│
                         └─────────────────┘

                         ┌─────────────────┐
                         │   Build macOS   │ ──►  Ancestree.dmg
                         │  (macos-latest) │
                         └─────────────────┘

                         ┌─────────────────┐
                         │   Build Linux   │ ──►  Ancestree-x86_64.AppImage
                         │ (ubuntu-latest) │
                         └─────────────────┘

                         ┌─────────────────┐
                         │ Create Release  │ ──►  GitHub Release
                         │  & Upload All   │       with all files
                         └─────────────────┘
```

### Workflow Jobs

The pipeline consists of **4 parallel jobs**:

1. **build-windows**: Creates Windows executable
2. **build-macos**: Creates macOS application and DMG
3. **build-linux**: Creates Linux AppImage
4. **create-release-notes**: Generates release documentation (runs after builds)

---

## 📄 Workflow Files

### Main Workflow File

**Location**: `.github/workflows/build-executables.yml`

**Size**: ~250 lines, 8.2 KB

**Structure**:
```yaml
name: Build Executables

on:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps: [...]

  build-macos:
    runs-on: macos-latest
    steps: [...]

  build-linux:
    runs-on: ubuntu-latest
    steps: [...]

  create-release-notes:
    runs-on: ubuntu-latest
    needs: [build-windows, build-macos, build-linux]
    steps: [...]
```

### Key Components

**Triggers** (`on:`):
- Push to `main` branch (excludes docs)
- Push tags starting with `v` (e.g., v1.0.0)
- Manual dispatch from GitHub UI

**Runners**:
- `windows-latest`: Windows Server 2022
- `macos-latest`: macOS 13 (Ventura)
- `ubuntu-latest`: Ubuntu 22.04 LTS

**Actions Used**:
- `actions/checkout@v4`: Clone repository
- `actions/setup-python@v5`: Install Python
- `actions/upload-artifact@v4`: Save executables
- `softprops/action-gh-release@v1`: Create releases

---

## 🚀 Triggering Builds

### Method 1: Create a Release Tag (Recommended)

**Creates a permanent GitHub Release with all executables**

```bash
# 1. Ensure code is committed and pushed
git add .
git commit -m "Release v1.0.0"
git push

# 2. Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# 3. Push tag to trigger workflow
git push origin v1.0.0
```

**Result**:
- ✅ All 3 executables built
- ✅ GitHub Release created automatically
- ✅ Files uploaded to release
- ✅ Release notes generated
- ✅ Permanent storage (no expiration)

### Method 2: Push to Main Branch

**Creates artifacts (90-day retention)**

```bash
git add .
git commit -m "Update features"
git push origin main
```

**Result**:
- ✅ All 3 executables built
- ✅ Available as artifacts (90 days)
- ❌ No release created
- ❌ Must download from Actions tab

### Method 3: Manual Trigger

**Run workflow manually from GitHub**

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select **Build Executables** workflow
4. Click **Run workflow** dropdown
5. Select branch
6. Click **Run workflow** button

**Result**:
- ✅ All 3 executables built
- ✅ Available as artifacts (90 days)
- ❌ No release created (unless on tag)

### Trigger Comparison

| Method | Release Created? | Permanent Storage? | Use Case |
|--------|------------------|-------------------|----------|
| **Tag push** | ✅ Yes | ✅ Yes | Production releases |
| **Main push** | ❌ No | ❌ No (90 days) | Testing/development |
| **Manual** | Depends on branch | Depends on branch | Ad-hoc builds |

---

## 🔨 Build Process

### Windows Build Job

**Runner**: `windows-latest` (Windows Server 2022)

**Steps**:
1. **Checkout code** - Clone repository
2. **Setup Python 3.11** - Install Python environment
3. **Install dependencies** - `pip install -r build_requirements.txt`
4. **Build executable** - `pyinstaller --clean --noconfirm ancestree.spec`
5. **Upload artifact** - Save `Ancestree.exe`
6. **Create release asset** (if tag) - Add to GitHub Release

**Output**: `dist/Ancestree.exe` (~15-20 MB)

**Build time**: ~3-5 minutes

### macOS Build Job

**Runner**: `macos-latest` (macOS 13 Ventura)

**Steps**:
1. **Checkout code** - Clone repository
2. **Setup Python 3.11** - Install Python environment
3. **Install dependencies** - `pip install -r build_requirements.txt`
4. **Build application** - `pyinstaller --clean --noconfirm ancestree.spec`
5. **Create DMG** - Package app into disk image
   ```bash
   mkdir -p dmg
   cp -R dist/Ancestree.app dmg/
   ln -s /Applications dmg/Applications
   hdiutil create -volname "Ancestree" -srcfolder dmg Ancestree.dmg
   ```
6. **Upload artifacts** - Save app bundle and DMG
7. **Create release asset** (if tag) - Add DMG to GitHub Release

**Output**:
- `dist/Ancestree.app` (application bundle)
- `Ancestree.dmg` (~15-20 MB)

**Build time**: ~4-6 minutes

### Linux Build Job

**Runner**: `ubuntu-latest` (Ubuntu 22.04 LTS)

**Steps**:
1. **Checkout code** - Clone repository
2. **Setup Python 3.11** - Install Python environment
3. **Install system dependencies** - `apt-get install python3-tk`
4. **Install Python dependencies** - `pip install -r build_requirements.txt`
5. **Build executable** - `pyinstaller --clean --noconfirm ancestree.spec`
6. **Create AppImage** - Package into universal Linux format
   ```bash
   # Download AppImage tools
   wget appimagetool-x86_64.AppImage

   # Create AppDir structure
   mkdir -p AppDir/usr/bin
   cp -r dist/Ancestree AppDir/usr/bin/

   # Create desktop file and AppRun
   # Package into AppImage
   ./appimagetool-x86_64.AppImage AppDir Ancestree-x86_64.AppImage
   ```
7. **Upload artifact** - Save AppImage
8. **Create release asset** (if tag) - Add to GitHub Release

**Output**: `Ancestree-x86_64.AppImage` (~20-25 MB)

**Build time**: ~3-5 minutes

### Release Notes Job

**Runner**: `ubuntu-latest`

**Dependencies**: Runs after all build jobs complete

**Steps**:
1. **Checkout code** - Clone repository
2. **Create release notes** - Generate formatted documentation
3. **Attach to release** - Add notes to GitHub Release

**Output**: Formatted release description with installation instructions

---

## 📦 Artifacts and Releases

### Artifacts (Temporary Storage)

**What are artifacts?**
- Build outputs stored by GitHub Actions
- Available for **90 days** after workflow run
- Downloadable from Actions tab
- Used for testing and temporary storage

**Accessing artifacts**:
1. Go to repository → **Actions** tab
2. Click on a workflow run
3. Scroll to **Artifacts** section
4. Download:
   - `Ancestree-Windows.zip` (contains .exe)
   - `Ancestree-macOS-DMG.zip` (contains .dmg)
   - `Ancestree-Linux.zip` (contains .AppImage)

**Artifact sizes** (zipped):
- Windows: ~10-12 MB
- macOS: ~8-10 MB
- Linux: ~12-15 MB

### Releases (Permanent Storage)

**What are releases?**
- Official versioned distributions
- **Permanent storage** (no expiration)
- Professional release pages
- Automatic release notes
- Direct download links

**Accessing releases**:
1. Go to repository homepage
2. Click **Releases** on right sidebar
3. Click on version (e.g., v1.0.0)
4. Download from **Assets** section:
   - `Ancestree.exe`
   - `Ancestree.dmg`
   - `Ancestree-x86_64.AppImage`
   - Source code (zip)
   - Source code (tar.gz)

**Release content**:
```
v1.0.0
├── Assets
│   ├── Ancestree.exe
│   ├── Ancestree.dmg
│   ├── Ancestree-x86_64.AppImage
│   ├── Source code (zip)
│   └── Source code (tar.gz)
└── Release Notes
    ├── Installation instructions
    ├── Requirements (Docker)
    └── Documentation links
```

---

## ⚙️ Configuration

### Environment Variables

**No configuration required!** The workflow uses sensible defaults.

**Available for customization**:

```yaml
env:
  PYTHON_VERSION: '3.11'
  BUILD_NAME: 'Ancestree'
  RETENTION_DAYS: 90
```

### Secrets

**None required** for basic functionality.

**Optional secrets** (for code signing):

| Secret Name | Purpose | How to Get |
|-------------|---------|------------|
| `WINDOWS_CERT` | Windows code signing | Microsoft Authenticode certificate |
| `WINDOWS_CERT_PASSWORD` | Certificate password | From certificate provider |
| `MACOS_CERT` | macOS code signing | Apple Developer ID certificate |
| `MACOS_CERT_PASSWORD` | Certificate password | From Apple Developer |
| `CODESIGN_IDENTITY` | macOS signing identity | Apple Developer account |

**Adding secrets**:
1. Repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add name and value
4. Click **Add secret**

### Modifying Python Version

Edit `.github/workflows/build-executables.yml`:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # Change here (e.g., '3.12')
```

**Note**: Test locally first - some Python versions may have compatibility issues.

### Changing Build Triggers

Edit the `on:` section:

```yaml
on:
  push:
    branches:
      - main
      - develop      # Add more branches
      - release/*    # Pattern matching
    tags:
      - 'v*'         # v1.0.0, v2.1.3, etc.
      - 'release-*'  # release-1.0.0, etc.
  pull_request:      # Build on PRs
    branches:
      - main
```

### Adding Build Steps

Example: Run tests before building

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run tests
        run: |
          pip install pytest
          pytest tests/

  build-windows:
    needs: test  # Only build if tests pass
    runs-on: windows-latest
    steps: [...]
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering

**Symptoms**: No workflow runs appear after pushing code

**Solutions**:
- ✅ Check Actions are enabled: Settings → Actions → Allow all actions
- ✅ Verify workflow file is in `.github/workflows/`
- ✅ Check YAML syntax: Use GitHub's YAML validator
- ✅ Ensure branch/tag matches triggers

#### 2. Build Fails - Import Error

**Error**: `ModuleNotFoundError: No module named 'xyz'`

**Solution**: Add to `build_requirements.txt`:
```txt
pyinstaller>=6.0.0
setuptools>=68.0.0
wheel>=0.41.0
xyz>=1.0.0  # Add missing module
```

**Or** add to `ancestree.spec` hidden imports:
```python
hiddenimports=[
    'tkinter',
    'tkinter.ttk',
    'xyz',  # Add missing module
],
```

#### 3. Build Fails - File Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'docs/OLD_FILE.md'`

**Solution**:
- Update `ancestree.spec` to reference correct files
- Use relative paths (not absolute)
- Ensure files exist in repository

#### 4. Artifact Not Appearing

**Symptoms**: Build succeeds but no artifact to download

**Solutions**:
- ✅ Wait 1-2 minutes after workflow completes
- ✅ Check workflow logs for upload errors
- ✅ Verify path in `actions/upload-artifact`:
  ```yaml
  - uses: actions/upload-artifact@v4
    with:
      name: Ancestree-Windows
      path: dist/Ancestree.exe  # Check this path
      if-no-files-found: error   # Fails if path wrong
  ```

#### 5. Release Not Created

**Symptoms**: Build succeeds but no release appears

**Solutions**:
- ✅ Ensure you pushed a **tag** (not just code)
  ```bash
  git tag v1.0.0
  git push origin v1.0.0  # Push the tag
  ```
- ✅ Tag must start with `v` (e.g., `v1.0.0`, not `1.0.0`)
- ✅ Check workflow condition: `if: startsWith(github.ref, 'refs/tags/')`

#### 6. Build Times Out

**Error**: `The job running on runner XYZ has exceeded the maximum execution time of 360 minutes.`

**Solutions**:
- ✅ Reduce build complexity
- ✅ Cache dependencies:
  ```yaml
  - uses: actions/cache@v3
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
  ```
- ✅ Split into multiple workflows

#### 7. macOS Build - Code Signing Error

**Error**: `errSecInternalComponent` or signing failed

**Solution**: Either:
- Remove code signing (builds without signature):
  ```yaml
  # Remove or comment out signing step
  # - name: Sign application
  #   run: codesign --force --deep --sign "${{ secrets.CODESIGN_IDENTITY }}" ...
  ```
- Or add proper signing certificate to secrets

#### 8. Windows Build - UPX Error

**Error**: `Cannot find 'upx' in PATH`

**Solution**: Disable UPX compression in `ancestree.spec`:
```python
exe = EXE(
    # ...
    upx=False,  # Change from True to False
    upx_exclude=[],
    # ...
)
```

### Debugging Workflows

**Enable debug logging**:

1. Repository → **Settings** → **Secrets** → **Actions**
2. Add secret: `ACTIONS_STEP_DEBUG` = `true`
3. Add secret: `ACTIONS_RUNNER_DEBUG` = `true`
4. Re-run workflow

**Result**: Extremely verbose logging for troubleshooting

**View logs**:
1. Go to **Actions** tab
2. Click workflow run
3. Click job name (e.g., "Build Windows Executable")
4. Expand steps to see detailed output
5. Download logs: Click ⚙️ icon → Download log archive

---

## 🚀 Advanced Usage

### Caching Dependencies

Speed up builds by caching Python packages:

```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/build_requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Install dependencies
  run: pip install -r build_requirements.txt
```

**Benefit**: Saves 1-2 minutes per build

### Matrix Builds

Build multiple Python versions:

```yaml
jobs:
  build-windows:
    runs-on: windows-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # ... rest of build
```

### Conditional Steps

Run steps only on specific conditions:

```yaml
- name: Sign application (macOS only)
  if: runner.os == 'macOS' && github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')
  run: codesign --deep --force --sign "${{ secrets.CODESIGN_IDENTITY }}" Ancestree.app

- name: Upload to S3 (production only)
  if: github.ref == 'refs/heads/main'
  run: aws s3 cp dist/ s3://my-bucket/ --recursive
```

### Notifications

Send notifications on build completion:

```yaml
- name: Notify Slack
  if: always()  # Run even if build fails
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Version Bumping

Automatically increment version:

```yaml
- name: Bump version
  run: |
    # Extract version from tag
    VERSION=${GITHUB_REF#refs/tags/v}

    # Update version in files
    sed -i "s/version = .*/version = '$VERSION'/" setup.py
    sed -i "s/\"version\": .*/\"version\": \"$VERSION\",/" package.json
```

---

## 💰 Cost and Limits

### GitHub Actions Limits

#### Free Tier (Public Repositories)

| Resource | Limit |
|----------|-------|
| **Build minutes** | Unlimited |
| **Storage** | 500 MB |
| **Artifact retention** | 90 days |
| **Concurrent jobs** | 20 |

#### Free Tier (Private Repositories)

| Resource | Limit |
|----------|-------|
| **Build minutes** | 2,000/month |
| **Storage** | 500 MB |
| **Artifact retention** | 90 days |
| **Concurrent jobs** | 20 |

### Build Minute Multipliers

| OS | Multiplier | Example |
|----|------------|---------|
| **Linux** | 1x | 5 real min = 5 billed min |
| **Windows** | 2x | 5 real min = 10 billed min |
| **macOS** | 10x | 5 real min = 50 billed min |

### This Workflow's Cost

**Per build run** (all 3 platforms):

| Platform | Real Time | Multiplier | Billed Minutes |
|----------|-----------|------------|----------------|
| Linux | 5 min | 1x | 5 min |
| Windows | 5 min | 2x | 10 min |
| macOS | 5 min | 10x | 50 min |
| **Total** | **15 min** | - | **65 min** |

**Monthly usage** (private repos):
- Free tier: 2,000 minutes/month
- This workflow: 65 minutes/run
- **Runs per month**: ~30 releases (well within limits)

**Storage usage**:
- Artifacts: ~35 MB per run
- Retention: 90 days
- Free tier: 500 MB
- **Cleanup**: Artifacts auto-delete after 90 days

### Cost Optimization

**1. Limit triggers**:
```yaml
on:
  push:
    tags: ['v*']  # Only on releases, not every push
```

**2. Use branch protection**:
- Require PR reviews before merging
- Reduces unnecessary builds on main

**3. Cancel redundant builds**:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old builds when new one starts
```

**4. Skip docs changes**:
```yaml
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

---

## 📚 Best Practices

### Version Tagging

Use **semantic versioning**:
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.1.1` - Patch release (bug fixes)
- `v2.0.0-beta.1` - Pre-release

### Release Checklist

Before creating a release:

- [ ] All tests passing locally
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped in code
- [ ] No uncommitted changes
- [ ] Branch up to date with main

**Then**:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial stable release"
git push origin v1.0.0
```

### Workflow Maintenance

**Monthly tasks**:
- [ ] Check for workflow updates
- [ ] Update action versions
- [ ] Review artifact storage usage
- [ ] Clean old releases if needed

**Update actions**:
```yaml
# Old
uses: actions/checkout@v3

# New
uses: actions/checkout@v4  # Update version
```

### Security

**Best practices**:
- ✅ Use specific action versions (not `@latest`)
- ✅ Store secrets in GitHub Secrets (never in code)
- ✅ Enable branch protection on `main`
- ✅ Require PR reviews
- ✅ Use `GITHUB_TOKEN` (auto-provided, no setup needed)
- ❌ Don't commit `.env` files
- ❌ Don't echo secrets in logs

---

## 📖 Additional Resources

### GitHub Documentation

- [GitHub Actions Overview](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

### Ancestree Documentation

- [Build Instructions](BUILD_INSTRUCTIONS.md) - Manual building
- [For Developers](FOR_DEVELOPERS.md) - Development guide
- [GitHub Actions README](../.github/README.md) - Quick start guide

### PyInstaller

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [Spec File Options](https://pyinstaller.org/en/stable/spec-files.html)

---

## 🎓 Learning More

### Experiment Safely

**Test changes** without creating releases:

1. Push to a feature branch
2. Use manual workflow dispatch
3. Check artifacts (not releases)
4. Iterate until working

**Example**:
```bash
git checkout -b test-github-actions
# Make changes to workflow
git push origin test-github-actions

# Manually trigger from GitHub UI
# Check results in Actions tab
```

### Customize for Your Needs

This pipeline is a **starting point**. Consider adding:

- Automated testing
- Code linting
- Security scanning
- Performance benchmarking
- Deployment to app stores
- Update server integration
- Telemetry and analytics

---

## ✨ Summary

### What You Have

✅ **Automated cross-platform builds** - Windows, macOS, Linux
✅ **Professional CI/CD pipeline** - Industry-standard workflow
✅ **Zero configuration** - Works out of the box
✅ **Free for public repos** - Unlimited builds
✅ **Easy to use** - One tag push creates everything
✅ **Well documented** - Complete guides available

### Next Steps

1. **Push workflow to GitHub**: `git push`
2. **Create first release**: `git tag v1.0.0 && git push origin v1.0.0`
3. **Download executables**: Check Releases page
4. **Customize**: Adapt workflow to your needs

---

**The CI/CD pipeline is ready to use!** 🚀

**Created:** November 17, 2024
**Status:** Production Ready
**Maintenance:** Review quarterly, update actions annually
