import onnxruntime as ort

# Create a session
session = ort.InferenceSession("path_to_model.onnx")
print("onnxruntime loaded successfully")
