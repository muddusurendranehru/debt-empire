# Step-by-Step: Add a New Loan (PowerShell)

## Step 1. Go to the project folder

```powershell
cd "C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire"
```

---

## Step 2. Drag your documents into `new_uploads/`

- Open: **`loans\new_uploads`** (or run: `explorer loans\new_uploads`)
- **Drag** your PDF/DOCX/Excel (e.g. `bjmagnarepay1.pdf`) into that folder
- The verifier will find the file when you type just the **filename**

---

## Step 3. Run the Loan Verifier

```powershell
py loan_verifier.py
```

---

## Step 4. In the menu, choose: Add new loan

- **Enter choice [1-4]:** type **1** (Verify new loan) → Enter

---

## Step 5. Choose loan source

- **Enter choice [1-4]:**  
  - **1** = Parse Bajaj PDF  
  - **2** = Parse L&T PDF  
  - **3** = Parse HDFC DOCX  
  - **4** = Manual entry  

Example for Bajaj: type **1** → Enter

---

## Step 6. Enter the filename (file is in `new_uploads/`)

- **PDF path:** type the **filename only**, e.g.  
  **`bjmagnarepay1.pdf`**  
  (The script looks in `loans\new_uploads\`, project folder, and Documents.)

---

## Step 7. Complete the wizard

- Answer the prompts (Borrower, Account, OS, EMI, etc.)
- At **Approve and save this loan? [Y/N]:** type **Y** → Enter

---

## Step 8. Regenerate dashboard

```powershell
py empire.py
```

---

## Step 9. Open dashboard (print / email)

```powershell
start dashboard.html
```

Then: **Ctrl+P** → Save as PDF → Email (e.g. OTS Settlement Offer).

---

## Quick copy-paste (all steps in one go)

```powershell
cd "C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire"
explorer loans\new_uploads
# ↑ Drag your PDF into the window that opened, then run:
py loan_verifier.py
# → 1 → 1 → type filename (e.g. bjmagnarepay1.pdf) → complete wizard → Y
py empire.py
start dashboard.html
```
