# 🛠️ Step-by-Step: School Lockdown Setup (Windows 11 + Microsoft Family Safety + Google Family Link)

This is a **hands-on tutorial** that walks you through configuring a full school lockdown environment based on the previous guide. Follow these steps for EACH laptop.

---

# ✅ Prerequisites

Before you begin:

- You have a **Microsoft account (parent)**
- You have (or will create) **Microsoft child accounts**
- You have (or will create) **Google accounts for each child**
- You have access to a phone for **Google Family Link app**

---

# 🪟 PART 1 — Microsoft Family Safety (Device Lockdown)

---

## Step 1 — Create Child Accounts

1. On the laptop, open:
   - **Settings → Accounts → Family**
2. Click **Add someone**
3. Select **Create one for a child**
4. Complete account setup

✅ Repeat for each child

---

## Step 2 — Sign Into the Laptop as the Child

1. Log out of your account
2. Log in using the child account you created
3. Let Windows finish setup

✅ This connects the device to Microsoft Family Safety

---

## Step 3 — Open Family Safety Dashboard

On your parent device:

👉 https://family.microsoft.com

1. Log in
2. Verify each child appears
3. Select a child

---

## Step 4 — Configure Screen Time Schedule

1. Select the child → **Screen Time**
2. Turn ON **Use one schedule for all devices**

### Configure WEEKDAYS (Mon–Fri):

- Allowed: **7:00 AM – 8:30 PM**
- Blocked: overnight

### Set total time:

- 6–8 hours

✅ Click **Done**

---

## Step 5 — Configure School Hours Restrictions

There is no direct “school mode”, so do this:

### During school hours (8 AM – 3 PM):

Use **App & Game Limits**:

1. Go to **Apps & Games**
2. Block or limit:
   - Minecraft
   - Roblox
   - Steam
   - Any games

3. Allow unlimited access:
   - Browser
   - Word / Excel
   - Teams / Zoom

💡 Tip: Set games to **0 minutes allowed** on weekdays

---

## Step 6 — Turn On Web Filtering

1. Go to **Content filters → Web and search**
2. Enable:
   - ✅ Filter inappropriate websites
   - ✅ Use only allowed websites (optional but strong lockdown)

### Add allowed sites (example):

- https://classroom.google.com
- https://docs.google.com
- https://khanacademy.org

---

## Step 7 — Configure App Permissions

1. Go to **Spending / App permissions**
2. Enable **Ask to buy / approval required**

✅ Prevents installing games or new apps

---

## Step 8 — Lock Down User Permissions

On each laptop:

1. Go to **Settings → Accounts → Other users**
2. Confirm:
   - Parent = Administrator
   - Kids = Standard User

✅ IMPORTANT: Kids must NOT have admin rights

---

# 🌐 PART 2 — Google Family Link (Content + Browser Control)

---

## Step 1 — Install Family Link App

On your phone:

- Install **Google Family Link**
- Sign in with your Google account

---

## Step 2 — Add Your Child

1. Tap **Add child**
2. Create or connect their Google account
3. Enable supervision

✅ Repeat for each child

---

## Step 3 — Sign Into Chrome on Laptop

On each laptop:

1. Open **Google Chrome**
2. Click profile icon → **Add profile**
3. Sign in using child's Google account
4. Enable sync

---

## Step 4 — Enable Safe Browsing Controls

In Family Link app:

1. Select child
2. Tap **Controls → Content restrictions → Google Chrome**

Enable:

- ✅ Try to block explicit sites
- ✅ Manage sites manually

---

## Step 5 — Configure Allowed / Blocked Sites

In Family Link:

### Allow:
- classroom.google.com
- docs.google.com
- school domains

### Block:
- gaming websites
- streaming sites

---

## Step 6 — YouTube Restrictions

1. Go to **Content restrictions → YouTube**
2. Enable **Restricted Mode**

✅ Reduces inappropriate content

---

# 🔐 PART 3 — Anti-Bypass Hardening (Critical)

---

## Step 1 — Lock Browser Installation

- Kids cannot install software (standard accounts)
- Only allow ONE browser (Edge or Chrome)

---

## Step 2 — Enforce Browser Usage

Option A (simple):
- Uninstall other browsers

Option B (stronger):
- Use Microsoft Family filters (works best with Edge)

---

## Step 3 — Optional DNS Filtering (Advanced)

On your router or device:

- Use **OpenDNS Family Shield**
- Blocks inappropriate content globally

---

# 🧪 PART 4 — Test the Setup

Do this before handing off laptops:

### Test cases:

- Try opening a blocked site ✅ should fail
- Try launching a blocked game ✅ should fail
- Try installing an app ✅ should require approval
- Try logging in outside hours ✅ should fail

---

# ✅ Daily Behavior (Final State)

## 🟢 8:00 AM – 3:00 PM
- Only school tools available
- Games blocked

## 🟡 3:00 PM – 8:30 PM
- Limited entertainment allowed

## 🔴 8:30 PM – 7:00 AM
- Device locked

---

# ✅ Final Checklist

- [ ] Microsoft child accounts created
- [ ] Screen time schedule configured
- [ ] Games blocked during school hours
- [ ] Web filtering enabled
- [ ] Google Family Link configured
- [ ] Chrome signed in and synced
- [ ] No admin access for kids
- [ ] Tested restrictions

---

✅ You now have a **fully enforced school lockdown system** that is realistic, maintainable, and difficult to bypass.
