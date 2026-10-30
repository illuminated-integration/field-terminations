# Field Terminations

Device-specific pinouts, photos and manuals for Illuminated Integration installs. The QR code on the field flipbook opens this site.

**Live site:** https://illuminated-integration.github.io/field-terminations/

## How it fits together

Everything lives in this GitHub repo. There's no outside service.

```
 Tech's phone                       Reviewer                         GitHub
 ────────────                       ────────                         ──────
 submit.html → opens their   ──▶  email arrives with pinout,   ──▶  upload photos to media/<id>/
 email app, pre-filled;           photos, and a ready-to-paste      paste entry into devices.json
 they attach photos & send        devices.json entry                → Pages republishes the site
```

| File | What it does |
| --- | --- |
| `index.html` | The site: search, category filters, one card per device with photos and manual links. |
| `submit.html` | The submission form. Builds an email and opens the tech's mail app. |
| `data/devices.json` | The database. One entry per device. |
| `media/<device-id>/` | Photos and manual PDFs for each device. |
| `.github/workflows/check-data.yml` | Checks the data and media files on every change. |

---

## One-time setup
1. In the illuminated-integration org, create a **public** repo named `field-terminations`.
2. Upload these files (GitHub Desktop is easiest; it doesn't skip the hidden `.github` folder).
3. **Settings → Pages →** Deploy from a branch → `main` / `(root)` → Save. The site appears at the URL above in a minute or two.
4. In `submit.html`, set the address submissions go to (near the bottom):
   ```js
   const SUBMIT_EMAIL = "development-team@illuminated-integration.com";
   ```
   A shared mailbox or distribution list works best, so submissions don't depend on one person.

## Reviewing a submission
1. An email arrives titled **[Field Terminations] Maker Model - port**. Check the pinout against the attached photos.
2. Save the photos and manual (if attached). Give them simple names like `terminal.jpg`, `wiring.jpg`, `manual.pdf`.
3. In the repo, open `media/`, click **Add file → Upload files**, and type the device id as a new folder in the path box first (e.g. `media/qsc-core110f-mic1/`), then drop the files in. Commit.
4. Open `data/devices.json`, click the pencil, and paste the entry from the bottom of the email after the last entry (with a comma between them). Fill in the file paths:
   ```json
   "images": [{ "file": "media/qsc-core110f-mic1/terminal.jpg", "caption": "Rear panel" }],
   ```
   For an attached manual, add `"file": "media/<id>/manual.pdf"` to its entry under `manuals`.
5. Commit, check **Actions** for a green check, and the site updates in about a minute.

## Device entry template
```json
{
  "id": "qsc-core110f-mic1",
  "title": "QSC Core 110f: Mic/Line In 1",
  "manufacturer": "QSC",
  "model": "Core 110f",
  "category": "Audio",
  "connector": "Euroblock 3-pos",
  "pins": [
    { "pin": "+", "signal": "Hot", "wire": "Red" },
    { "pin": "-", "signal": "Cold", "wire": "Black" },
    { "pin": "G", "signal": "Shield", "wire": "Drain" }
  ],
  "notes": ["Anything that trips people up."],
  "images": [
    { "file": "media/qsc-core110f-mic1/terminal.jpg", "caption": "Rear panel, inputs 1-4" }
  ],
  "manuals": [
    { "title": "Core 110f user manual", "file": "media/qsc-core110f-mic1/manual.pdf",
      "url": "https://manufacturer.example/download", "page": "14" }
  ],
  "source": "Manual p. 14, verified on site",
  "updated": "2026-10-30"
}
```
- `images` and `manuals` are optional. A manual can have a `file` (copy in this repo), a `url` (manufacturer's page), or both. The PDF link opens at `page`.
- Categories: Audio, Lighting, Network, Fiber, Video/RF, Control.
- Wire names such as `Red`, `White/Orange` or `Drain` get a color swatch automatically.
- The `id` is also the deep link: `…/field-terminations/#qsc-core110f-mic1`.

## Limits worth knowing
- **Public repo:** everything here, including photos and manuals, is publicly viewable. Check photos for client information before promoting, and prefer a manufacturer link over hosting a PDF unless you're sure redistribution is allowed.
- **Sizes:** GitHub web uploads accept files up to 25 MB. Phone photos are 3–10 MB each; that's fine, but the repo works best under about 1 GB total.
- **Email length:** the form keeps the email short, but some desktop mail apps (Outlook on Windows) cut off long pre-filled emails. The form shows a Copy button as a fallback.
- **Cost:** free. GitHub Pages and Actions are included with GitHub.

## Previewing locally
```
python3 -m http.server
```
Then open http://localhost:8000. The data won't load if you double-click `index.html` directly.
