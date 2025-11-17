# GitHub Actions for AncesTree

This directory contains GitHub Actions workflows that automatically build executables for all platforms.

## Workflows

### `build-executables.yml`

Automatically builds Windows, macOS, and Linux executables.

**Triggers:**
- Push to `main` branch (excludes documentation changes)
- New version tags (e.g., `v1.0.0`)
- Manual trigger via GitHub Actions tab

**What it builds:**
- **Windows**: `AncesTree.exe`
- **macOS**: `AncesTree.dmg` (disk image with app bundle)
- **Linux**: `AncesTree-x86_64.AppImage`

## How to Use

### Option 1: Create a Release (Recommended)

This will build all executables and create a GitHub release:

```bash
# 1. Commit your changes
git add .
git commit -m "Ready for release"
git push

# 2. Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
1. Build executables for all three platforms
2. Create a GitHub Release with the tag name
3. Upload all executables to the release
4. Generate release notes

### Option 2: Manual Build

Go to your GitHub repository:
1. Click the "Actions" tab
2. Select "Build Executables" workflow
3. Click "Run workflow"
4. Choose the branch
5. Click "Run workflow" button

Executables will be available as artifacts (downloadable for 90 days).

### Option 3: Automatic Build on Push

Simply push to the `main` branch:

```bash
git add .
git commit -m "Your changes"
git push
```

Executables will be available as artifacts.

## Downloading Build Artifacts

### From Workflow Runs:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click on a workflow run
4. Scroll to "Artifacts" section
5. Download:
   - `AncesTree-Windows` (Windows .exe)
   - `AncesTree-macOS-DMG` (macOS disk image)
   - `AncesTree-Linux` (Linux AppImage)

### From Releases:

1. Go to your repository on GitHub
2. Click "Releases" on the right sidebar
3. Click on a release version
4. Download files from "Assets" section

## Build Times

Approximate build times:
- **Windows**: 3-5 minutes
- **macOS**: 4-6 minutes
- **Linux**: 3-5 minutes
- **Total**: ~10-15 minutes for all platforms

## Troubleshooting

### Build fails on Windows/Linux/macOS

Check the workflow logs:
1. Go to "Actions" tab
2. Click the failed workflow run
3. Click the failed job (e.g., "Build Windows Executable")
4. Expand the failed step to see error logs

Common issues:
- **Missing dependencies**: Add to `build_requirements.txt`
- **Import errors**: Add to `hiddenimports` in `ancestree.spec`
- **File not found**: Ensure paths are relative and cross-platform

### Icon not showing

Make sure icon files exist in `assets/` directory:
- Windows: `assets/icon.ico`
- macOS: `assets/icon.icns`
- Linux: `assets/icon.png`

If missing, the executables will build without custom icons.

### Artifacts expired

Artifacts are kept for 90 days. To keep executables permanently:
1. Create a release tag (see Option 1 above)
2. Release assets are stored permanently

## Customization

### Change Python version

Edit `.github/workflows/build-executables.yml`:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # Change this
```

### Add more platforms

You can add builds for:
- ARM Linux (Raspberry Pi)
- ARM macOS (M1/M2)
- Windows ARM

Just add another job in the workflow file.

### Change triggers

Edit the `on:` section in `build-executables.yml`:

```yaml
on:
  push:
    branches:
      - main
      - develop  # Add more branches
    tags:
      - 'v*'
      - 'release-*'  # Add more tag patterns
```

## Cost

GitHub Actions is **free** for:
- Public repositories: Unlimited
- Private repositories: 2,000 minutes/month

This workflow uses approximately 30-45 minutes per run (all 3 platforms combined).

## Security

The workflow uses:
- `GITHUB_TOKEN`: Automatically provided by GitHub
- No secrets needed for building executables

If you add code signing:
- Add signing certificates as GitHub Secrets
- Reference them in the workflow: `${{ secrets.CERT_PASSWORD }}`

## Next Steps

1. **Push to GitHub**: Commit and push these workflow files
2. **Enable Actions**: Ensure GitHub Actions is enabled in repository settings
3. **Create first release**: Use `git tag v1.0.0 && git push origin v1.0.0`
4. **Download executables**: Check the Releases page

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
