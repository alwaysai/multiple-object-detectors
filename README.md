This app utilizes two object detection models, with the option of adding additional detection models. This may be helpful for including models that comprise very different libraries. In this example, one model detects numerous objects of small to medium size, and the other has a more limited library but detects some larger objects, such as airplanes, trains, and sofas. As there is some overlap between models, for instance they both detect people, you can compare the prediction confidences. The different model's output appears in separate video frames.


To run this app, you will need an alwaysAI account. Please register at https://alwaysai.co/auth?register=true


Easy start up guides can be found following registration. Please see the docs page for more information: https://alwaysai.co/docs/getting_started/introduction.html


If you are having trouble connecting to your edge device, use the CLI configure command to reset the device. Please see the following page for more details: https://alwaysai.co/docs/reference/cli_commands.html


You can alter the code to used different detection and classification models: https://alwaysai.co/docs/application_development/changing_the_model.html


Additional notes:
For convenience, there is a variable called 'colors' included in the code. Should you alter 'models' to include more than two detection models, also include a new list of tuples to be used as the color to mark up the detected objects in the new model. In the included code, each 'list' contains only one tuple, so all detection boxes for a given model will appear with that color.