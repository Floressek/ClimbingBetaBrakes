# Climbing Route Creator - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Application Interface](#application-interface)
3. [Creating a Route](#creating-a-route)
4. [Editing and Adjustments](#editing-and-adjustments)
5. [Saving Your Route](#saving-your-route)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Operating System: Windows 10/11, Linux, or macOS
- Minimum Requirements:
  - 4GB RAM
  - Dual-core 2.0 GHz processor
  - 500MB free disk space

### Launching the Application
1. Run the application executable
2. You'll see a welcome screen with an image upload option
3. Either drag and drop an image or click the "Upload Wall Image" button

### Image Preparation
- Use JPG or PNG format images
- Ensure the climbing wall is well-lit
- Avoid images with heavy shadows or glare
- Recommended resolution: minimum 1920x1080 pixels

## Application Interface

### Toolbar
- **New Route** - starts a new route
- **Save Route** - saves the current route
- **Hands/Feet** - toggles between hand and foot hold selection modes
- **Edit Curves** - enables connection line editing mode
- **Instructions** - displays usage instructions
- **Grade Selector** - sets route difficulty

### Colors and Indicators
- Orange - hand holds
- Red - foot holds
- Gray - unselected holds
- Blue highlight - currently edited element

## Creating a Route

### Step 1: Loading the Image
1. Select your climbing wall photo
2. Wait for automatic hold detection
3. All detected holds will be highlighted in gray

### Step 2: Selecting Holds
1. Choose "Hands" or "Feet" mode from the toolbar
2. Click holds in sequence of use:
   - For hands: start → progression → top
   - For feet: follow the same logic
3. Holds will be automatically numbered in selection order

### Step 3: Editing Connections
1. Enable "Edit Curves" mode
2. Click the middle of a line to convert it to a curve
3. Drag control points to adjust the curve shape
4. Right-click on a line to toggle between straight and curved

## Editing and Adjustments

### Removing Selections
- Click a selected hold again to deselect it
- All subsequent holds will be automatically renumbered

### Changing Order
1. Deselect the hold you want to reposition in the sequence
2. Select it again at the desired point in the sequence

### Curve Editing
- Use control points to adjust curve shapes
- Toggle between straight lines and curves
- Curves help better visualize movement between holds

## Saving Your Route

### Step 1: Initiating Save
1. Click "Save Route" on the toolbar
2. Fill in the route information form:
   - Route name
   - Difficulty grade
   - Author
   - Description (optional)

### Step 2: Export
1. Choose save location
2. The route will be saved in two formats:
   - JSON file with route data
   - JPG image with route visualization

### Step 3: Verification
- Check if all information is correct
- Open the generated image to ensure everything is visible
- Return to editing if needed and save again

## Troubleshooting

### Hold Detection Issues
- Ensure image quality is good
- Check lighting conditions in the photo
- Try taking a new photo from a different angle

### Hold Selection Problems
- Make sure you're clicking precisely on the hold
- Verify the correct mode is selected (Hands/Feet)
- Try zooming in if holds are small

### Saving Issues
- Check that all required fields are filled
- Ensure you have write permissions in the selected location
- Verify sufficient disk space

### Storage and Compatibility
- Routes are stored in a standardized format
- Images and data can be backed up and transferred
- Compatible with all major operating systems

## Additional Tips

### Best Practices
- Take clear, well-lit photos of the wall
- Plan your route before starting to mark holds
- Use curves to indicate dynamic movements
- Add detailed descriptions for complex sequences

### Route Grading Tips
- Consider overall difficulty
- Factor in hold types and sizes
- Account for movement complexity
- Think about sequence length
