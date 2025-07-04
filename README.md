# NSFW_checker
NSFW_checker is based of Fast API and use Deep AI and Sightengine.

To run this NSFW checker, first activate your Python environment and start the FastAPI server.
Then, open your browser and go to http://localhost:8000 to ensure it's running.

You can test the /moderate_sightengine/ endpoint using the following example command:
curl -X POST -F "file=@image.jpg" http://localhost:8000/moderate_sightengine/
