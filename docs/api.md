## **Using the Roboflow API in Climbing Route Creator**

The **Climbing Route Creator** application utilizes the **Roboflow Hold Detector** model to provide advanced computer vision capabilities for detecting climbing holds in images. This integration allows climbers to easily identify holds on climbing walls, facilitating the creation of custom climbing routes.

---

### **Overview of the Roboflow API**
The Roboflow Hold Detector is a powerful model designed to detect climbing holds in images with high accuracy. It is built to streamline the process of analyzing climbing wall images and extracting hold positions.

**Model Information:**
- **Model Name:** Hold Detector
- **Version:** 2
- **API Documentation:** [Roboflow Hold Detector](https://universe.roboflow.com/climb-ai/hold-detector-rnvkl/model/2)

**Key Features:**
- Detects holds in images with specified confidence and overlap thresholds.
- Provides coordinates of detected holds for route creation.
- Supports multiple image formats (e.g., JPEG, PNG).

---

### **How It Works**
1. **Image Upload**:
   Users can upload an image of a climbing wall. The image is sent to the Roboflow API for analysis.

2. **Hold Detection**:
   The Roboflow API processes the image using the Hold Detector model and returns predictions, including:
   - **Bounding Boxes:** Define the location of holds.
   - **Confidence Scores:** Indicate the likelihood that a detected region is a hold.

3. **Route Creation**:
   The detected holds are visualized in the application, allowing users to:
   - Select holds for their custom route.
   - Add descriptions and share the route with the community.

---

### **API Integration**
#### **Endpoints**
- **Hold Detection API**:  
  Sends an image for analysis and retrieves hold predictions.  
  Example request:
  ```http
  POST https://detect.roboflow.com/hold-detector/2
  ```

#### **Required Parameters**:
- `api_key`: Your Roboflow API key (retrieved from environment variables in the application).
- `confidence_threshold`: Minimum confidence for a hold to be considered valid (e.g., 0.4).
- `overlap_threshold`: Threshold for overlapping detections (e.g., 0.3).

#### **Sample API Request**:
```python
import requests

url = "https://detect.roboflow.com/hold-detector/2"
api_key = "YOUR_API_KEY"
image_path = "path/to/image.jpg"
params = {
    "api_key": api_key,
    "confidence": 0.4,
    "overlap": 0.3
}
files = {"file": open(image_path, "rb")}
response = requests.post(url, params=params, files=files)

print(response.json())
```

---

### **Example Output**
The API returns a JSON object with details of the detected holds. Sample response:
```json
{
  "predictions": [
    {
      "class": "hold",
      "x": 150,
      "y": 200,
      "width": 50,
      "height": 50,
      "confidence": 0.92
    },
    {
      "class": "hold",
      "x": 300,
      "y": 400,
      "width": 60,
      "height": 60,
      "confidence": 0.87
    }
  ]
}
```

- **`x` and `y`**: Coordinates of the center of the hold.
- **`width` and `height`**: Dimensions of the bounding box.
- **`confidence`**: Confidence score for the detection.

---

### **Future Enhancements**
- Support for additional hold types and classifications.
- Improved detection accuracy using custom-trained models.
- Offline hold detection with pre-downloaded models.

This integration enables climbers to focus on creating and sharing routes without worrying about manual hold identification. For more details, visit [Roboflow Universe](https://universe.roboflow.com/climb-ai/hold-detector-rnvkl/model/2).