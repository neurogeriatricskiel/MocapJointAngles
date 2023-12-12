import matplotlib.pyplot as plt
import numpy as np

def plot_angles(nDynam, Knee_Angles_left, Knee_Angles_right, Hip_Angles_left, Hip_Angles_right, ppID, task):
    time = np.linspace(0, nDynam/200 ,num=nDynam)
    fig, axes = plt.subplots(3, 2, sharex=True)
    fig.set_figwidth(15.0)
    fig.set_figheight(10.0)
    
    # Left column

    # Plot flexion/extension angles
    axes[0, 0].plot(time,Knee_Angles_left[0,:])
    axes[0, 0].plot(time,Hip_Angles_left[0,:])
    axes[0, 0].set_title('FLX/EXT LEFT')
    axes[0, 0].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[0, 0].set_ylabel('Angle(°)')
    axes[0, 0].set_xlabel('Time [s]')
    axes[0, 0].set_ylim([-80, 80])
    axes[0, 0].grid(True)

    # Plot abduction/adduction angles
    axes[1, 0].plot(time,Knee_Angles_left[1,:])
    axes[1, 0].plot(time,Hip_Angles_left[1,:])
    axes[1, 0].set_title('AB/AD LEFT')
    axes[1, 0].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[1, 0].set_ylabel('Angle(°)')
    axes[1, 0].set_xlabel('Time [s]')
    axes[1, 0].set_ylim([-80, 80])
    axes[1, 0].grid(True)
    
    # Plot internal/external rotation angles
    axes[2, 0].plot(time,Knee_Angles_left[2,:])
    axes[2, 0].plot(time,Hip_Angles_left[2,:])
    axes[2, 0].set_title('INT/EXT LEFT')
    axes[2, 0].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[2, 0].set_ylabel('Angle(°)')
    axes[2, 0].set_xlabel('Time [s]')
    axes[2, 0].set_ylim([-80, 80])
    axes[2, 0].grid(True) 

    # Right column

    # Plot flexion/extension angles
    axes[0, 1].plot(time,Knee_Angles_right[0,:])
    axes[0, 1].plot(time,Hip_Angles_right[0,:])
    axes[0, 1].set_title('FLX/EXT RIGHT')
    axes[0, 1].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[0, 1].set_ylabel('Angle(°)')
    axes[0, 1].set_xlabel('Time [s]')
    axes[0, 1].set_ylim([-80, 80])
    axes[0, 1].grid(True)

    # Plot abduction/adduction angles
    axes[1, 1].plot(time,Knee_Angles_right[1,:])
    axes[1, 1].plot(time,Hip_Angles_right[1,:])
    axes[1, 1].set_title('AB/AD RIGHT')
    axes[1, 1].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[1, 1].set_ylabel('Angle(°)')
    axes[1, 1].set_xlabel('Time [s]')
    axes[1, 1].set_ylim([-80, 80])
    axes[1, 1].grid(True)

    # Plot internal/external rotation angles
    axes[2, 1].plot(time,Knee_Angles_right[2,:])
    axes[2, 1].plot(time,Hip_Angles_right[2,:])
    axes[2, 1].set_title('INT/EXT RIGHT')
    axes[2, 1].legend(['knee', 'hip'],loc=1, prop={'size': 9})
    axes[2, 1].set_ylabel('Angle(°)')
    axes[2, 1].set_xlabel('Time [s]')
    axes[2, 1].set_ylim([-80, 80])
    axes[2, 1].grid(True) 


    plt.suptitle(f'{ppID} {task}')
    plt.show()