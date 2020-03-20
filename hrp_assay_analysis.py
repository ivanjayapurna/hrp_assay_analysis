import numpy as np
import cv2
import matplotlib.pyplot as plt


#####################
##### FUNCTIONS #####
#####################

def get_points(img):
    print('Please select centers of 4 wells for analysis')
    plt.imshow(img)
    p1, p2, p3, p4 = plt.ginput(4)
    plt.close()
    return [p1, p2, p3, p4]


def get_colour(img, pts):
	# get pixel value for each RGB channel for each of the 4 well plate points
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h_vals = []
	s_vals = []
	v_vals = []

	for pt in pts:
		h_vals.append(img[np.int(pt[1]), np.int(pt[0]), 0])
		s_vals.append(img[np.int(pt[1]), np.int(pt[0]), 1])
		v_vals.append(img[np.int(pt[1]), np.int(pt[0]), 2])
	
	return h_vals, s_vals, v_vals


def vid2research(input_media, some_param=1):
	# Create Video Capture object and read from input file
	# if camera input, pass in 0 instead of file name
	cap = cv2.VideoCapture(input_media)
	if (cap.isOpened() == False):
		print("Error opening video stream or file")

	# Default resolutions of the frame are obtained. The default resolutions are system dependent.
	frame_width, frame_height = cap.get(3), cap.get(4)

	# get total number of frames to pre-allocate matrix!
	n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


	ret, frame = cap.read()
	points = get_points(frame)

	h_vals_mat = []
	s_vals_mat = []
	v_vals_mat = []
	# Read until video is completed
	while (cap.isOpened()):
		# capture frame-by-frame
		ret, frame = cap.read()

		if ret == True:

			# get colour values and append to colour values matrix
			h_vals, s_vals, v_vals = get_colour(frame, points)
			h_vals_mat.append(h_vals)
			s_vals_mat.append(s_vals)
			v_vals_mat.append(v_vals)

			# display the resulting frame
			#cv2.imshow('frame', frame)

			# press Q on keyboard to exit
			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		else:
			break

	# when done, release video capture and write objects & close all frames
	cap.release()
	#cv2.destroyAllWindows()

	return h_vals_mat, s_vals_mat, v_vals_mat



##################
##### SCRIPT #####
##################

# MAKE SURE TO CROP STARTING FROM AFTER THE SHAKING IS DONE
# specify video name
media_path = 'videos'
media_name = '25mgmL_THF_varying_pH'

# get RGB values for each of the 4 wells for every frame
h_mat, s_mat, v_mat = vid2research(media_path + '/' + media_name + '.mov')
h_mat = np.array(h_mat)
s_mat = np.array(s_mat)
v_mat = np.array(v_mat)

# plotting
fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(7, 7))

for i in range(3):
	for j in range(4):
		axs[i,j].set_xlabel("Time")
		axs[i,j].set_ylabel("Central Pixel Value")

for j in range(4):
	axs[0, j].set_title("H, Well " + str(j + 1))
	axs[1, j].set_title("S, Well " + str(j + 1))
	axs[2, j].set_title("V, Well " + str(j + 1))

	axs[0, j].plot(np.arange(len(h_mat[:,j])), h_mat[:,j])
	axs[1, j].plot(np.arange(len(h_mat[:,j])), s_mat[:,j])
	axs[2, j].plot(np.arange(len(h_mat[:,j])), v_mat[:,j])

fig.tight_layout()
output_path = 'outputs'
plt.savefig(output_path + '/' + media_name)

