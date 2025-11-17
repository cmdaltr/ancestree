# 👥 AncesTree - User Guide

**A complete guide for non-technical users**

---

## 🚀 Getting Started

### Step 1: Install AncesTree

**Super Easy - One Command!**

Choose your operating system:

**Windows:**
1. Right-click `scripts\install_windows.bat`
2. Select "Run as administrator"
3. Wait for installation to complete (5-10 minutes)
4. Restart your computer when prompted

**Mac:**
1. Double-click `scripts/install_macos.sh` (or run in Terminal)
2. Wait for installation to complete (5-10 minutes)
3. Docker Desktop will open automatically

**Linux:**
1. Run `./scripts/install_linux.sh` in Terminal
2. Wait for installation to complete
3. Log out and log back in

### Step 2: Start AncesTree

**Windows:**
- Double-click `scripts\Start AncesTree.bat`

**Mac:**
- Double-click `scripts/Start AncesTree.command`

**Linux:**
- Run `./scripts/start_ancestree.sh`

### Step 3: Use AncesTree

Your browser will open automatically to http://localhost:3000

---

## 👤 Creating Your Account

The first time you open AncesTree:

1. Click **"Register"**
2. Fill in:
   - **Email**: Your email address
   - **Username**: Choose a username
   - **Password**: Choose a password
   - **Confirm Password**: Type password again
3. Click **"Register"**
4. Click **"Login"** and enter your username and password

**Your family tree is private** - only you can see it.

---

## 👨‍👩‍👧‍👦 Adding Family Members

### Add Your First Person

1. Click **"+ Add Member"** button at top
2. Fill in what you know:
   - **First Name**: Required
   - **Last Name**: Required
   - **Gender**: Male, Female, or Unknown
   - **Birth Date**: Format: YYYY-MM-DD (like 1950-05-15)
   - **Birth Place**: City, State/Country
   - **Death Date**: If applicable
   - **Death Place**: If applicable
   - **Notes**: Any other information
3. Click **"Add Member"**

### Add More Family Members

- **Parents**: Click a person, then add a new member as their parent
- **Children**: Click a person, then add a new member as their child
- **Spouse**: Click a person, add their spouse, connect them

**Tip**: Start with yourself or your parents, then expand!

---

## 🌲 Using the Family Tree

### Navigation

- **Zoom In/Out**: Mouse wheel (scroll up/down)
- **Move Around**: Click and drag anywhere
- **Select Person**: Click on any person's box

### Colors

- 💙 **Blue** = Male
- 💗 **Pink** = Female
- ⚫ **Gray** = Unknown gender
- 💚 **Green** = Currently selected

### Lines

Lines show relationships (parents to children)

---

## ✏️ Editing People

1. **Click on a person** in the tree
2. Side panel opens with their details
3. Click the **pencil icon (✏️)** to edit
4. Change any information
5. Click **"Save"**

---

## 📸 Adding Photos

1. **Click on a person**
2. In side panel, click **"Upload Document"**
3. Choose a photo from your computer
4. Photo appears in their profile
5. Click photos to view larger

**Accepted formats**: JPG, PNG, PDF

---

## 🔍 Searching Records (Optional)

1. Click **"🔍 Search"** button
2. Enter person's information
3. Choose websites to search
4. Click **"Search"**

**Note**: Requires accounts with genealogy websites (Ancestry.com, FamilySearch.org, etc.)

---

## 💾 Your Data

- **Saved automatically** - No need to save manually
- **Stored on your computer** - Not in the cloud
- **Private** - Only you can access it
- **Backup**: Copy the `ancestree` folder to USB/cloud storage

---

## ⚠️ Troubleshooting

### Won't Start

- Make sure Docker Desktop is running (whale icon in tray/menu bar)
- Try clicking "Stop" then "Start" again
- Restart your computer

### Can't Login

- Use your **username** (not email)
- Passwords are case-sensitive
- If forgot password, create new account

### Page Won't Open

- Wait 1-2 minutes after starting
- Click "🌐 Open in Browser" button
- Or manually go to: http://localhost:3000

### Error Messages

- Take a screenshot
- Click "Stop" and "Start" again
- Ask someone technical for help

---

## 🛑 Stopping AncesTree

When you're done:

1. Everything saves automatically
2. Click **"Stop"** button (if using launcher)
3. Or run `./scripts/stop_ancestree.sh`
4. Close your browser
5. You can close Docker Desktop too

Next time: Just start it again - all your data is saved!

---

## 💡 Tips for Success

- **Start small**: Add people you know well first
- **Add dates**: Even just a year helps
- **Use photos**: Makes the tree more interesting
- **Double-check**: Verify information before adding
- **Ask family**: Older relatives remember details
- **Take your time**: Building a tree is a journey!

---

## 🆘 Getting Help

1. Check troubleshooting section above
2. Make sure Docker Desktop is running
3. Try restarting everything
4. Ask a technically-minded family member
5. Show them `docs/FOR_DEVELOPERS.md`

---

**Enjoy building your family tree!** 🌳
