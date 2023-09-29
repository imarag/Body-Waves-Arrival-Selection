# Body-Waves-Arrival-Selection
This project focuses on the precise determination of arrival times for P and S waves. It employs the Python PyQt5 library to create a user-friendly graphical interface and utilizes the Pyqtgraph library for plotting recorded data. The project takes MiniSEED data files as input and extracts the arrival times of body waves, measured in seconds from the waveforms' starting time. It proves particularly valuable when you have multiple MiniSEED files located within a directory on your machine, streamlining the process of arrival time selection.


Start by running the python script:

![PS_arr_run_script](https://github.com/imarag/Body-Waves-Arrival-Selection/assets/97481016/ab75d3c5-f236-4d2e-ad82-7d1e30b2b3a2)

Open the MiniSEED data file to plot the recordings:

![PS_arr_load_mseed](https://github.com/imarag/Body-Waves-Arrival-Selection/assets/97481016/2e2623e8-bad8-4683-9eee-f2e6b17054b5)

Apply a filter to remove the surrounding noise and facilitate the selection of the arrivals:

![PS_arr_apply_filter](https://github.com/imarag/Body-Waves-Arrival-Selection/assets/97481016/55fd996f-3250-4693-8314-64fd6b017896)

Then, select the arrivals of the P and the S waves:

![PS_arr_select_arrivals](https://github.com/imarag/Body-Waves-Arrival-Selection/assets/97481016/a511f67f-342e-4a22-a9f0-b929db642f00)

Finally, save the arrivals at a file:

![PS_arr_save_the_arrivals](https://github.com/imarag/Body-Waves-Arrival-Selection/assets/97481016/67129eb9-a45a-4291-829d-96be330f49dd)
