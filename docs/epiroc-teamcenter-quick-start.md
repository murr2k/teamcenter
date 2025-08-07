# Teamcenter Quick Start Guide for Epiroc
*Your survival guide for the first week and beyond*

---

## 🚀 Day 1 Essentials: Hit the Ground Running

### Your Digital Command Center
Think of Teamcenter as the "Google Drive of engineering" – but way more powerful and slightly more complicated. It's where all of Epiroc's product data lives, breathes, and gets things done.

**First Things First:**
- **Active Workspace (AWC)** = Your new best friend (web-based, works everywhere)
- **Rich Client (RAC)** = The old-school desktop app (still needed for some admin tasks)
- **Your Login** = Your golden ticket to engineering data paradise

### The 15-Minute Power User Setup

1. **Bookmark These URLs**
   - Production Teamcenter: `[Your IT team will provide this]`
   - Training environment: `[Usually ends with -train or -dev]`

2. **Set Your Preferences**
   - Go to User Settings → Display preferences
   - Enable "Show line numbers" (trust us on this one)
   - Set your default folder view to "Details"

3. **Learn the Magic Search**
   - **Ctrl+Shift+F** = Global search (works from anywhere)
   - Use wildcards: `*pump*` finds anything with "pump" in it
   - Search by part number, description, or even drawing number

### Your First Day Checklist
- [ ] Can you log in to Active Workspace?
- [ ] Can you navigate to your team's folder?
- [ ] Can you search for and find a part you know exists?
- [ ] Have you bookmarked your most-used folders?
- [ ] Can you view a 3D model? (If this fails, ask IT about viewer plugins)

---

## 🔄 Common Workflows: The Daily Grind Made Easy

### The "I Need to Find Something" Workflow
*AKA: Where did they hide my part?*

1. **Quick Search**: Type in the search box (top of screen)
2. **Advanced Search**: Click the filter icon for detailed criteria
3. **Browse by Structure**: Navigate folders like Windows Explorer
4. **Ask a Colleague**: Sometimes the fastest way (seriously)

**Pro Tip**: If you can't find it in 2 minutes, it's either named something weird or living in someone's personal folder.

### The "I Need to Create Something" Workflow
*AKA: Making new stuff without breaking everything*

1. **Right-click** in your destination folder
2. **Select "Create"** → Choose your object type
3. **Fill in the required fields** (red asterisks = mandatory)
4. **Save** and celebrate your first Teamcenter creation!

**Golden Rule**: Always create in the right folder the first time. Moving things later is like rearranging furniture with glue on it.

### The "I Need to Release Something" Workflow
*AKA: Making it official*

1. **Check-in** all your files (no loose ends)
2. **Create Change Request** if required by your process
3. **Submit for Review** (usually via workflow)
4. **Follow up** (politely nudge reviewers if needed)
5. **Release** once approved

**Reality Check**: This process can take anywhere from 1 day to 1 month depending on complexity and review cycles.

### The "Something Broke and It's Probably My Fault" Workflow
*AKA: Damage control*

1. **Don't panic** (seriously, deep breaths)
2. **Check if you can undo** (Recent changes in your session)
3. **Contact your Teamcenter admin** (they've seen worse)
4. **Document what happened** (helps prevent future issues)
5. **Learn from it** (every expert has broken something spectacular)

---

## 📚 Key Terminology: Speaking Teamcenter

### The Essential Vocabulary

| Term | What It Really Means | Why You Care |
|------|---------------------|--------------|
| **Item** | The "thing" you're working on | Everything starts here |
| **Item Revision** | A version of your thing | Like "Part_v1", "Part_v2" |
| **BOM** | Bill of Materials | Recipe for building your product |
| **EBOM** | Engineering BOM | What engineering designed |
| **MBOM** | Manufacturing BOM | What manufacturing actually builds |
| **Dataset** | A file attached to an item | Your CAD files, docs, etc. |
| **Workspace** | Your personal work area | Like your desk, but digital |
| **Check-out** | "I'm working on this" | Prevents conflicts |
| **Check-in** | "I'm done with this" | Makes changes available |
| **Release** | "This is official" | No more changes allowed |
| **ACL** | Access Control List | Who can see/do what |

### The Acronym Soup

**Must-Know Acronyms:**
- **PLM** = Product Lifecycle Management
- **AWC** = Active Workspace (the web interface)
- **RAC** = Rich Application Client (desktop app)
- **SOA** = Service-Oriented Architecture (how things talk to each other)
- **ITK** = Integration Toolkit (for customizations)
- **BMIDE** = Business Modeler IDE (for data model changes)

**Nice-to-Know Acronyms:**
- **PSE** = Product Structure Editor
- **MEI** = Multi-CAD Easy Integration
- **TCM** = Teamcenter Manufacturing
- **ECR/ECN** = Engineering Change Request/Notice

---

## 💡 Tips and Tricks: Insider Secrets

### Keyboard Shortcuts That'll Make You Look Like a Pro

| Shortcut | Action | Why It's Awesome |
|----------|--------|------------------|
| **Ctrl+Shift+F** | Global search | Find anything, anywhere |
| **Ctrl+N** | New item | Skip the right-click menu |
| **F5** | Refresh | When things look weird |
| **Ctrl+S** | Save | Muscle memory from everywhere else |
| **Ctrl+Z** | Undo (sometimes) | Your safety net |

### Hidden Gems

**The Right-Click is Your Friend**
- Right-click on EVERYTHING to see available actions
- Context menus change based on what you're clicking
- When in doubt, right-click it out

**Search Like a Detective**
- Use quotes for exact phrases: `"hydraulic pump"`
- Use wildcards generously: `*2023*` finds anything from 2023
- Combine criteria: part number AND description
- Save frequent searches as "Saved Searches"

**Workflow Wisdom**
- Always read the task description (it usually has important info)
- You can add comments to workflow tasks (reviewers love context)
- Check your "Inbox" regularly for assigned tasks
- You can delegate tasks if you're going on vacation

**File Management Magic**
- Name files consistently (your future self will thank you)
- Use the "Add Files" dialog instead of drag-and-drop (more reliable)
- Check file sizes before uploading (large files = long waits)
- Keep local copies of important files (just in case)

### The Teamcenter Zen Garden

**Folder Organization Philosophy:**
- Create a logical hierarchy (not too deep, not too flat)
- Use consistent naming conventions
- One project = One main folder (with subfolders for phases)
- Archive old projects to keep active areas clean

**Version Control Wisdom:**
- Check in frequently (don't hoard changes)
- Use meaningful check-in comments
- Create new revisions for significant changes
- Keep the revision history clean and logical

---

## ⚠️ Common Pitfalls: Learn from Others' Pain

### The "I Wish Someone Had Told Me" List

**Rookie Mistake #1: The Forgotten Check-in**
- **What happens**: You work all day, forget to check in, and lose changes
- **Prevention**: Set a reminder to check in every few hours
- **Recovery**: Contact admin immediately if you lose work

**Rookie Mistake #2: The Wrong Folder Fiasco**
- **What happens**: Create everything in your personal folder, can't share with team
- **Prevention**: Always navigate to the project folder first
- **Recovery**: Move items (painful) or recreate them (also painful)

**Rookie Mistake #3: The Overwrite Oops**
- **What happens**: Check out someone else's file and overwrite their changes
- **Prevention**: Always check who has files checked out before working
- **Recovery**: Restore from backup (if you're lucky) or recreate changes

**Rookie Mistake #4: The Permission Problem**
- **What happens**: Can't access something you need for your job
- **Prevention**: Request appropriate role assignments during onboarding
- **Recovery**: Submit access request (and wait... and wait...)

**Rookie Mistake #5: The Naming Nightmare**
- **What happens**: Use spaces, special characters, or inconsistent naming
- **Prevention**: Follow your company's naming conventions religiously
- **Recovery**: Rename (if possible) or live with the shame forever

### Red Flags That Mean "Stop and Ask for Help"

- Any error message mentioning "database" or "server"
- Can't check in/out files for more than 30 minutes
- Performance suddenly becomes terrible
- Missing data that should definitely be there
- Any operation that takes more than 10 minutes

### The "When to Escalate" Guide

**Level 1 (Ask a Colleague)**:
- Can't find something
- Don't understand a workflow step
- Need to learn a new feature

**Level 2 (Contact Power User/Admin)**:
- Performance issues
- Permission problems
- Workflow stuck or broken
- Data seems corrupted

**Level 3 (Call IT/Siemens Support)**:
- System completely down
- Data loss
- Security issues
- Integration problems

---

## 🎯 Your First Week Action Plan

### Day 1: Exploration
- Log in successfully
- Navigate the interface
- Find your team's work areas
- Attempt one simple search

### Day 2-3: Basic Operations
- Create your first item
- Check out and check in a file
- Add a document to an existing item
- Practice searching with different criteria

### Day 4-5: Collaboration
- Submit something for review
- Complete a workflow task assigned to you
- Share a folder with a colleague
- Ask questions without fear

### By Week's End, You Should:
- Feel comfortable navigating Active Workspace
- Know how to find and check out files
- Understand your team's folder structure
- Have created at least one item successfully
- Know who to ask when things go wrong

---

## 🆘 Emergency Contacts & Resources

### Your Lifelines
- **Teamcenter Admin**: `[Name and contact info]`
- **IT Help Desk**: `[Contact info]`
- **Team Lead/Mentor**: `[Your designated guide]`
- **Power Users on Team**: `[Names of go-to people]`

### Self-Help Resources
- **Siemens Documentation**: Usually comprehensive but sometimes dense
- **Internal Wiki**: `[Your company's knowledge base]`
- **Training Environment**: Perfect for practicing without fear
- **User Community**: Other Teamcenter users who share the pain

---

## 🏆 Remember: Everyone Was New Once

Every Teamcenter expert started exactly where you are now. The learning curve is real, but so is the payoff. Within a month, you'll be navigating like a pro. Within three months, colleagues will start asking YOU for help.

**The Teamcenter Motto**: *"It's not just software, it's your digital workspace. Make it work for you."*

Welcome to the team, and happy engineering! 🛠️

---

*Last updated: [Date] | Questions or suggestions? Contact [Your Admin]*