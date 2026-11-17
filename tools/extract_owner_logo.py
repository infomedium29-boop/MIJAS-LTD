"""Extract the exact user-supplied logo from the composite image (crop and background-removal only)."""
from pathlib import Path
from PIL import Image
import numpy as np
root = Path(__file__).resolve().parents[1]
source = root / 'tools/vlasnikov-logo-originalna-slika.png'
out = root / 'assets/images'
im = Image.open(source).convert('RGB')
# the owner's complete logo occupies the top white area, above the horizontal delimiter
logo = im.crop((40, 68, 1090, 556))
logo.save(out / 'mijas-logo-izvorni.png', optimize=True)
# optional transparent cutout, created by backing out a white matte without repainting any graphics.
arr=np.asarray(logo,dtype=np.float32)
alpha=np.max(255.0-arr,axis=2)/255.0
# knock out only near-white matte; formula preserves original chroma after removal of white background.
alpha=np.clip(alpha*1.10,0,1)
# protect against division by zero
recover=np.clip(255.0+(arr-255.0)/np.maximum(alpha[:,:,None],.001),0,255)
rgba=np.dstack((recover,np.round(alpha*255))).astype('uint8')
Image.fromarray(rgba,'RGBA').save(out / 'mijas-logo-transparent.png', optimize=True)
# preserve a larger original wordmark for compact header, without the service strapline
mark=logo.crop((0,0,1050,315))
mark.save(out/'mijas-logo-natpis-original.png',optimize=True)
print('Extracted owner-supplied logo to', out)
