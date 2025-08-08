#!/usr/bin/env python3
"""
Video Transcription Tool for Teamcenter Training Videos
Extracts and processes video content for analysis
"""

import json
import argparse
import requests
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoTranscriber:
    """Handles video transcription and content extraction"""
    
    def __init__(self, output_dir: str = "transcripts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_video_metadata(self, url: str) -> Dict:
        """Fetch video metadata from URL"""
        try:
            # For Consensus demos, extract ID from URL
            if 'goconsensus.com' in url:
                video_id = url.split('/')[-1]
                return {
                    'id': video_id,
                    'platform': 'consensus',
                    'url': url,
                    'fetched_at': datetime.now().isoformat()
                }
            else:
                return {
                    'url': url,
                    'platform': 'unknown',
                    'fetched_at': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            return {}
    
    def extract_transcript(self, url: str) -> str:
        """Extract transcript from video URL"""
        # Note: In production, this would integrate with actual transcription services
        # like YouTube API, Whisper AI, or video platform APIs
        
        transcript = f"""
# Video Transcript

## Metadata
- URL: {url}
- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Status: Manual transcription required

## Content
[Manual transcription needed - use one of these methods:]

### Option 1: YouTube Videos
1. Enable captions/subtitles in the video
2. Click the three dots menu → Show transcript
3. Copy and paste the transcript here

### Option 2: Audio Extraction
1. Use browser extension to download audio
2. Use Whisper AI or similar service for transcription
3. Add timestamps for key sections

### Option 3: Manual Transcription
1. Play video at 0.75x speed
2. Document key points with timestamps
3. Focus on:
   - UI demonstrations
   - Commands and shortcuts
   - Workflow steps
   - Technical specifications
   - Best practices mentioned

## Placeholder Sections

### Introduction [00:00 - XX:XX]
[Transcribe introduction]

### Main Content [XX:XX - XX:XX]
[Transcribe main demonstrations]

### Key Features Demonstrated
- Feature 1: [Description]
- Feature 2: [Description]
- Feature 3: [Description]

### Conclusion [XX:XX - XX:XX]
[Transcribe summary and closing]
"""
        return transcript
    
    def process_transcript(self, transcript: str) -> Dict:
        """Process transcript to extract key information"""
        sections = {
            'timestamps': [],
            'commands': [],
            'features': [],
            'workflows': [],
            'tips': []
        }
        
        # Extract timestamps (format: [HH:MM:SS] or [MM:SS])
        timestamp_pattern = r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]'
        sections['timestamps'] = re.findall(timestamp_pattern, transcript)
        
        # Extract commands (format: `command` or $command)
        command_pattern = r'[`$]([^`$\n]+)[`$]'
        sections['commands'] = re.findall(command_pattern, transcript)
        
        # Extract feature mentions
        feature_keywords = ['feature', 'function', 'capability', 'tool', 'module']
        for keyword in feature_keywords:
            pattern = rf'{keyword}[:\s]+([^.\n]+)'
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            sections['features'].extend(matches)
        
        return sections
    
    def generate_markdown(self, url: str, metadata: Dict, transcript: str, sections: Dict) -> str:
        """Generate formatted markdown document"""
        template = f"""# Teamcenter Training Video Transcript

## Video Information
- **URL**: {url}
- **Platform**: {metadata.get('platform', 'Unknown')}
- **Date Accessed**: {datetime.now().strftime('%Y-%m-%d')}
- **Transcription Status**: {'Complete' if transcript else 'Pending'}

## Summary
[To be added after transcription]

## Key Timestamps
{self._format_timestamps(sections.get('timestamps', []))}

## Commands & Shortcuts Mentioned
{self._format_commands(sections.get('commands', []))}

## Features Covered
{self._format_features(sections.get('features', []))}

## Full Transcript
{transcript}

## Epiroc Applications
[To be analyzed after transcription]

## Action Items
- [ ] Complete transcription
- [ ] Identify Epiroc-relevant features
- [ ] Extract best practices
- [ ] Create practice exercises
- [ ] Document integration points

## Notes
- This is a template for manual transcription
- Add actual content from the video
- Focus on mining equipment workflows
- Note any compliance-related features

---
*Generated by Teamcenter Video Transcription Tool*
"""
        return template
    
    def _format_timestamps(self, timestamps: List[str]) -> str:
        """Format timestamps list"""
        if not timestamps:
            return "- No timestamps extracted yet"
        return '\n'.join(f"- [{ts}] [Description]" for ts in timestamps[:10])
    
    def _format_commands(self, commands: List[str]) -> str:
        """Format commands list"""
        if not commands:
            return "- No commands extracted yet"
        return '\n'.join(f"- `{cmd}`: [Description]" for cmd in commands[:10])
    
    def _format_features(self, features: List[str]) -> str:
        """Format features list"""
        if not features:
            return "- No features extracted yet"
        return '\n'.join(f"- {feature.strip()}" for feature in features[:10])
    
    def save_transcript(self, url: str, content: str) -> Path:
        """Save transcript to file"""
        # Generate filename from URL
        safe_name = re.sub(r'[^\w\-_]', '_', url.split('/')[-1])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{safe_name}_{timestamp}.md"
        
        filepath = self.output_dir / filename
        filepath.write_text(content)
        logger.info(f"Transcript saved to: {filepath}")
        
        return filepath
    
    def update_sources(self, url: str, transcript_path: Path):
        """Update sources.json with processing status"""
        sources_file = Path("training/videos/raw/sources.json")
        if sources_file.exists():
            with open(sources_file, 'r') as f:
                data = json.load(f)
            
            # Find and update video entry
            for video in data.get('videos', []):
                if video.get('url') == url:
                    video['status'] = 'transcribed'
                    video['transcript_path'] = str(transcript_path)
                    video['processed_date'] = datetime.now().isoformat()
                    break
            
            # Update metadata
            data['metadata']['last_updated'] = datetime.now().isoformat()
            data['metadata']['processed'] = sum(1 for v in data['videos'] if v.get('status') == 'transcribed')
            data['metadata']['pending'] = sum(1 for v in data['videos'] if v.get('status') == 'pending')
            
            with open(sources_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Updated sources.json")

def main():
    parser = argparse.ArgumentParser(description='Transcribe Teamcenter training videos')
    parser.add_argument('--url', required=True, help='Video URL to transcribe')
    parser.add_argument('--output', default='training/videos/transcripts', help='Output directory')
    parser.add_argument('--update-sources', action='store_true', help='Update sources.json')
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = VideoTranscriber(output_dir=args.output)
    
    logger.info(f"Processing video: {args.url}")
    
    # Fetch metadata
    metadata = transcriber.fetch_video_metadata(args.url)
    
    # Extract transcript (placeholder for now)
    transcript = transcriber.extract_transcript(args.url)
    
    # Process transcript
    sections = transcriber.process_transcript(transcript)
    
    # Generate markdown
    content = transcriber.generate_markdown(args.url, metadata, transcript, sections)
    
    # Save transcript
    filepath = transcriber.save_transcript(args.url, content)
    
    # Update sources if requested
    if args.update_sources:
        transcriber.update_sources(args.url, filepath)
    
    logger.info("Transcription template created successfully!")
    logger.info(f"Next steps: Edit {filepath} with actual video content")

if __name__ == "__main__":
    main()