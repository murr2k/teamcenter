# Teamcenter Training Video Analysis

## 📹 Video Transcription & Analysis Framework

This directory contains tools and documentation for transcribing and analyzing Teamcenter training videos to extract valuable insights for Epiroc operations.

## 📁 Directory Structure

```
training/
├── README.md                        # This file
├── videos/
│   ├── transcripts/                 # Transcribed video content
│   │   └── [video-name].md         # Individual transcripts
│   ├── analysis/                    # Analyzed content & insights
│   │   └── [video-name]-analysis.md
│   ├── scripts/                     # Automation scripts
│   │   ├── transcribe.py           # Video transcription tool
│   │   ├── analyze.py              # Content analysis tool
│   │   └── summarize.py            # Summary generator
│   ├── templates/                   # Analysis templates
│   │   ├── transcript-template.md
│   │   └── analysis-template.md
│   └── raw/                        # Raw video metadata
│       └── sources.json            # Video source catalog
└── requirements.txt                 # Python dependencies
```

## 🎯 Purpose

1. **Knowledge Extraction**: Convert video content into searchable documentation
2. **Training Optimization**: Identify key learning points for Epiroc staff
3. **Feature Discovery**: Document undocumented features and workflows
4. **Best Practices**: Extract expert tips and recommended approaches

## 📋 Video Sources

### Sample Videos
- **Consensus Demo**: https://play.goconsensus.com/s4404385e
- Additional sources to be added

## 🔧 Tools & Scripts

### Video Transcription (`scripts/transcribe.py`)
```bash
python training/videos/scripts/transcribe.py --url [video-url] --output transcripts/
```

### Content Analysis (`scripts/analyze.py`)
```bash
python training/videos/scripts/analyze.py --transcript [file] --focus epiroc
```

### Summary Generation (`scripts/summarize.py`)
```bash
python training/videos/scripts/summarize.py --input analysis/ --output summary.md
```

## 📊 Analysis Framework

### Key Areas of Focus

1. **User Interface Navigation**
   - Menu structures
   - Navigation patterns
   - Keyboard shortcuts
   - UI customization

2. **Core Workflows**
   - Item creation
   - BOM management
   - Change processes
   - Release procedures

3. **Integration Points**
   - CAD integration
   - ERP connections
   - Third-party tools
   - API usage

4. **Best Practices**
   - Performance tips
   - Common pitfalls
   - Efficiency techniques
   - Data management

5. **Epiroc-Specific Applications**
   - Mining equipment workflows
   - Compliance procedures
   - Battery-electric vehicle management
   - Safety documentation

## 📝 Transcript Template

Each transcript follows this structure:

```markdown
# [Video Title]

## Metadata
- Source: [URL]
- Duration: [HH:MM:SS]
- Date Accessed: [YYYY-MM-DD]
- Presenter: [Name if available]
- Topic: [Main topic]

## Summary
[Brief overview of video content]

## Transcript
[Time-stamped transcript]

## Key Points
- [Important takeaway 1]
- [Important takeaway 2]

## Commands/Shortcuts Mentioned
- [Command 1]: [Description]
- [Command 2]: [Description]

## Epiroc Relevance
[How this applies to Epiroc operations]
```

## 🎓 Learning Paths

### Beginner Path
1. Teamcenter UI Navigation
2. Basic Item Creation
3. Simple BOM Structure
4. Document Management

### Intermediate Path
1. Change Management
2. Workflow Creation
3. Reporting Tools
4. Integration Basics

### Advanced Path
1. API Development
2. Custom Workflows
3. Performance Optimization
4. System Administration

### Epiroc-Specific Path
1. Mining Equipment Setup
2. Compliance Management
3. Battery-Electric Integration
4. Safety Documentation

## 🚀 Getting Started

1. **Install Dependencies**
```bash
pip install -r training/requirements.txt
```

2. **Process First Video**
```bash
python training/videos/scripts/transcribe.py \
  --url https://play.goconsensus.com/s4404385e \
  --output training/videos/transcripts/consensus-demo.md
```

3. **Analyze Content**
```bash
python training/videos/scripts/analyze.py \
  --transcript training/videos/transcripts/consensus-demo.md \
  --output training/videos/analysis/consensus-demo-analysis.md
```

## 📈 Progress Tracking

### Completed Videos
- [ ] Consensus Demo (in progress)

### Pending Videos
- [ ] Teamcenter 101
- [ ] BOM Management
- [ ] Change Management
- [ ] Workflow Automation
- [ ] Active Workspace Overview

## 🤝 Contributing

To add new video analysis:
1. Add video URL to `raw/sources.json`
2. Run transcription script
3. Review and correct transcript
4. Run analysis script
5. Add insights to relevant documentation

## 📞 Resources

- Siemens Training Portal: [Link]
- Teamcenter YouTube Channel: [Link]
- Epiroc Internal Training: [Contact PLM Team]

## 📄 License

© 2025 Murray Kopit. All Rights Reserved.

Training materials are for internal Epiroc use only.