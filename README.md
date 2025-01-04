# CyberSplit - Secure File Splitting Utility

<p align="center">
  <img src="assets/file.ico" width="150" alt="CyberSplit Logo">
</p>

## About
CyberSplit is a secure offline file splitting and compression utility with a cyberpunk-themed interface. Split large files into manageable chunks and merge them back together without any data modification or internet connectivity.

## Key Benefits
- 🔒 100% Offline Operation - No internet required
- 🛡️ Zero Data Modification - Files remain unaltered
- 🔐 No Cloud Storage - Everything stays on your machine
- 🎯 Simple & Focused - Does one job and does it well
- ⚡ Fast Performance - Optimized for speed

## Download & Install
1. Download the latest release from the Releases page
2. Run the installer (CyberSplit_Setup.exe)
3. Launch CyberSplit from your Start Menu

## Quick Start Guide

### Splitting Files
1. Click [SPLIT_MODE] tab
2. Select input file using [ SELECT_FILE ]
3. Choose output directory with [ SELECT_DIR ] 
4. Set chunk size in MB (1-1000)
5. Click [ EXECUTE_SPLIT ]
6. Files will be created as: filename.000, filename.001, etc.

### Merging Files
1. Click [MERGE_MODE] tab
2. Click [ ADD_CHUNKS ] to select split files
3. Ensure chunks are in correct order (.000, .001, etc.)
4. Click [ EXECUTE_MERGE ]
5. Original file will be reconstructed


## Important Notes
- Keep chunks in sequence (.000, .001, etc.)
- Do not rename chunk files
- Ensure enough disk space
- No internet connection needed
- Files never leave your computer

## Antivirus Information
Some antivirus software may flag CyberSplit as suspicious. This is a false positive due to:
- The executable being packed with PyInstaller
- File manipulation capabilities
- Not being a widely recognized publisher

### Why CyberSplit is Safe:
- ✅ 100% Open Source - All code is visible and verifiable
- ✅ No Network Access - Works completely offline
- ✅ No System Changes - Only reads/writes user-selected files
- ✅ No Data Collection - Zero telemetry or tracking
- ✅ Transparent Operation - Clear visual feedback of all actions

### If Your Antivirus Blocks CyberSplit:
1. Verify you downloaded from official releases
2. Check file hash matches release hash
3. Add CyberSplit to antivirus exclusions
4. Run source code directly if preferred

## Support
Having issues? Check the [HELP] tab in the application for troubleshooting steps.

### DONATE
BTC ADDRESS:
 bc1qhwfd6zm7t7uqrk77uc5t788h4h6sadw48mqfzn
