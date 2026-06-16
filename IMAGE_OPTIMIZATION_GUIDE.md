# Image Optimization Guide

## WEBP Conversion Strategy

This guide explains how to optimize the `/photos` directory for better performance.

### Current Status
- Original format: JPEG (assumed)
- Current size: Unknown (photos not tracked in repo)
- Target: WEBP + fallback JPEG

### Step 1: Convert Images to WEBP

#### Using ImageMagick (Recommended)
```bash
# Convert all JPG to WEBP (60% size reduction typical)
for img in photos/*.jpg; do
  convert "$img" -quality 80 "${img%.jpg}.webp"
done

# For PNG files
for img in photos/*.png; do
  convert "$img" -quality 80 "${img%.png}.webp"
done
```

#### Using ffmpeg
```bash
ffmpeg -i photos/g1.jpg -c:v libwebp -quality 80 photos/g1.webp
```

#### Using Node.js (sharp library)
```javascript
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const photosDir = './photos';
fs.readdirSync(photosDir).forEach(file => {
  if (/\.(jpg|jpeg|png)$/i.test(file)) {
    sharp(path.join(photosDir, file))
      .webp({ quality: 80 })
      .toFile(path.join(photosDir, file.replace(/\.\w+$/, '.webp')))
      .then(() => console.log(`Converted: ${file}`));
  }
});
```

### Step 2: Update generate.py for Picture Elements

Replace simple `<img>` tags with responsive picture elements:

```python
def responsive_image(src, alt, width, height):
    base = src.rsplit('.', 1)[0]
    return f"""
    <picture>
      <source srcset="{base}.webp" type="image/webp">
      <source srcset="{src}" type="image/jpeg">
      <img src="{src}" alt="{H.escape(alt)}" width="{width}" height="{height}" 
           decoding="async" loading="lazy" fetchpriority="high">
    </picture>
    """
```

### Step 3: Image Dimensions & Srcset

Add responsive image handling:

```python
def responsive_image_srcset(src, alt, width, height):
    base = src.rsplit('.', 1)[0]
    return f"""
    <picture>
      <source 
        srcset="{base}-small.webp 480w, {base}-medium.webp 900w, {base}.webp 1200w" 
        type="image/webp">
      <source 
        srcset="{base}-small.jpg 480w, {base}-medium.jpg 900w, {src} 1200w" 
        type="image/jpeg">
      <img src="{src}" alt="{H.escape(alt)}" width="{width}" height="{height}" 
           decoding="async" loading="lazy" fetchpriority="high">
    </picture>
    """
```

### Step 4: Vercel Configuration

Update `vercel.json` to cache WEBP images aggressively:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/photos/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        },
        {
          "key": "Accept-Encoding",
          "value": "gzip, deflate, br"
        }
      ]
    }
  ]
}
```

## Expected Results

| Format | Size | Savings |
|--------|------|---------|
| JPEG (original) | 100% | - |
| WEBP (quality 80) | 40% | 60% ↓ |
| WEBP (quality 70) | 30% | 70% ↓ |

## Next Steps

1. Convert all photos to WEBP
2. Keep JPEG originals as fallback
3. Update HTML generation to use picture elements
4. Test on Chrome DevTools (Network tab)
5. Monitor Core Web Vitals (LCP, FID, CLS)

## Tools

- **ImageMagick**: `brew install imagemagick`
- **FFmpeg**: `brew install ffmpeg`
- **Sharp (Node)**: `npm install sharp`
- **Squoosh**: https://squoosh.app/ (GUI alternative)
