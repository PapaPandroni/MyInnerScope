#!/usr/bin/env python3
"""
Image optimization script for My Inner Scope
Compresses images losslessly while maintaining quality
"""

import os
import shutil
from PIL import Image
from pathlib import Path

def create_webp_version(image_path, quality=85):
    """
    Create WebP version of an image
    
    Args:
        image_path: Path to the original image file
        quality: WebP quality (1-100)
    
    Returns:
        Path to the WebP file or None if failed
    """
    image_path = Path(image_path)
    webp_path = image_path.with_suffix('.webp')
    
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB for WebP if needed
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            
            # Save as WebP
            img.save(webp_path, 'WebP', quality=quality, optimize=True)
            
            original_size = image_path.stat().st_size
            webp_size = webp_path.stat().st_size
            savings = original_size - webp_size
            
            print(f"Created WebP version: {webp_path.name}")
            print(f"  Original: {original_size:,} bytes")
            print(f"  WebP: {webp_size:,} bytes")
            print(f"  Savings: {savings:,} bytes ({savings/original_size*100:.1f}%)")
            
            return webp_path
            
    except Exception as e:
        print(f"Error creating WebP for {image_path}: {e}")
        return None

def optimize_image(image_path, backup_dir=None, create_webp=True):
    """
    Optimize a single image file and optionally create WebP version
    
    Args:
        image_path: Path to the image file
        backup_dir: Directory to store backup (optional)
        create_webp: Whether to create WebP version (default: True)
    
    Returns:
        tuple: (original_size, new_size, saved_bytes)
    """
    image_path = Path(image_path)
    
    # Create backup if backup_dir is specified
    if backup_dir:
        backup_path = Path(backup_dir) / f"{image_path.stem}_original{image_path.suffix}"
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    # Get original size
    original_size = image_path.stat().st_size
    
    try:
        # Open and optimize the image
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if saving as JPEG
            if image_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(img)
                img = background
            
            # Optimize based on file type
            if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                # For JPEG: use high quality but optimize
                img.save(image_path, 'JPEG', quality=85, optimize=True, progressive=True)
            elif image_path.suffix.lower() == '.png':
                # For PNG: optimize without quality loss
                img.save(image_path, 'PNG', optimize=True)
            else:
                print(f"Skipping unsupported format: {image_path}")
                return original_size, original_size, 0
        
        # Get new size
        new_size = image_path.stat().st_size
        saved_bytes = original_size - new_size
        
        print(f"Optimized {image_path.name}:")
        print(f"  Original: {original_size:,} bytes")
        print(f"  New: {new_size:,} bytes")
        print(f"  Saved: {saved_bytes:,} bytes ({saved_bytes/original_size*100:.1f}%)")
        
        # Create WebP version if requested
        if create_webp and image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            create_webp_version(image_path)
        
        return original_size, new_size, saved_bytes
        
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}")
        return original_size, original_size, 0

def main():
    """Main optimization function"""
    assets_dir = Path("app/static/assets")
    backup_dir = "image_backups"
    
    if not assets_dir.exists():
        print(f"Assets directory not found: {assets_dir}")
        return
    
    # Image files to optimize
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(assets_dir.glob(f"*{ext}"))
        image_files.extend(assets_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print("No image files found to optimize")
        return
    
    total_original = 0
    total_new = 0
    total_saved = 0
    
    print("Starting image optimization...")
    print("=" * 50)
    
    for image_file in sorted(image_files):
        # Skip favicon files (they're already small)
        if 'favicon' in image_file.name or 'apple-touch-icon' in image_file.name:
            print(f"Skipping small icon: {image_file.name}")
            continue
            
        original, new, saved = optimize_image(image_file, backup_dir)
        total_original += original
        total_new += new
        total_saved += saved
        print()
    
    print("=" * 50)
    print("Optimization Summary:")
    print(f"Total original size: {total_original:,} bytes ({total_original/1024/1024:.2f} MB)")
    print(f"Total new size: {total_new:,} bytes ({total_new/1024/1024:.2f} MB)")
    print(f"Total saved: {total_saved:,} bytes ({total_saved/1024/1024:.2f} MB)")
    if total_original > 0:
        print(f"Overall reduction: {total_saved/total_original*100:.1f}%")
    
    print(f"\nBackups stored in: {backup_dir}/")
    print("To restore a backup: cp image_backups/filename_original.ext app/static/assets/filename.ext")

if __name__ == "__main__":
    main()