# # Use the official OpenCV Python image as the base image
# FROM opencv-python:4.5.4

# # Copy the script and video into the container
# COPY Vehicle.py /Vehicle_project/Vehicle.py
# COPY video.mp4 /Vehicle_project/video.mp4

# # Set the working directory
# WORKDIR /Vehicle_project

# # Install any needed packages
# RUN pip install numpy

# # Run the script when the container starts
# CMD ["python", "Vehicle.py"]

# Use the official Python image as the base image
FROM python:3.8

# Copy the script and video into the container
COPY Vehicle.py /Vehicle_project/Vehicle.py
COPY video.mp4 /Vehicle_project/video.mp4

# Set the working directory
WORKDIR /Vehicle_project

# Install OpenCV and other needed packages
RUN pip install opencv-python-headless numpy cv2

# Run the script when the container starts
CMD ["python", "Vehicle.py"]
