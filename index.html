# SVS Law Offices — website

Static site. No build step, no server. Deployable to GitHub Pages as-is.

```
index.html                        the website
news.json                         legal news feed (auto-regenerated weekly)
update_news.py                    script that rebuilds news.json
assets/note.css                   styles for the note pages
notes/*.html                      8 full Firm Notes
.github/workflows/update-news.yml weekly scheduled job
```

---

## 1. Publish on GitHub Pages

1. Create a repository (e.g. `svs-website`) and upload every file above,
   keeping the folder structure exactly as it is.
2. Go to **Settings → Pages**.
3. Under *Source*, choose **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. Save. The site goes live at `https://<username>.github.io/svs-website/` in a minute or two.

### Custom domain (svslawoffices.in)

1. In **Settings → Pages → Custom domain**, enter `svslawoffices.in` and save.
2. At your domain registrar, create these DNS records:

   | Type  | Name  | Value                     |
   |-------|-------|---------------------------|
   | A     | @     | 185.199.108.153           |
   | A     | @     | 185.199.109.153           |
   | A     | @     | 185.199.110.153           |
   | A     | @     | 185.199.111.153           |
   | CNAME | www   | `<username>.github.io`    |

3. Wait for DNS to propagate, then tick **Enforce HTTPS** on the Pages settings.

---

## 2. Connect the enquiry form  ← REQUIRED

The form does nothing until you do this. It takes about three minutes.

1. Sign up at **https://formspree.io** (free tier is sufficient).
2. Create a new form. Set the recipient to **contact@svslawoffices.in**.
3. Formspree will email that address to verify it. Click the link in that email.
4. Formspree gives you an endpoint like `https://formspree.io/f/xyzabcde`.
   Copy the last part — the 8-character ID (`xyzabcde`).
5. Open `index.html`, find this line (near the bottom, in the script):

   ```js
   const FORMSPREE_ID = "YOUR_FORM_ID";
   ```

   Replace `YOUR_FORM_ID` with your ID:

   ```js
   const FORMSPREE_ID = "xyzabcde";
   ```

6. Commit and push. Enquiries now arrive at contact@svslawoffices.in.

Until this is done, the form shows a message saying it is not yet connected.
Note that owning the domain does not create the mailbox — you still need email
hosting (Zoho Mail has a free tier; Google Workspace is around Rs 150/user/month).

---

## 3. The weekly Legal News feed

`.github/workflows/update-news.yml` runs **every Monday at 06:00 IST**. It pulls
the RSS feeds of Bar and Bench, LiveLaw and SCC Online Blog, writes `news.json`,
and commits it. The site reads that file and renders the headlines.

**Enable it once:** go to the **Actions** tab and click *I understand my workflows,
go ahead and enable them*. To test immediately, open *Update Legal News* → **Run workflow**.

### What it stores

Only the **headline, a short summary (max 28 words) and a link** to the publisher's
own page. Full articles are never copied. Every item opens on the original site.
This matters: those articles are the publishers' copyright, and reproducing them
on the firm's website would infringe it. Do not increase `SUMMARY_WORDS` in
`update_news.py` without thinking carefully about this.

### If a feed changes

`update_news.py` tries several candidate URLs per publication and uses whichever
responds. If a publisher moves or removes its feed, the script logs a warning and
**leaves the existing `news.json` in place** rather than blanking the section.
The site therefore keeps showing the last good headlines. Check the Actions log
if the feed appears stale, and update the URLs in `SOURCES` if needed.

---

## 4. Editing the Firm Notes

The eight notes in `notes/` are ordinary HTML files. To edit one, change the text
between the `<p>` tags. To add a new note, copy an existing file, change the
content, and add a matching card to the *Firm Notes* grid in `index.html`.

---

## Before going live

- Connect the form (section 2) — otherwise enquiries vanish.
- Set up the `contact@svslawoffices.in` mailbox.
- Have the Bar Council disclaimer wording and the practice-area descriptions
  reviewed against the BCI rules as they currently stand.
- The Firm Notes state legal positions. Read them once as the lawyer whose
  registration is attached to them.
