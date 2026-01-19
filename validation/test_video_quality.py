"""
Automated video quality checks
"""

import os

def validate_video_submission():
    """
    Check video meets technical requirements
    """
    
    # User might not have video yet, checking placeholders
    video_paths = [
        "docs/challenge/demo_video.mp4",
        "assets/demo.mp4",
        "demo_video.mp4"
    ]
    
    print("=== VIDEO VALIDATION ===\n")
    
    video_found = False
    for path in video_paths:
        if os.path.exists(path):
            print(f"✓ Video file found at {path}")
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"  File size: {size_mb:.1f} MB")
            video_found = True
            break
            
    if not video_found:
        print("⚠️  No video file found yet. Ensure it is placed in docs/challenge/ before submission.")
        print("  Requirement: < 3 minutes, < 500MB, 720p+ resolution")
    
    print("\n✅ Video technical validation script ready")
    print("\n⚠️  MANUAL CHECKS REQUIRED:")
    print("  - Watch full video for quality")
    print("  - Verify audio is clear and balanced")
    print("  - Check all text is readable")
    print("  - Ensure narrative flow is compelling")
    print("  - Verify captions are accurate")

if __name__ == "__main__":
    validate_video_submission()
