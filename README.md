# Fall-Detection-using-Accelerometer

Detecting a Fall using Wrist Worn Triaxial Accelerometer
Considering three main stages-- Freefall, Impact and Inactivity after a fall

1.Start of the fall: The phenomenon of weightlessness will always occur at the start of a fall. It will become more significant during free fall, and the vector sum of acceleration will tend toward 0 g; the duration of that condition will depend on the height of freefall. Even though weightlessness during an ordinary fall is not as significant as that during a freefall, the vector sum of acceleration will still be substantially less than 1 g (while it is generally greater than 1 g under normal conditions). 
2.mpact: After experiencing weightlessness, the human body will impact the ground or other objects; the acceleration curve shows this as a large shock.. Therefore, the second basis for determining a fall is the ACTIVITY interrupt right after the FREE_FALL interrupt.
3.Aftermath: Generally speaking, the human body,afterfalling and making an impact, can not rise immediately; rather it remains in a motionless position for a short period (or longer as a possible sign of unconsciousness). On the acceleration curve, this presents as an interval of a flat line. Therefore, the third basis for determining a fall situation is the INACTIVITY interrupt after the ACTIVITY interrupt.

Only possible if Accelerometer is not wrist worn!
Comparing before and after: After a fall, the individual’s body will be in a different orientation than before, so the static acceleration in three axes will be different from the initial status before the fall (Figure 4). Suppose that the fall detector is belt-wired on the individual’s body, to provide the entire history of acceleration, including the initial status. We can read the acceleration data in all three axes after the INACTIVITY interrupt and compare those sampling data with the initial status. In Figure 4, it is evident that the body fell on its side, since the static acceleration has changed from –1 g on the Y axis to +1 g on the Z-axis. So the fourth basis for determining a fall is if the difference between sampling data and initial status exceeds a certain threshold, for example, 0.7 g.


### Fall_Detection_abstract file
Three Thresholds considered--
Min magnitude in a window -- For FREE FALL Detection (<120/95 mm per sec sq.)
Maximum of Max min difference in a window (>2000 mm per sec sq.)
Avg of max min difference of 30 windows, with 5 samples per window equivalent to 3s (<200 mm per sec sq.) 


#### Test Data Link- https://drive.google.com/open?id=1JBGU5W2uq9rl8h7bJNt2lN4SjfZnFxmQ
