import time
import edgeiq
import numpy
"""
Simultaneously utilize two object detection models and present the results to
a single output stream.

The models used in this app are ssd_inception_v2_coco_2018_01_28, which can detect
numerous inanimate objects, such as bikes, utensils, animals, etc., and the
the mobilenet_ssd, which is a smaller library but detects some larger objects that
ssd_inception_v2_coco_2018_01_28 does not, such as a sofa, a train, or an airplane.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():

    # if you would like to test an additional model, add one to the list below:
    models = ["alwaysai/mobilenet_ssd", "alwaysai/ssd_inception_v2_coco_2018_01_28"]

    # if you've added a model, add a new color in as a list of tuples in BGR format
    # to make visualization easier (e.g. [(B, G, R)]).
    colors = [[(66, 68, 179)], [(50, 227, 62)]]

    detectors = []

    # load all the models (creates a new object detector for each model)
    for model in models:

        # start up a first object detection model
        obj_detect = edgeiq.ObjectDetection(model)
        obj_detect.load(engine=edgeiq.Engine.DNN)

        # track the generated object detection items by storing them in detectors
        detectors.append(obj_detect)

        # print the details of each model to the console
        print("Model:\n{}\n".format(obj_detect.model_id))
        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()

                text = [""]

                # gather data from the all the detectors
                for i in range(0, len(detectors)):
                    results = detectors[i].detect_objects(
                        frame, confidence_level=.5)
                    object_frame = edgeiq.markup_image(
                        frame, results.predictions, show_labels=False, colors=colors[i])

                    # for the first frame, overwrite the input feed
                    if i == 0:
                        display_frame = object_frame
                    else:

                        # otherwise, append the new marked-up frame to the previous one
                        display_frame = numpy.concatenate((object_frame, display_frame))

                    # append each prediction
                    for prediction in results.predictions:
                        text.append(
                                "Model {} detects {}: {:2.2f}%".format(detectors[i].model_id,
                                prediction.label, prediction.confidence * 100))

                # send the image frame and the predictions for both
                # prediction models to the output stream
                streamer.send_data(display_frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
