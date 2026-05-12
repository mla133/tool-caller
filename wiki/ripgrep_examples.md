# Ripgrep Usage Examples

Ripgrep (`rg`) is a fast search tool that recursively searches directories for a regex pattern.

---

## Basic Searches

### 1. Search for a string in current directory
```bash
rg "TODO"
```
Searches all files recursively for the word `TODO`.

### 2. Case-insensitive search
```bash
rg -i "error"
```
Matches `error`, `Error`, `ERROR`, etc.

---

## File-Specific Searches

### 3. Search only in specific file types
```bash
rg "function" -t js
```
Searches only JavaScript files.

### 4. Search multiple file types
```bash
rg "class" -t py -t js
```
Searches Python and JavaScript files.

### 5. Search in a single file
```bash
rg "main" src/app.cpp
```

---

## Directory & Path Filtering

### 6. Search in a specific directory
```bash
rg "config" ./configs
```

### 7. Exclude directories
```bash
rg "password" --glob '!node_modules/*'
```

---

## Advanced Pattern Matching

### 8. Regex search
```bash
rg "^import .*from"
```
Matches import statements.

### 9. Show line numbers
```bash
rg -n "error"
```

### 10. Count matches
```bash
rg -c "warning"
```

---

## Context & Display Options

### 11. Show context lines before/after match
```bash
rg -C 3 "panic"
```

### 12. Only show matching part
```bash
rg -o "\d+"
```

---

## Searching Across Timeframes (Workarounds)

Ripgrep itself does not filter by file timestamps, but you can combine it with other tools.

### 13. Search files modified in last 24 hours
```bash
find . -type f -mtime -1 -print0 | xargs -0 rg "error"
```

### 14. Search files modified in last 7 days
```bash
find . -type f -mtime -7 -print0 | xargs -0 rg "TODO"
```

---

## Git Integration

### 15. Search only tracked files
```bash
rg "fixme" --no-ignore-vcs
```

### 16. Search only changed files (example)
```bash
git diff --name-only | xargs rg "bug"
```

---

## Performance Tips

- Ripgrep automatically respects `.gitignore`
- Use `--hidden` to include hidden files
- Use `--threads N` to limit CPU usage

---

## Summary

Ripgrep is extremely powerful when combined with:
- File filters (`-t`, `--glob`)
- Regex patterns
- Unix tools like `find` and `xargs`

