# 🚀 Teamcenter Quick Start Guide - Epiroc Edition

*Your survival guide for the first week with Teamcenter PLM*

---

## 🎯 Day 1 Essentials - What You MUST Know

### The 15-Minute Power User Setup

1. **Get Your Login Working**
   - URL: [Your Teamcenter URL - ask IT]
   - Username: Your Epiroc email (usually)
   - Password: Your Windows password (usually)
   - If it doesn't work: Call IT immediately, don't waste time troubleshooting

2. **Choose Your Weapon (Interface)**
   - **Active Workspace** (Web) ← Start here! No installation needed
   - **Rich Client** (Desktop) - Only if specifically told to use it

3. **Find These THREE Things First**
   ```
   🏠 Home Dashboard - Your command center
   📁 Your Project Folder - Where your work lives
   🔍 Search Bar - Your best friend (seriously)
   ```

4. **Emergency Contacts** (Fill these in!)
   - PLM Help Desk: ___________
   - Your PLM Buddy: ___________
   - IT Support: ___________

### Your First Hour Checklist

- [ ] Successfully logged in
- [ ] Found the main project folder for your team
- [ ] Performed one search (try searching for "drill" or "loader")
- [ ] Opened one document (anything, just to see it work)
- [ ] Found the "Help" menu (you'll need it)

---

## 🔄 Common Workflows You'll Actually Use

### Workflow 1: "I Need to Find That Drawing"
```
1. Click Search 🔍
2. Type part number or description
3. Filter by "Type: Drawing"
4. Sort by "Modified Date" (newest first)
5. Click to preview, double-click to open
```

### Workflow 2: "Someone Asked Me to Review Something"
```
1. Check "My Tasks" on dashboard
2. Click the task name
3. Review the attached documents
4. Add comments in the comment box
5. Click "Complete Task" with your decision
```

### Workflow 3: "I Need to See What Changed"
```
1. Find the item
2. Look for "Revision" column
3. Right-click → "Compare with Previous"
4. Changes highlighted in the comparison view
```

### Workflow 4: "Creating a New Document"
```
1. Navigate to your project folder
2. Right-click → "New" → "Document"
3. Fill in the form (ask if unsure about fields)
4. Upload your file
5. Click "Finish"
```

---

## 📚 Key Terms Translator

| They Say... | They Mean... | What It Really Means |
|-------------|--------------|----------------------|
| **Item** | A thing in the system | Any part, document, or assembly |
| **Revision** | Version of that thing | A, B, C... when something changes |
| **BOM** | Bill of Materials | The recipe for building equipment |
| **Dataset** | Attached files | The actual CAD file, PDF, etc. |
| **Workflow** | Approval process | How stuff gets approved |
| **ECN** | Engineering Change Notice | "We're officially changing this" |
| **Check Out/In** | Lock/unlock for editing | Like Google Docs but more serious |
| **Released** | Approved and frozen | Don't touch it without an ECN |
| **WIP** | Work in Progress | Still being worked on |
| **Assembly** | Collection of parts | Like a Lego set instruction |

---

## 💡 Tips and Tricks for New Users

### Search Like a Pro
- Use `*` as wildcard: `DRILL*` finds DRILL001, DRILL-FRAME, etc.
- Use quotes for exact phrases: `"hydraulic pump"`
- Right-click search results → "Add to Clipboard" to collect multiple items

### Navigation Shortcuts
- **Home button** always takes you back to safety
- **Breadcrumbs** at top show where you are
- **Recent Items** in menu = your history
- **Bookmarks** = save important locations

### Don't Panic When...
- 🔴 **"Access Denied"** - You probably need permission, ask your lead
- 🔴 **"Checked Out by [Someone]"** - They're editing it, message them
- 🔴 **"Workflow Failed"** - Check comments for what went wrong
- 🔴 **Loading Forever** - Refresh browser, if still stuck, restart

### Power User Secrets
1. **Ctrl+F** works in most views for quick find
2. **Export to Excel** is your friend for reports
3. **Subscribe** to items to get email notifications of changes
4. **Saved Searches** are worth setting up by Week 2

---

## ⚠️ Common Pitfalls to Avoid

### The "Oh No" Moments to Prevent

1. **Don't Release Something by Accident**
   - Released = Locked forever (without ECN)
   - Double-check before clicking "Release"

2. **Don't Edit Without Checking Out**
   - Always check out first
   - Others can't edit while you have it

3. **Don't Ignore Workflow Tasks**
   - They have deadlines
   - People are waiting on you
   - Check "My Tasks" daily

4. **Don't Create Duplicates**
   - Search first, create second
   - Reuse existing parts when possible

5. **Don't Forget Where You Saved Things**
   - Use consistent folder structure
   - Follow naming conventions
   - Ask about standards

---

## 📅 Your Week 1 Learning Path

### Monday - Survival Mode
- ✅ Login and basic navigation
- ✅ Find your project area
- ✅ Search for something successfully

### Tuesday - Explorer Mode
- 📋 Navigate BOMs (find a loader or drill rig)
- 📋 Open different document types
- 📋 Understand statuses (WIP, Released, etc.)

### Wednesday - Contributor Mode
- 📝 Check out and check in a document
- 📝 Add a comment to something
- 📝 Complete a simple workflow task (if assigned)

### Thursday - Builder Mode
- 🔨 Create a new document
- 🔨 Upload a file to Teamcenter
- 🔨 Understand basic Properties

### Friday - Connected Mode
- 🔗 Understand relationships between items
- 🔗 Find where a part is used
- 🔗 Generate a simple report

---

## 🆘 When to Ask for Help

### Green Flags - Try It Yourself First
- Can't find something (use search)
- Forgot how to do something (check help)
- Want to explore a feature

### Yellow Flags - Ask a Colleague
- Unsure about naming convention
- Don't know which folder to use
- Need workflow guidance

### Red Flags - Escalate Immediately
- Can't login at all
- Accidentally deleted something
- System errors or crashes
- About to release something important

---

## 📊 Epiroc-Specific Quick Reference

### Common Equipment Types You'll See
- **Scooptram** - Underground loaders
- **Boomer** - Drilling rigs
- **Simba** - Production drilling
- **Boltec** - Rock reinforcement

### Typical Folder Structure
```
/Epiroc
  /Projects
    /[Your Project]
      /Design
      /Documentation  
      /Manufacturing
      /Service
  /Libraries
    /Standard Parts
    /Hydraulics
    /Electronics
```

### Status Workflow at Epiroc
```
Draft → In Review → Approved → Released
         ↓ (if issues)
      Rejected → Draft
```

---

## 🎓 Advanced Topics for Week 2+

Once you're comfortable with basics:
- Learn about Change Management (ECN process)
- Explore CAD integration (if relevant to your role)
- Set up email notifications
- Create saved searches
- Learn report generation
- Understand configuration management

---

## 📝 Notes Section

*Use this space to write down important things specific to your role:*

My Project Folder: _______________________

My Main Part Numbers: ___________________

Important Workflows: ____________________

Key Contacts: __________________________

---

## 💪 Final Encouragement

**Remember:**
- Everyone was new once (even that expert who seems to know everything)
- It gets easier after Week 2
- The search function is incredibly powerful once you learn it
- When in doubt, ask - people prefer questions over mistakes
- Teamcenter is actually logical once you understand its thinking

**You've got this! Welcome to the team!** 🎉

---

*Last tip: Bookmark this guide and the Teamcenter URL in your browser. You'll thank yourself later.*