#!/bin/bash
# Comprehensive Import Checker
# Verifies all imports in TypeScript files point to actual files

echo "🔍 Checking All Imports and File Locations"
echo "==========================================="
echo ""

cd /home/user/movie-summary/frontend

ERRORS=0
WARNINGS=0

# Check if src directory exists
if [ ! -d "src" ]; then
    echo "❌ ERROR: src directory not found!"
    exit 1
fi

echo "📁 Checking directory structure..."
echo ""

# List all directories
find src -type d | while read dir; do
    perms=$(stat -c "%a" "$dir" 2>/dev/null || stat -f "%A" "$dir" 2>/dev/null)
    if [ "$perms" != "755" ] && [ "$perms" != "775" ]; then
        echo "⚠️  WARNING: Directory $dir has permissions $perms (should be 755)"
        ((WARNINGS++))
    fi
done

echo ""
echo "📄 Checking all TypeScript files exist and are readable..."
echo ""

# Check all .ts and .tsx files
find src -name "*.ts" -o -name "*.tsx" | while read file; do
    if [ ! -r "$file" ]; then
        echo "❌ ERROR: Cannot read $file"
        ((ERRORS++))
    else
        perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
        if [ "$perms" != "644" ] && [ "$perms" != "664" ]; then
            echo "⚠️  WARNING: $file has permissions $perms (should be 644)"
            ((WARNINGS++))
        fi
    fi
done

echo ""
echo "🔗 Checking @/ path alias imports..."
echo ""

# Find all imports using @/ alias
grep -r "from ['\"]@/" src --include="*.ts" --include="*.tsx" | while IFS=: read -r file import_line; do
    # Extract the import path
    import_path=$(echo "$import_line" | sed -n "s/.*from ['\"]@\/\([^'\"]*\)['\"].*/\1/p")

    if [ -n "$import_path" ]; then
        # Convert @/ to src/
        actual_path="src/$import_path"

        # Try with .ts extension
        if [ -f "$actual_path.ts" ]; then
            echo "✅ $file -> @/$import_path (found: $actual_path.ts)"
        # Try with .tsx extension
        elif [ -f "$actual_path.tsx" ]; then
            echo "✅ $file -> @/$import_path (found: $actual_path.tsx)"
        # Try as index file
        elif [ -f "$actual_path/index.ts" ]; then
            echo "✅ $file -> @/$import_path (found: $actual_path/index.ts)"
        elif [ -f "$actual_path/index.tsx" ]; then
            echo "✅ $file -> @/$import_path (found: $actual_path/index.tsx)"
        else
            echo "❌ ERROR: $file imports @/$import_path but file not found!"
            echo "   Looked for:"
            echo "     - $actual_path.ts"
            echo "     - $actual_path.tsx"
            echo "     - $actual_path/index.ts"
            echo "     - $actual_path/index.tsx"
            ((ERRORS++))
        fi
    fi
done

echo ""
echo "📦 Checking relative imports..."
echo ""

# Find all relative imports
grep -r "from ['\"]\.\./" src --include="*.ts" --include="*.tsx" | head -20 | while IFS=: read -r file import_line; do
    echo "  $file: $import_line"
done

echo ""
echo "🔍 Checking specific critical files..."
echo ""

critical_files=(
    "src/lib/utils.ts"
    "src/main.tsx"
    "src/App.tsx"
    "src/stores/index.ts"
    "src/hooks/use-toast.ts"
    "src/components/ui/button.tsx"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        perms=$(ls -l "$file" | awk '{print $1}')
        echo "✅ $file exists ($perms)"
    else
        echo "❌ ERROR: $file NOT FOUND!"
        ((ERRORS++))
    fi
done

echo ""
echo "=========================================="
echo "📊 Summary:"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ Found $ERRORS errors that need to be fixed!"
    exit 1
else
    echo "✅ All import checks passed!"
    exit 0
fi
