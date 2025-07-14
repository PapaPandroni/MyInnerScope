#!/usr/bin/env python3
"""
Asset minification script for My Inner Scope
Minifies CSS and JavaScript files while preserving originals
"""

import os
import shutil
import json
from pathlib import Path
import rcssmin
import re

def minify_css(css_path, backup_dir=None):
    """
    Minify a CSS file
    
    Args:
        css_path: Path to the CSS file
        backup_dir: Directory to store backup (optional)
    
    Returns:
        tuple: (original_size, new_size, saved_bytes)
    """
    css_path = Path(css_path)
    
    # Create backup if backup_dir is specified
    if backup_dir:
        backup_path = Path(backup_dir) / f"{css_path.stem}_original{css_path.suffix}"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(css_path, backup_path)
        print(f"CSS backup created: {backup_path}")
    
    # Get original size
    original_size = css_path.stat().st_size
    
    try:
        # Read original CSS
        with open(css_path, 'r', encoding='utf-8') as f:
            original_css = f.read()
        
        # Minify CSS
        minified_css = rcssmin.cssmin(original_css)
        
        # Write minified CSS
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        # Get new size
        new_size = css_path.stat().st_size
        saved_bytes = original_size - new_size
        
        print(f"Minified {css_path.name}:")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Minified: {new_size:,} bytes")
        print(f"  Saved: {saved_bytes:,} bytes ({saved_bytes/original_size*100:.1f}%)")
        
        return original_size, new_size, saved_bytes
        
    except Exception as e:
        print(f"Error minifying {css_path}: {e}")
        return original_size, original_size, 0

def minify_js_simple(js_path, backup_dir=None):
    """
    Simple JavaScript minification (removes comments and extra whitespace)
    Note: This is basic minification. For production, consider using more advanced tools.
    
    Args:
        js_path: Path to the JS file
        backup_dir: Directory to store backup (optional)
    
    Returns:
        tuple: (original_size, new_size, saved_bytes)
    """
    js_path = Path(js_path)
    
    # Create backup if backup_dir is specified
    if backup_dir:
        backup_path = Path(backup_dir) / f"{js_path.stem}_original{js_path.suffix}"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(js_path, backup_path)
        print(f"JS backup created: {backup_path}")
    
    # Get original size
    original_size = js_path.stat().st_size
    
    try:
        # Read original JavaScript
        with open(js_path, 'r', encoding='utf-8') as f:
            original_js = f.read()
        
        # Simple minification
        # Remove single-line comments (but preserve URLs)
        minified_js = re.sub(r'(?<!:)//.*$', '', original_js, flags=re.MULTILINE)
        
        # Remove multi-line comments (but preserve license comments)
        minified_js = re.sub(r'/\*(?!\*[\s\S]*?@license)[\s\S]*?\*/', '', minified_js)
        
        # Remove extra whitespace
        minified_js = re.sub(r'\n\s*\n', '\n', minified_js)  # Multiple newlines
        minified_js = re.sub(r'^\s+', '', minified_js, flags=re.MULTILINE)  # Leading whitespace
        minified_js = re.sub(r'\s+$', '', minified_js, flags=re.MULTILINE)  # Trailing whitespace
        
        # Remove unnecessary semicolons and spaces around operators
        minified_js = re.sub(r'\s*([{}();,:])\s*', r'\1', minified_js)
        minified_js = re.sub(r'\s*([=<>!+\-*/&|])\s*', r'\1', minified_js)
        
        # Write minified JavaScript
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(minified_js)
        
        # Get new size
        new_size = js_path.stat().st_size
        saved_bytes = original_size - new_size
        
        print(f"Minified {js_path.name}:")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Minified: {new_size:,} bytes")
        print(f"  Saved: {saved_bytes:,} bytes ({saved_bytes/original_size*100:.1f}%)")
        
        return original_size, new_size, saved_bytes
        
    except Exception as e:
        print(f"Error minifying {js_path}: {e}")
        return original_size, original_size, 0

def main():
    """Main minification function"""
    static_dir = Path("app/static")
    backup_dir = "asset_backups"
    
    if not static_dir.exists():
        print(f"Static directory not found: {static_dir}")
        return
    
    # Find CSS and JS files
    css_files = list(static_dir.glob("**/*.css"))
    js_files = list(static_dir.glob("**/*.js"))
    
    total_original = 0
    total_new = 0
    total_saved = 0
    
    print("Starting asset minification...")
    print("=" * 50)
    
    # Minify CSS files
    if css_files:
        print("Minifying CSS files:")
        for css_file in sorted(css_files):
            original, new, saved = minify_css(css_file, backup_dir)
            total_original += original
            total_new += new
            total_saved += saved
            print()
    
    # Minify JavaScript files
    if js_files:
        print("Minifying JavaScript files:")
        for js_file in sorted(js_files):
            # Skip if file is already minified
            if '.min.js' in js_file.name:
                print(f"Skipping already minified: {js_file.name}")
                continue
                
            original, new, saved = minify_js_simple(js_file, backup_dir)
            total_original += original
            total_new += new
            total_saved += saved
            print()
    
    print("=" * 50)
    print("Minification Summary:")
    print(f"Total original size: {total_original:,} bytes ({total_original/1024:.2f} KB)")
    print(f"Total new size: {total_new:,} bytes ({total_new/1024:.2f} KB)")
    print(f"Total saved: {total_saved:,} bytes ({total_saved/1024:.2f} KB)")
    if total_original > 0:
        print(f"Overall reduction: {total_saved/total_original*100:.1f}%")
    
    print(f"\nBackups stored in: {backup_dir}/")
    print("To restore a backup: cp asset_backups/filename_original.ext app/static/path/filename.ext")

if __name__ == "__main__":
    main()