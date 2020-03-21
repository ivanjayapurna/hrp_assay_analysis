# hrp_assay_analysis

Colorimetric analysis of HRP assays from video files to get kinetic data.

Input: Video of assay cropped to post-shaking (i.e. plate fixed in place)
Outputs: Plots of hue, saturation & value changes over time in each of the 4 well plates under analysis AND CSV file of (grayscale) values over time.

Use Instructions: Run program, pick 4 points at center of each well [ignore discolouring in sample image], view results in output folders [make sure input and output folders are created and in the same directory as python script]

TODO:
- Analysis pipeline i.e. automated generation of log-plots, best-fit lines and slope calculations.
- Make plots look nicer (publication quality)
