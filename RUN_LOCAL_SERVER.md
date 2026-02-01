# Run Server & Check HTML Locally

## Option 1: Python HTTP Server (recommended)

### Python 3
```powershell
cd c:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
python -m http.server 8080
```
Then open: **http://localhost:8080/verifier_with_upload_v3.2.html**

### Python 2
```powershell
cd c:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
python -m SimpleHTTPServer 8080
```
Then open: **http://localhost:8080/verifier_with_upload_v3.2.html**

---

## Option 2: Node.js (npx)

```powershell
cd c:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
npx -y serve -p 3000
```
Then open: **http://localhost:3000/verifier_with_upload_v3.2.html**

---

## Option 3: Open file directly (no server)

Double-click `verifier_with_upload_v3.2.html` or:
```powershell
start c:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\verifier_with_upload_v3.2.html
```
Note: `fetch('masters.json')` may fail with file://; use a server for full behavior.

---

## Quick checklist

1. Open PowerShell in project folder (or `cd` to `debt-empire`).
2. Run one of the server commands above.
3. In browser go to the URL shown (e.g. http://localhost:8080/verifier_with_upload_v3.2.html).
4. Test: Tab 1 → drop/select a PDF or image → check extraction; Tab 2 → EXTRACT GOOD → NEW LOAN; Tab 3 → active loans.

To stop server: **Ctrl+C** in the terminal.
