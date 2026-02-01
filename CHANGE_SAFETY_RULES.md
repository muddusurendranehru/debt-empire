# CHANGE-SAFETY RULES

Follow these rules **before and after** any edit to the working HTML app. Do not skip steps.

---

## 1. Before any change

- **Duplicate the current HTML** as `*_STABLE.html` and **only edit the copy.**
  - Example: before editing `senior_arbitrage_manager.html`, copy it to `senior_arbitrage_manager_STABLE.html`. Then edit only `senior_arbitrage_manager.html` (or a separate working copy), never the `_STABLE` file.
  - The `_STABLE` file is your rollback. Do not edit it.

---

## 2. One tiny feature per prompt

- Ask AI for **ONE tiny feature per prompt.**
- **Never mix multiple changes at once.** One request = one feature = one round of testing.

---

## 3. After change — run 5 checks

After every change, run these **5 checks**:

1. **Open app** — App opens without errors (file or localhost).
2. **Add loan** — Add a new loan (Tab 1 or Tab 2) and save.
3. **See in Verifier + Manager** — New loan appears in Verifier dropdown and in Manager table.
4. **Print one loan** — Click 🖨️ Print next to a loan; only that loan appears in the print window.
5. **Test new feature** — Confirm the new feature works as intended.

---

## 4. If anything breaks

- If **ANY** old behavior breaks (e.g. loans not showing, print broken, save broken):
  - **Delete the new/edited file.**
  - **Go back to `*_STABLE.html` immediately** (copy it back to the main filename and use that).
  - Do not try to “fix” the broken file until you have a fresh backup again.

---

## Summary

| Step | Action |
|------|--------|
| Before edit | Copy current HTML → `*_STABLE.html`; edit only the copy. |
| Prompt | One tiny feature per prompt; no mixing. |
| After edit | 5 checks: open app, add loan, Verifier + Manager, print one loan, test new feature. |
| If break | Delete edited file; restore from `*_STABLE.html`. |
