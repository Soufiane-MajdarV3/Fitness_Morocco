# Files to Remove from Repository for Vercel Deployment

## Large Files to Remove (Use Git)

```bash
# Remove SQLite database (will use MySQL in production)
git rm --cached db.sqlite3
echo "db.sqlite3" >> .gitignore

# Remove cache directories from git
git rm -r --cached __pycache__
git rm -r --cached .pytest_cache
git rm -r --cached .mypy_cache
git rm -r --cached .hypothesis

# Remove compiled Python files
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name ".py[cod]" -delete

# Remove unnecessary documentation (duplicates)
git rm TEMPLATES_CONVERSION_SUMMARY.md 2>/dev/null || true
git rm README_TEMPLATES_GUIDE.md 2>/dev/null || true

# Commit cleanup
git add .
git commit -m "Optimize for Vercel: remove large files and cache"
git push -u origin main
```

## Files Removed and Why

| File/Directory | Reason | Size Impact |
|---|---|---|
| `db.sqlite3` | Use MySQL in production | ~350KB |
| `__pycache__/` | Python cache (regenerated at build) | ~1MB+ |
| `*.pyc` | Compiled Python (regenerated) | ~100KB |
| `TEMPLATES_CONVERSION_SUMMARY.md` | Duplicate documentation | ~12KB |
| `README_TEMPLATES_GUIDE.md` | Duplicate documentation | ~16KB |
| `setup_mysql.py` | Development only | ~4KB |
| `setup_database.sh` | Development only | ~4KB |

## Total Size Reduction

- **Before**: ~500MB+ (with git history and cache)
- **After**: ~100-150MB (optimized)
- **Repository size**: ~5-10MB (cleaned)

## Vercel Memory Limit

- **Hobby Plan Limit**: 2048 MB
- **Production Bundle**: ~150-200 MB (after cleanup)
- **Safe Margin**: Plenty of room for dependencies

## What Gets Added Back During Build

Vercel's build process will automatically:
- ✅ Install packages from `requirements.txt`
- ✅ Create `staticfiles/` directory
- ✅ Generate `__pycache__/` if needed
- ✅ Run Django migrations
- ✅ Cache dependencies (first build only)

## After Cleanup - Run This

```bash
# 1. Remove old git history (optional but reduces size further)
git filter-branch --prune-empty --all

# 2. Clean git garbage
git gc --aggressive --prune

# 3. Push cleanup
git push -f origin main

# 4. Deploy to Vercel
```

## Verify Sizes

```bash
# Check current size
du -sh .

# Check git size
du -sh .git

# Check for remaining large files
find . -type f -size +1M

# This should return minimal results
```
