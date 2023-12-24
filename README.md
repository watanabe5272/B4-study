# B4-study
These Python programs are designed to perform data analysis studies on my solar wind velocity model, the "DCHB model".
They require the following observation data as input
  - solar wind velocity observed by the IPS radio telescope
  - photospheric magnetic field observed by the telescopes (KPVT/SPM, SOLIS/VSM, GONG)
  - coronal magnetic field calculated by the PFSS model
  - extreme ultraviolet images of coronal holes observed by the satellites (SDO/EIT, SOHO/HMI)
However, we do not have those observation data in this repository.

My original implementation is as follows
  - A program that executes the DCHB model to calculates solar wind velocity from the 3D structure of the coronal magnetic field by the PFSS model and outputs a color map.
  - A program that calculates statistical parameters taking into account the area expansion effect associated with a 360 x 180 orthogonal grid of latitude and longitude is pasted on a spherical surface (the same as the area distortion at high latitudes in the Mercator map).
  - A program that reduces the resolution of the data by performing convolution with a kernel that can keep the same shape on the sphere.
  - A program that determines the DCHB model parameters that have the highest correlation coefficient with the IPS solar wind speed through a full search.
  - A program that produces a scatter plot of the solar wind speed versus distance from the CHB from the results of statistical parameter calculations.
