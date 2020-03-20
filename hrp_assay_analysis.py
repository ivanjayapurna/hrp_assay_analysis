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
	r_vals = []
	g_vals = []
	b_vals = []

	for pt in pts:
		r_vals.append(img[np.int(pt[1]), np.int(pt[0]), 0])
		g_vals.append(img[np.int(pt[1]), np.int(pt[0]), 1])
		b_vals.append(img[np.int(pt[1]), np.int(pt[0]), 2])
	
	return r_vals, g_vals, b_vals


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

	r_vals_mat = []
	g_vals_mat = []
	b_vals_mat = []
	# Read until video is completed
	while (cap.isOpened()):
		# capture frame-by-frame
		ret, frame = cap.read()

		if ret == True:

			# get colour values and append to colour values matrix
			r_vals, g_vals, b_vals = get_colour(frame, points)
			r_vals_mat.append(r_vals)
			g_vals_mat.append(g_vals)
			b_vals_mat.append(b_vals)

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

	return r_vals_mat, g_vals_mat, b_vals_mat



##################
##### SCRIPT #####
##################

# MAKE SURE TO CROP STARTING FROM AFTER THE SHAKING IS DONE
# specify video name
media_path = 'videos'
media_name = '25mgmL_THF_varying_pH'

# get RGB values for each of the 4 wells for every frame
r_mat, g_mat, b_mat = vid2research(media_path + '/' + media_name + '.mov')
r_mat = np.array(r_mat)
g_mat = np.array(g_mat)
b_mat = np.array(b_mat)

# plotting
fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(7, 7))

for i in range(3):
	for j in range(4):
		axs[i,j].set_xlabel("Time")
		axs[i,j].set_ylabel("Pixel Value")

for j in range(4):
	axs[0, j].set_title("R, Well " + str(j + 1))
	axs[1, j].set_title("G, Well " + str(j + 1))
	axs[2, j].set_title("B, Well " + str(j + 1))

	axs[0, j].plot(r_mat[:,j], np.arange(len(r_mat[:,j])))
	axs[1, j].plot(g_mat[:,j], np.arange(len(r_mat[:,j])))
	axs[2, j].plot(b_mat[:,j], np.arange(len(r_mat[:,j])))

fig.tight_layout()
output_path = 'outputs'
plt.savefig(outputs + '/' + media_name)

