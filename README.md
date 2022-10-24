# Facecurity

Essentially, there are three components to the application. The Chrome Extension, the website, and facial recognition script. 
The Chrome extension was created through the use of Google Developer API in chrome web extensions. 
Through a combo of Json, Javascript, CSS, and HTML, we created a pop up based extension that would link to the second part of the application, the website.
The website is a hub for users to create a Facecurity account. Upon registering, an initial photo is provided by the user. 
This is used to train the face recognition model. Blocked websites are listed on the dashboard section of the websites, 
and these sites require facial matching. The face-recognition library in python is useful for matching faces using user webcam data. 
Using the initial photo, the algorithm is able to detect the presence of the same face in another picture. For subsequent logins to websites where the 
user enabled facecurity, new user pictures must be provided. Once the match has been confirmed, the user is redirected back to the original site they 
enabled facecurity on. 

For facial recognition, you need to install PythonV3+, OpenCV, CMake, Dlib, and the facial recognition python library. 
