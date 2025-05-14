# Camera Intel Project

## Project Overview

Camera Intel is a tool that processes video files to extract frames at regular intervals and then uses ChatGPT to generate detailed descriptions of each frame. This tool is particularly useful for security analysis, content cataloging, or automatic video summarization.

## Project Structure

The project will be organized as follows:

```
camera-intel/
├── input/                   # Directory for input video files
├── output/                  # Directory for processed frames
│   ├── frame1/              # Directory for each frame
│   │   ├── frame1.jpg       # The extracted image
│   │   └── frame1.json      # ChatGPT's description in JSON format
│   ├── frame2/
│   │   ├── frame2.jpg
│   │   └── frame2.json
│   └── ...
├── response.json            # Compiled JSON file containing all responses
├── camera_intel.py           # Main Python script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Step 1: Extract Frames from Video

### Requirements

To run this project, you'll need the following:

1. Python 3.7 or higher
2. FFmpeg installed on your system
3. Python libraries (specified in requirements.txt):
   - opencv-python
   - ffmpeg-python
   - requests
   - python-dotenv

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/camera-intel.git
   cd camera-intel
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Install FFmpeg:
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: Use Homebrew: `brew install ffmpeg`
   - **Linux**: Use package manager: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

5. Create the input and output directories:
   ```
   mkdir -p input output
   ```

### How Frame Extraction Works

The script uses FFmpeg to extract one frame per second from the video file. Each frame is saved as a JPEG image in its own directory within the output folder.

To use the script:

1. Place your MP4 video file(s) in the `input` directory
2. Run the script with: `python camera_intel.py`

The script will:
1. Scan the input directory for video files
2. For each video:
   - Create an output directory structure
   - Extract frames at 1-second intervals
   - Save each frame as a JPEG in its own directory

## Step 2: Process Images with ChatGPT

### API Setup

To use the ChatGPT API for image description, you'll need:

1. An OpenAI API key with access to GPT-4 Vision
2. Create a `.env` file in the project root with your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### The Image Processing Workflow

For each extracted frame, the script will:

1. Send the image to the ChatGPT API
2. Use the prompt: "Describe this image in a detailed way. Imagine you're a security officer trying to extract important information from this image."
3. Save the API response in a JSON file in the same directory as the frame
4. Compile all responses into a single `response.json` file for easy access

### JSON Structure

Each frame's JSON file will contain:

```json
{
  "frame_id": "frame1",
  "timestamp": "00:00:01",
  "description": "The image shows...",
  "processing_time": "2023-05-15T14:30:45Z"
}
```

The compiled `response.json` will contain an array of all frame descriptions.

## Running the Complete Pipeline

To run the entire process:

1. Place your video files in the `input` directory
2. Ensure your OpenAI API key is set in the `.env` file
3. Run the script: `python camera_intel.py`
4. The script will:
   - Extract frames from all videos in the input directory
   - Process each frame with ChatGPT
   - Save individual JSON files for each frame
   - Create a compiled `response.json` file

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Ensure FFmpeg is installed and in your system PATH
2. **API Rate Limiting**: If you hit OpenAI's rate limits, the script will pause and retry
3. **Large Video Files**: Processing large videos might take significant time and API credits

### Debug Mode

Add the `--debug` flag to enable verbose logging:
```
python camera_intel.py --debug
```

## Code Implementation Overview

The Python code will:

1. Use FFmpeg to extract frames from videos
2. Create the directory structure for each frame
3. Process each image with the OpenAI API
4. Save individual and compiled JSON responses

## Next Steps

- Add support for batch processing multiple videos
- Implement a web interface for easier interaction
- Add options for different frame extraction rates

## License

This project is licensed under the MIT License - see the LICENSE file for details. 