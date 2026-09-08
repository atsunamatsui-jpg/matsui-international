# Matsui DTF Tradeshow Banner — Print Specification

## Aspect ratio — read this first

The finished banner is **20 × 8 ft — exactly 2.500000 : 1**.

The main file measures **61 × 25 in, which is deliberately _not_ 2.5:1**. That
is the bleed. The chain is:

```
61 × 25 in  (file, quarter scale)
  × 400%      → 244 × 100 in
  − 2 in bleed on each edge → 240 × 96 in = 20 × 8 ft = 2.500000 : 1
```

**Do not let a printer scale 61 × 25 to fit a 20 × 8 frame** — that stretches
the artwork about 2.5% horizontally and throws away the bleed. Two files are
supplied so this cannot be ambiguous:

| If the printer wants… | Send |
|---|---|
| artwork **with bleed** (most vinyl shops, for the hem) | `...-300dpi.eps` — 61 × 25 in |
| artwork at **exact finished size** | `...-300dpi-TRIM-no-bleed.eps` — 60 × 24 in, exactly 2.5:1 |

The trim file is the composite with the bleed cut off — 18000 × 7200 px, which
is 2.500000 : 1 to six decimal places. `matsui-banner-20x8-trim-export.py`
regenerates it and **asserts** the ratio, so a build that drifted off 2.5:1
fails rather than shipping quietly.

## Finished size

| | inches | feet |
|---|---|---|
| **Trim (finished)** | 240 × 96 | 20 × 8 |
| **With bleed** | 244 × 100 | — |
| **Bleed** | 2 in all sides | — |
| **Safe margin** | 4 in inside trim | — |
| **Content band** | top 66 in | top 5 ft 6 in |
| **Clear zone** | bottom 30 in | bottom 2 ft 6 in |

No printer spec was supplied, so these are standard vinyl-banner values:
2 in bleed clears the hem, and the 4 in safe margin keeps all type off the
hem and grommet line. **If your printer specifies different values, send them
and the files can be rebuilt — the bleed and safe margin are parameters in
`matsui-banner-20x8-build.py`, not baked into the artwork.**

## Clear zone — bottom 2.5 ft

All artwork is held in the **top 66 in**. The **bottom 30 in (2.5 ft) carries
background gradient only** — no logos, machines, product shots or type —
because on a booth that band sits behind tables, below eye level and behind
foot traffic.

This is enforced, not just laid out: the content box is clipped at the 66 in
line, so the artwork layer contains **zero** pixels below it, drop-shadow
tails included. The background gradient still runs the full height and full
bleed, so the banner reads as one piece.

The gradient was re-tuned for this: the blue → violet → pink → orange
progression is compressed into the content band so the luminous part of the
field sits behind the artwork, and the clear strip resolves into deeper
indigo and plum. It holds the same saturation as the rest of the sheet
(0.56) at about 80% of the value, so it stays coloured ink rather than
turning into a dark margin.

The proof (`...-PROOF-guides.png`) marks the line in green.

The split is a constant — `CLEAR_IN` in the build script (30 in). If the booth
setup changes, edit that one value and rebuild; the content band and the
background's colour distribution both follow from it.

## Column spacing

The three columns are separated by a single constant, `COL_GAP` (180 px =
7.2 in), with the group centred. Column widths are 1659 / 1453 / 2288 px
(66.4 / 58.1 / 91.5 in), solved so that **both machines reach the same
height**, and the group spans 230.4 in of the 240 in width — **4.8 in outer
margins**, just outside the 4 in safe line.

The consumables column is the widest because its lockup — the Matsui mark
beside "DTF CONSUMABLES", matched on cap height and baseline — is sized to
span the column rather than float in it.

The machine images are set to 100% of their column, not more: an earlier 104%
let them bleed past the safe line once the columns got this wide.

## Files

Artwork is supplied at **quarter scale, 300 DPI** — a 61 × 25 in sheet.
**Print at 400%.** The files report 300 DPI in their metadata.

| File | Use |
|---|---|
| `matsui-banner-20x8-300dpi.eps` | **Send this to the printer.** Composite, 61 × 25 in with bleed. |
| `...-300dpi-TRIM-no-bleed.eps` | Composite at exact finished size, 60 × 24 in = exactly 2.5:1. Use if the printer wants no bleed. |
| `...-300dpi-BACKGROUND.eps` | Background layer only. |
| `...-300dpi-ARTWORK.eps` | Content layer only (ground baked in — EPS cannot hold alpha). |
| `...-300dpi-artwork.png` | Content layer on **true transparency** — use this one to drop the artwork over a different background. |
| `matsui-banner-20x8-PROOF-guides.png` | Proof only. Shows bleed / trim / safe lines. **Do not print.** |
| `matsui-banner-20x8-build.py` | Build script — regenerates every file above, including the HTML source. |
| `matsui-banner-20x8-trim-export.py` | Cuts the bleed off the composite to make the exact-2.5:1 trim file. |
| `matsui-banner-mm2-machine-cutout.png` | The MM2 machine as the banner uses it — cut from `IMG_1635.JPG`, alpha only, no shadow (the shadow is applied at build time). |

## Resolution — read before ordering

The sheet is 300 DPI **at quarter scale**, which is **75 DPI at the finished
20 × 8 ft size**. That is normal and correct for a banner viewed from several
feet, and the source art is what sets the real ceiling per element:

| Element | Source | At final size |
|---|---|---|
| Consumable product shots | 3–4k cutouts | **141–251 DPI** |
| MM2 machine | 3212 px over 58.1 in | **~55 DPI** |
| MM4 machine | 2596 px over 66.4 in | **~39 DPI** |

Rendering a larger canvas would upscale those photos, not sharpen them. True
300 DPI at full size would be 72,000 × 28,800 px (2.1 gigapixels) and would
still carry the same underlying photo detail.

The MM4 render is now the weakest element on the sheet. **A larger MM4 render
would raise it** — the layout takes a drop-in replacement without changes.

**To genuinely increase sharpness, supply higher-resolution source art:**
original machine renders and original product photography. The layout will
take them without changes.

## Known gaps

- **MM2 lockup carries a generated white keyline.** The supplied MM4 art has
  a white keyline baked in and holds on the dark ground; the supplied MM2 art
  is black with no keyline and was effectively invisible there. A matching
  keyline was generated so the pair reads as one system. **If Matsui has an
  official reversed / knockout MM2 for dark backgrounds, use it instead** —
  drop it in as `mm2_logo.png` and rebuild.
- **A patch of floor stays with the MM2 machine.** The render sits on a glossy
  floor that carries its own reflection, and around the printer's base the
  floor never resolves into a hard edge to cut against — the boundary there is
  a smooth gradient, not a silhouette. The cut is held generous on purpose:
  tightening it further amputates the caster. It reads as a faint pale apron
  under the rear unit. Cleaning it properly needs a hand-drawn mask.
- **"Shishine gloss"** in the G600 copy looks like a typo; left as supplied.

## Regenerating

`matsui-banner-20x8-build.py` rebuilds every output. It takes a layer mode
(`bg`, `fg`, `all`) and an optional `--guides` flag for the proof. Bleed and
safe margin are constants at the top of the file.

Full-size PNG copies of the composite and background layers are **not**
committed -- each is ~95 MB and duplicates its EPS counterpart. Rebuild them
from the script if a printer asks for PNG rather than EPS. The artwork PNG
*is* committed, because it is the only file carrying real transparency.

The **HTML source is not committed either**, for the same reason: it inlines
every asset as base64 and now weighs ~89 MB, and a copy left in the tree goes
stale the moment any source image is replaced. The build script writes it
(`wide_all.html`) on every run.
