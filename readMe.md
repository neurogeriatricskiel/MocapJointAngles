# Mocap Joint Angles

**Author:** Karolina Saegner

Extract hip and knee angles from motion capture data uisng the reference position as a calibration method. This method uses technical marker frames that are linked to the reference position, which is recorded during a static trial. Alternatively, a reference position can be obtained from dynamic trial data if such position is identified and thata from that instance is extracted. The reference position needs to be aligned with the global coordinate frame as these represent the body axes in the anatomical position.


Local coordinate systems are computed from both static and dynamic data for pelvis, both thigh marker clusters and both shank marker clusters. The origins of the local coordinate systems are the mid-points computed for each marker cluster. Next, a transformation matrix for the pelvis, thigh and shank markers is calculated. For the static trials, the average of the marker positions is used; for the dynamic trials the marker positions are multiplied by the transformation matrix for each time stamp. To obtain the reference position, the transformation matrix of each time stamp from the dynamic data is multiplied by the inverse transformation matrix of the corresponding static data. The left and right Euler angles for the hip rotations around the three axes (vertical, antero-posterior and medio-lateral) are determined by multiplying the inverse pelvic transformation matrix with the left and right hip transformation matrices; similarly for the knee rotations the inverse left and right thigh transformation matrices are multiplied with the corresponding shank transformation matrices. As the last step, Euler angles are converted to degrees using the following rotation sequence:

α=arcsin(R[2,1]) * 180/π

β=arctan2(-R[2,0],R[2,2]) * 180/π

γ=arctan2(-R[0,1],R[1,1]) * 180/π
