#!/usr/bin/env python3
"""
Camera Intel - Step 1: Frame Extraction
This script extracts frames from video files at regular intervals
"""

import os
import cv2
import argparse
import json
from datetime import datetime
import logging
import glob


def setup_logging(debug=False):
    """Configure logging based on debug mode"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def create_directories():
    """Create the necessary directory structure if it doesn't exist"""
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    logging.info("Directory structure verified")


def extract_frames(video_path, output_dir, frame_interval=1):
    """
    Extract frames from the video at specified intervals
    video_path: Path to the input video file
    output_dir: Directory to save the extracted frames
    frame_interval: Extract one frame every N seconds (default: 1)
    """
    # Get the base name of the video file (without extension)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Create output directory for this video
    video_output_dir = os.path.join(output_dir, video_name)
    os.makedirs(video_output_dir, exist_ok=True)
    
    logging.info(f"Processing video: {video_path}")
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        logging.error(f"Error: Could not open video {video_path}")
        return False
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    
    logging.info(f"Video FPS: {fps}, Total frames: {frame_count}, Duration: {duration:.2f}s")
    
    # Calculate frame interval in terms of frame count
    frame_interval_count = int(fps * frame_interval)
    
    # Initialize variables
    frame_number = 0
    saved_frames = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Extract frames at specified interval
        if frame_number % frame_interval_count == 0:
            # Calculate timestamp
            timestamp_seconds = frame_number / fps
            timestamp = f"{int(timestamp_seconds // 60):02d}:{int(timestamp_seconds % 60):02d}"
            
            # Create frame directory
            frame_id = f"frame{saved_frames + 1}"
            frame_dir = os.path.join(video_output_dir, frame_id)
            os.makedirs(frame_dir, exist_ok=True)
            
            # Save frame image
            frame_path = os.path.join(frame_dir, f"{frame_id}.jpg")
            cv2.imwrite(frame_path, frame)
            
            # Create initial JSON metadata file
            json_data = {
                "frame_id": frame_id,
                "timestamp": timestamp,
                "description": "",
                "processing_time": datetime.now().isoformat()
            }
            
            json_path = os.path.join(frame_dir, f"{frame_id}.json")
            with open(json_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            logging.debug(f"Saved frame {frame_id} at timestamp {timestamp}")
            saved_frames += 1
        
        frame_number += 1
    
    cap.release()
    logging.info(f"Extracted {saved_frames} frames from {video_path}")
    return True


def process_videos(input_dir, output_dir, debug=False):
    """Process all video files in the input directory"""
    # Supported video formats
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    
    # Get all video files in input directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    if not video_files:
        logging.warning(f"No video files found in {input_dir}")
        return
    
    logging.info(f"Found {len(video_files)} video file(s) to process")
    
    for video_path in video_files:
        extract_frames(video_path, output_dir)
    
    logging.info("All videos processed successfully")


def main():
    """Main function to execute the frame extraction pipeline"""
    parser = argparse.ArgumentParser(description='Camera Intel - Frame Extraction Tool')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--input', default='input', help='Input directory containing video files')
    parser.add_argument('--output', default='output', help='Output directory for extracted frames')
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    
    # Create necessary directories
    create_directories()
    
    # Process videos
    process_videos(args.input, args.output, args.debug)


if __name__ == "__main__":
    main() 