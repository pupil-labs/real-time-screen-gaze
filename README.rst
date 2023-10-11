=====================
Real-time Screen Gaze
=====================
This package is designed to allow users of the Pupil Labs eyetracking hardware, especially `Neon <https://pupil-labs.com/products/neon/>`_, to acquire screen-based gaze coordinates in realtime without relying on `Pupil Core software <https://github.com/pupil-labs/pupil>`_.

This works by identifying the image of the display as it appears in the scene camera. We accomplish this with `AprilTags <https://april.eecs.umich.edu/software/apriltag>`_, 2D barcodes similar to QR codes. This package provides a ``marker_generator`` module to create AprilTag image data.

.. code-block:: python

   from pupil_labs.real_time_screen_gaze import marker_generator
   ...

   marker_pixels = marker_generator.generate_marker(marker_id=0)


More markers will yield higher accuracy, and we recommend a minimum of four. Each marker must be unique, and the ``marker_id`` parameter is provided for this purpose.

Once you've drawn the markers to the screen using your GUI toolkit of choice, you'll next need to setup a ``GazeMapper`` object. This requires calibration data for the scene camera.

.. code-block:: python

   from pupil_labs.realtime_api.simple import discover_one_device
   from pupil_labs.real_time_screen_gaze.gaze_mapper import GazeMapper
   ...

   device = discover_one_device()
   calibration = device.get_calibration()
   gaze_mapper = GazeMapper(calibration)


Now that we have a ``GazeMapper`` object, we need to specify which AprilTag markers we're using and where they appear on the screen.

.. code-block:: python

   marker_verts = {
      0: [ # marker id 0
         (32, 32), # Top left marker corner
         (96, 32), # Top right
         (96, 96), # Bottom right
         (32, 96), # Bottom left
      ],
      ...
   }

   screen_size = (1920, 1080)

   screen_surface = gaze_mapper.add_surface(
      marker_verts,
      screen_size
   )

Here, ``marker_verts`` is a dictionary whose keys are the IDs of the markers we'll be drawing to the screen. The value for each key is a list of the 2D coordinates of the four corners of the marker, starting with the top left and going clockwise.

With that, setup is complete and we're ready to start mapping gaze to the screen! On each iteration of our main loop we'll grab a video frame from the scene camera and gaze data from the Realtime API. We pass those along to our ``GazeMapper`` instance for processing, and it returns our gaze positions mapped to screen coordinates.

.. code-block:: python

   from pupil_labs.realtime_api.simple import discover_one_device
   ...

   device = discover_one_device(max_search_duration_seconds=10)

   while True:
      frame, gaze = device.receive_matched_scene_video_frame_and_gaze()
      result = gaze_mapper.process_frame(frame, gaze)

      for surface_gaze in result.mapped_gaze[screen_surface.uid]:
         printf(f"Gaze at {surface_gaze.x}, {surface_gaze.y}")
