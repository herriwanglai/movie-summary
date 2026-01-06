# 🎯 Automatic Subtitle Detection & Extraction

## Overview

Enhance video upload process to automatically find and extract English subtitles from:
- Embedded subtitle tracks in video files
- External subtitle files (.srt, .vtt, .ass, .sub)
- Online subtitle databases (OpenSubtitles API)
- Auto-generated subtitles from video platforms

---

## 🔍 Subtitle Detection Pipeline

```
Video Upload Complete
        │
        ▼
┌─────────────────────────────────────────┐
│ Automatic Subtitle Detection            │
├─────────────────────────────────────────┤
│                                         │
│ 1. Check embedded subtitles             │
│    └─→ Extract subtitle tracks          │
│                                         │
│ 2. Scan for external files              │
│    └─→ Find .srt, .vtt, .ass files      │
│                                         │
│ 3. Search online databases              │
│    └─→ OpenSubtitles, SubDB, etc.       │
│                                         │
│ 4. Present options to user              │
│    └─→ Choose or use AI transcription   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎬 Embedded Subtitle Detection

### 1. Detect Subtitle Tracks

```python
# services/subtitle_detector.py
import ffmpeg
from typing import List, Optional

class SubtitleDetector:
    """Detect and extract subtitles from videos"""

    def __init__(self, video_path: str):
        self.video_path = video_path

    def detect_embedded_subtitles(self) -> List[SubtitleTrack]:
        """Detect subtitle tracks in video file"""

        try:
            # Probe video file for subtitle streams
            probe = ffmpeg.probe(self.video_path)

            subtitle_tracks = []
            for stream in probe['streams']:
                if stream['codec_type'] == 'subtitle':
                    track = SubtitleTrack(
                        index=stream['index'],
                        codec_name=stream.get('codec_name', 'unknown'),
                        language=stream.get('tags', {}).get('language', 'und'),
                        title=stream.get('tags', {}).get('title', ''),
                        is_default=stream.get('disposition', {}).get('default', 0) == 1,
                        is_forced=stream.get('disposition', {}).get('forced', 0) == 1
                    )
                    subtitle_tracks.append(track)

            return subtitle_tracks

        except ffmpeg.Error as e:
            print(f"Error detecting subtitles: {e}")
            return []

    def extract_subtitle_track(
        self,
        track_index: int,
        output_path: str
    ) -> Optional[str]:
        """Extract subtitle track to SRT file"""

        try:
            # Extract subtitle track
            (
                ffmpeg
                .input(self.video_path)
                .output(
                    output_path,
                    map=f'0:{track_index}',
                    format='srt'
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )

            return output_path

        except ffmpeg.Error as e:
            print(f"Error extracting subtitle: {e}")
            return None

    def get_english_subtitles(self) -> Optional[str]:
        """Get English subtitle track (auto-detect and extract)"""

        tracks = self.detect_embedded_subtitles()

        # Priority order: English, Default, First available
        english_tracks = [t for t in tracks if 'en' in t.language.lower()]

        if english_tracks:
            # Prefer non-forced subtitles
            preferred = [t for t in english_tracks if not t.is_forced]
            target_track = preferred[0] if preferred else english_tracks[0]
        elif tracks:
            # Fallback to default or first track
            default_tracks = [t for t in tracks if t.is_default]
            target_track = default_tracks[0] if default_tracks else tracks[0]
        else:
            return None

        # Extract to SRT
        output_path = self.video_path.replace('.mp4', f'_sub_{target_track.index}.srt')
        return self.extract_subtitle_track(target_track.index, output_path)
```

### 2. Data Models

```python
from dataclasses import dataclass
from typing import List

@dataclass
class SubtitleTrack:
    """Embedded subtitle track information"""
    index: int
    codec_name: str          # 'srt', 'ass', 'subrip', 'mov_text'
    language: str            # 'eng', 'und', 'chi', etc.
    title: str               # Track title/description
    is_default: bool
    is_forced: bool          # Forced subtitles (e.g., foreign language only)

@dataclass
class SubtitleFile:
    """External subtitle file"""
    path: str
    language: str
    format: str              # 'srt', 'vtt', 'ass', 'sub'
    encoding: str            # 'utf-8', 'latin1', etc.
    source: str              # 'embedded', 'external', 'online'
    confidence: float        # Match confidence (0-1)
```

---

## 📁 External Subtitle File Detection

### 1. Scan for Subtitle Files

```python
class ExternalSubtitleFinder:
    """Find external subtitle files"""

    SUBTITLE_EXTENSIONS = ['.srt', '.vtt', '.ass', '.ssa', '.sub']

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self.video_dir = self.video_path.parent
        self.video_name = self.video_path.stem

    def find_subtitle_files(self) -> List[SubtitleFile]:
        """Find subtitle files in same directory"""

        subtitle_files = []

        # Pattern matching for subtitle files
        patterns = [
            f"{self.video_name}*.srt",       # movie_name.srt
            f"{self.video_name}*.vtt",       # movie_name.vtt
            f"{self.video_name}*.ass",       # movie_name.ass
            f"{self.video_name}.en.srt",     # movie_name.en.srt
            f"{self.video_name}.eng.srt",    # movie_name.eng.srt
            f"{self.video_name}.english.srt" # movie_name.english.srt
        ]

        for pattern in patterns:
            matches = self.video_dir.glob(pattern)
            for file_path in matches:
                subtitle = self._analyze_subtitle_file(file_path)
                if subtitle:
                    subtitle_files.append(subtitle)

        return self._rank_by_quality(subtitle_files)

    def _analyze_subtitle_file(self, file_path: Path) -> Optional[SubtitleFile]:
        """Analyze subtitle file"""

        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = self._detect_encoding(raw_data)

            # Detect language from filename
            filename = file_path.stem.lower()
            language = self._detect_language_from_filename(filename)

            # Validate subtitle format
            if not self._is_valid_subtitle_file(file_path, encoding):
                return None

            return SubtitleFile(
                path=str(file_path),
                language=language,
                format=file_path.suffix[1:],  # Remove dot
                encoding=encoding,
                source='external',
                confidence=self._calculate_confidence(file_path, language)
            )

        except Exception as e:
            print(f"Error analyzing subtitle file: {e}")
            return None

    def _detect_encoding(self, raw_data: bytes) -> str:
        """Detect file encoding"""
        import chardet

        result = chardet.detect(raw_data)
        return result['encoding'] or 'utf-8'

    def _detect_language_from_filename(self, filename: str) -> str:
        """Detect language from filename"""

        # English indicators
        if any(indicator in filename for indicator in ['.en.', '.eng.', '.english.', 'english']):
            return 'eng'

        # Common language codes
        language_codes = {
            '.es.': 'spa', '.spanish.': 'spa',
            '.fr.': 'fra', '.french.': 'fra',
            '.de.': 'deu', '.german.': 'deu',
            '.zh.': 'chi', '.chinese.': 'chi',
            '.ja.': 'jpn', '.japanese.': 'jpn',
            '.ko.': 'kor', '.korean.': 'kor',
        }

        for indicator, code in language_codes.items():
            if indicator in filename:
                return code

        # Default to unknown
        return 'und'

    def _is_valid_subtitle_file(self, file_path: Path, encoding: str) -> bool:
        """Validate subtitle file format"""

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read(1000)  # Read first 1000 chars

                # Check for SRT format
                if file_path.suffix == '.srt':
                    return bool(re.search(r'^\d+\s*$', content, re.MULTILINE))

                # Check for VTT format
                if file_path.suffix == '.vtt':
                    return content.startswith('WEBVTT')

                # Check for ASS format
                if file_path.suffix in ['.ass', '.ssa']:
                    return '[Script Info]' in content

                return True

        except Exception:
            return False

    def _calculate_confidence(self, file_path: Path, language: str) -> float:
        """Calculate match confidence"""

        confidence = 0.5

        # Boost if filename matches exactly
        if file_path.stem == self.video_name:
            confidence += 0.3

        # Boost if English
        if language == 'eng':
            confidence += 0.2

        # Boost if common format
        if file_path.suffix == '.srt':
            confidence += 0.1

        return min(1.0, confidence)

    def _rank_by_quality(self, subtitles: List[SubtitleFile]) -> List[SubtitleFile]:
        """Rank subtitles by quality/confidence"""

        return sorted(subtitles, key=lambda s: (
            s.language == 'eng',        # English first
            s.confidence,               # Higher confidence
            s.format == 'srt',          # Prefer SRT format
        ), reverse=True)
```

---

## 🌐 Online Subtitle Database Search

### 1. OpenSubtitles API Integration

```python
class OnlineSubtitleFinder:
    """Find subtitles from online databases"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENSUBTITLES_API_KEY')
        self.base_url = 'https://api.opensubtitles.com/api/v1'

    async def search_subtitles(
        self,
        video_path: str,
        language: str = 'en'
    ) -> List[SubtitleFile]:
        """Search for subtitles online"""

        # Calculate file hash (OpenSubtitles standard)
        file_hash = self._calculate_opensubtitles_hash(video_path)
        file_size = os.path.getsize(video_path)

        # Extract movie info from filename
        movie_info = self._parse_filename(video_path)

        # Search by hash (most accurate)
        results = await self._search_by_hash(file_hash, file_size, language)

        # If no results, search by filename
        if not results and movie_info['title']:
            results = await self._search_by_title(movie_info, language)

        return results

    def _calculate_opensubtitles_hash(self, video_path: str) -> str:
        """Calculate OpenSubtitles hash"""

        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        with open(video_path, 'rb') as f:
            filesize = os.path.getsize(video_path)
            hash_value = filesize

            if filesize < 65536 * 2:
                return "SizeError"

            # Read first 64KB
            for _ in range(65536 // bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash_value += l_value
                hash_value &= 0xFFFFFFFFFFFFFFFF  # 64-bit

            # Read last 64KB
            f.seek(max(0, filesize - 65536), 0)
            for _ in range(65536 // bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash_value += l_value
                hash_value &= 0xFFFFFFFFFFFFFFFF

        return "%016x" % hash_value

    async def _search_by_hash(
        self,
        file_hash: str,
        file_size: int,
        language: str
    ) -> List[SubtitleFile]:
        """Search by file hash"""

        headers = {
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        params = {
            'moviehash': file_hash,
            'moviebytesize': file_size,
            'languages': language
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.base_url}/subtitles',
                headers=headers,
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_results(data)

        return []

    async def _download_subtitle(
        self,
        subtitle_id: str,
        output_path: str
    ) -> Optional[str]:
        """Download subtitle file"""

        headers = {'Api-Key': self.api_key}

        async with aiohttp.ClientSession() as session:
            # Request download link
            async with session.post(
                f'{self.base_url}/download',
                headers=headers,
                json={'file_id': subtitle_id}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    download_url = data['link']

                    # Download file
                    async with session.get(download_url) as dl_response:
                        content = await dl_response.read()

                        # Save to file
                        with open(output_path, 'wb') as f:
                            f.write(content)

                        return output_path

        return None

    def _parse_filename(self, video_path: str) -> dict:
        """Parse movie info from filename"""
        import re

        filename = Path(video_path).stem

        # Try to extract title and year
        # Pattern: Movie.Title.2023.1080p.BluRay.x264
        pattern = r'(.+?)\.(\d{4})'
        match = re.search(pattern, filename)

        if match:
            title = match.group(1).replace('.', ' ').strip()
            year = match.group(2)
        else:
            title = filename.replace('.', ' ').strip()
            year = None

        return {
            'title': title,
            'year': year,
            'filename': filename
        }
```

---

## 🎯 User Interface

### 1. Subtitle Selection Dialog

```tsx
// components/SubtitleSelector/SubtitleSelector.tsx
interface SubtitleSelectorProps {
  videoId: string;
  embeddedSubtitles: SubtitleTrack[];
  externalSubtitles: SubtitleFile[];
  onlineSubtitles: SubtitleFile[];
  onSelect: (subtitle: SubtitleSource) => void;
}

export const SubtitleSelector: React.FC<SubtitleSelectorProps> = ({
  videoId,
  embeddedSubtitles,
  externalSubtitles,
  onlineSubtitles,
  onSelect
}) => {
  const [selectedSource, setSelectedSource] = useState<SubtitleSource | null>(null);

  const allSubtitles = [
    ...embeddedSubtitles.map(s => ({ ...s, source: 'embedded' })),
    ...externalSubtitles,
    ...onlineSubtitles
  ];

  // Auto-select best English subtitle
  const bestEnglish = allSubtitles.find(s =>
    s.language === 'eng' || s.language.includes('en')
  );

  useEffect(() => {
    if (bestEnglish) {
      setSelectedSource(bestEnglish);
    }
  }, [bestEnglish]);

  return (
    <Dialog open>
      <DialogTitle>
        📝 Subtitles Found
      </DialogTitle>

      <DialogContent>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Choose a subtitle source or use AI transcription
        </Typography>

        <RadioGroup
          value={selectedSource?.id}
          onChange={(e) => {
            const subtitle = allSubtitles.find(s => s.id === e.target.value);
            setSelectedSource(subtitle);
          }}
        >
          {/* Embedded Subtitles */}
          {embeddedSubtitles.length > 0 && (
            <>
              <Typography variant="h6" sx={{ mt: 2 }}>
                Embedded Subtitles
              </Typography>
              {embeddedSubtitles.map(sub => (
                <FormControlLabel
                  key={sub.index}
                  value={sub.id}
                  control={<Radio />}
                  label={
                    <Box>
                      <Typography>
                        {sub.title || `Track ${sub.index}`}
                        {sub.is_default && <Chip label="Default" size="small" />}
                        {sub.language === 'eng' && <Chip label="English" size="small" color="primary" />}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        Format: {sub.codec_name} • Language: {sub.language}
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </>
          )}

          {/* External Files */}
          {externalSubtitles.length > 0 && (
            <>
              <Typography variant="h6" sx={{ mt: 2 }}>
                External Files
              </Typography>
              {externalSubtitles.map(sub => (
                <FormControlLabel
                  key={sub.path}
                  value={sub.id}
                  control={<Radio />}
                  label={
                    <Box>
                      <Typography>
                        {Path.basename(sub.path)}
                        {sub.language === 'eng' && <Chip label="English" size="small" color="primary" />}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        Format: {sub.format} • Confidence: {(sub.confidence * 100).toFixed(0)}%
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </>
          )}

          {/* Online Subtitles */}
          {onlineSubtitles.length > 0 && (
            <>
              <Typography variant="h6" sx={{ mt: 2 }}>
                Online Subtitles
              </Typography>
              {onlineSubtitles.map(sub => (
                <FormControlLabel
                  key={sub.id}
                  value={sub.id}
                  control={<Radio />}
                  label={
                    <Box>
                      <Typography>
                        {sub.title}
                        {sub.language === 'eng' && <Chip label="English" size="small" color="primary" />}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        Source: {sub.source} • Downloads: {sub.download_count}
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </>
          )}

          {/* AI Transcription */}
          <Divider sx={{ my: 2 }} />
          <FormControlLabel
            value="ai_transcribe"
            control={<Radio />}
            label={
              <Box>
                <Typography>
                  🤖 AI Transcription (Whisper)
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Generate new transcription using AI (~5-10 minutes)
                </Typography>
              </Box>
            }
          />
        </RadioGroup>

        {/* Preview */}
        {selectedSource && selectedSource !== 'ai_transcribe' && (
          <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
            <Typography variant="subtitle2">Preview:</Typography>
            <Box sx={{ mt: 1, maxHeight: 200, overflow: 'auto' }}>
              <SubtitlePreview subtitle={selectedSource} />
            </Box>
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={() => onSelect('skip')}>
          Skip (Add Later)
        </Button>
        <Button
          onClick={() => onSelect(selectedSource)}
          variant="contained"
          disabled={!selectedSource}
        >
          Use This Subtitle
        </Button>
      </DialogActions>
    </Dialog>
  );
};
```

---

## 🔄 Updated Upload Workflow

```
Upload Complete
        │
        ▼
┌───────────────────────────────────────┐
│ Automatic Subtitle Detection          │
│ 🔍 Searching for subtitles...         │
├───────────────────────────────────────┤
│ ✓ Found 2 embedded tracks             │
│ ✓ Found 1 external file               │
│ ⏳ Searching online database...       │
└────────────┬──────────────────────────┘
             │
             ▼
┌───────────────────────────────────────┐
│ Subtitles Found! 📝                   │
├───────────────────────────────────────┤
│ Embedded:                             │
│ ○ Track 1: English (Default)          │
│ ○ Track 2: Spanish                    │
│                                       │
│ External Files:                       │
│ ● movie.en.srt (95% match)            │
│                                       │
│ Online:                               │
│ ○ OpenSubtitles - English (HD)       │
│                                       │
│ ○ 🤖 AI Transcription (Whisper)      │
│                                       │
│ [Skip] [Use Selected]                │
└────────────┬──────────────────────────┘
             │
             ▼
Process Selected Subtitle
        │
        ├─→ If embedded: Extract track
        ├─→ If external: Parse file
        ├─→ If online: Download
        └─→ If AI: Run Whisper
        │
        ▼
Convert to Standard Format (SRT)
        │
        ▼
Store in Database
        │
        ▼
Ready for Analysis! ✅
```

---

## 📊 Database Schema Updates

```sql
-- Add subtitle sources table
CREATE TABLE subtitle_sources (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos(id),
  source_type VARCHAR(50),  -- 'embedded', 'external', 'online', 'ai'
  language VARCHAR(10),
  format VARCHAR(20),
  file_path VARCHAR(512),
  is_active BOOLEAN DEFAULT FALSE,
  confidence FLOAT,
  created_at TIMESTAMP
);

-- Add subtitle segments (parsed)
CREATE TABLE subtitle_segments (
  id UUID PRIMARY KEY,
  source_id UUID REFERENCES subtitle_sources(id),
  sequence_number INTEGER,
  start_time FLOAT,
  end_time FLOAT,
  text TEXT,
  created_at TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX idx_subtitle_segments_time
ON subtitle_segments(source_id, start_time, end_time);
```

---

## 🚀 API Endpoints

```python
# Detect subtitles in uploaded video
POST /api/videos/{video_id}/detect-subtitles
Response: {
  "embedded": [...],
  "external": [...],
  "online": [...]
}

# Select subtitle source
POST /api/videos/{video_id}/select-subtitle
Body: {
  "sourceType": "embedded",
  "sourceId": "track_0"
}
Response: {
  "success": true,
  "subtitleId": "uuid",
  "segmentCount": 1234
}

# Search online subtitles
GET /api/subtitles/search?videoId=xxx&language=en
Response: {
  "results": [...]
}

# Download subtitle
POST /api/subtitles/download
Body: {
  "subtitleId": "external_id",
  "videoId": "uuid"
}
```

---

## ✅ Summary

### Features Added:

1. **Embedded Subtitle Detection**
   - Detect all subtitle tracks in video
   - Identify languages
   - Extract to SRT format
   - Auto-select English

2. **External File Detection**
   - Scan directory for .srt, .vtt, .ass files
   - Detect language from filename
   - Validate format
   - Rank by quality/confidence

3. **Online Subtitle Search**
   - OpenSubtitles API integration
   - Search by file hash (most accurate)
   - Search by movie title/year
   - Download and save

4. **Smart Selection**
   - Auto-detect best English subtitle
   - Present all options to user
   - Preview before selection
   - Fall back to AI transcription

5. **User Experience**
   - Automatic detection on upload
   - Clear subtitle selection dialog
   - Preview functionality
   - Option to skip or use AI

**This eliminates manual transcription when subtitles exist!** 🎯✨
