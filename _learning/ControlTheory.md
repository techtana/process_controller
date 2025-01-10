# Control Theory
## Topics
* Time domain and frequency domain
* System and signal analysis
* PID controller
* MPC controller

__src__: http://www-control.eng.cam.ac.uk/gv/p6/index.html

## Looking through different lens
The most common way human makes sense of physical systems is by observing the behaviors over time. This is because the behavior pattern over time is generally useful. For example, we can observe the distance of the car over time to figure out if how close we are to destination and when to stop the car, or observe the motion of ocean wind over time to figure out when a sailboat can best sail out from shore. This can be called an observation based on "time-domain".

For some systems, we can observe additional patterns exists on the time-domain graphs. Ocean tide is a great example of a repeatable changes in water level as the moon rotates around the earth, pulling the water along with it. If we plot the water level over time, we can find an approximately-sinusoidal pattern i.e. water moves vertically, up and down, in a repeatable behavior. Looking at time-domain plot helps us determine the height of tide or time of highest tide in the data we collect historically. 

However, we may be more interested in how frequent the water level repeats the pattern or more accurately determind the more complex pattern which also include the location of the sun and tilt of the earth. We can analyze the data in terms of frequency and amplitudes. This way, we can see the oscillations caused by the moon are superposed by the effect of earth tilt and distance from the sun. Had we look at the time-domain plot, it would be difficult to discern this pattern and trend.

If we observe the middle point of a guitar string that is plucked, we can see that the string oscillates i.e. moves horizontally, back and forth, in a repeatable pattern. If we plot the location of the guitar string

### Linear time-invariant systems
Most real systems have non-linear input-output characteristics, but many systems operated within nominal parameters (not over-driven) have behavior close enough to linear that LTI system theory is an acceptable representation of their input-output behavior.

Transfer functions are commonly used in the analysis of systems such as single-input single-output filters in signal processing, communication theory, and control theory. The term is often used exclusively to refer to linear time-invariant (LTI) systems.

Impulse response represent the system in time domain and transfer function represent the system in frequency domain. Essentially both are same.

Think of the tide example again. We can convert the time-domain graphs into frequency-domain graph with a mathematical tool called "Forrier Transform". In the case of guitar string, to better approximate the pattern, we need to account for an exponential decay of amplitude which FT does not account for. Instead, we have Laplace transform.

### Stability analysis
link: https://www.youtube.com/watch?v=nzZ19jKm-jk&list=PLBlnK6fEyqRgyaWjvSyL5A3ozNcg8_ziw

Stability analysis is an analysis of whether the system can reach a steady state. Here, we care about the system over an infinite period of time, so whatever happens in transient is not of concerns. The minimum requirement before we can control a system is that, once an input is altered, the system must converge to steady state. 

There are four main scenarios when analyzing the state of a system over time: 
1. Stable system -- Over an infinite length of time, the system will approach some equilibrium state i.e. constant.
2. Unstable system -- Over an infinite length of time, the system continues to diverge i.e. continuously decreasing or increasing.
3. Conditionally stable system -- Within some boundary condition, the system will behaves as stable. System becomes stable if some parameter or input goes outside of the stable ranges.
4. Marginally stable system -- System neither converge or diverge, but continues to fluctuates within a stable range (think sine/cosine waves).

The most straightforward way to figure out the stability of the system is to plot out the function of system over infinite time $f(t \rightarrow \infty)$.  
For example: $f(t)=-1.25-2e^{-2t}u(t)+9e^{-4t}u(t) \Rightarrow f(t \rightarrow \infty)=-1.25$ meaning the system is stable.  
Whereas, $f(t)=-1.25-2e^{-2t}u(t)+9e^{4t}u(t) \Rightarrow f(t \rightarrow \infty)=+\infty$; the system is exponentially increasing.  
And, $f(t)=sin(5t) \Rightarrow f(t \rightarrow \infty)=sin(\infty)$; the system is marginally stable.



**Routh Hurwitz (RH) Criterion**




Bode Plots

Root Locus

Nyquist Stability Criterion

## Transfer Function

In control systems, "G" and "H" typically represent transfer functions within a feedback loop, where "G" refers to the "forward path" transfer function (the primary system being controlled) and "H" represents the "feedback path" transfer function, which measures the feedback signal sent back to the system to adjust its output; the product "G*H" is often called the "open-loop transfer function" of the system. [1, 2, 3]

Key points about G and H: [1, 2, 3]
G (forward path): This transfer function describes the behavior of the main system, like a motor or a plant, and represents how the input signal is transformed into the output signal without considering the feedback loop.
H (feedback path): This transfer function represents the sensor or measurement device that provides feedback information about the system's output, which is then compared to the desired input to calculate the error signal. [1, 2, 3]

How to use G and H: [2, 4]
Closed-loop transfer function: To calculate the overall behavior of a closed-loop system, the transfer function is typically expressed as "G/(1 + GH)" where "GH" is the open-loop transfer function. [2, 4]
Control design: Engineers often design controllers by manipulating the "H" transfer function to achieve desired system performance characteristics like stability and accuracy. [2, 4, 5]





# PID controller
...

## State Space Model
* Prior to running the process, we collect incoming data to determine Feed Forward recommendation. 
    > Given $Y = B \cdot U + G \cdot f + c$  
    Then, $\delta Y = B \cdot \delta U + G \cdot \delta f$  
    Feed-forward recommended inputs $\delta U = (\delta Y - G \cdot \delta f)/B$.

* After the process is commited, we collect data about the actual inputs used for the process.
    > We can calculate the updated state: $X_{k+1} = AX_k + BU_k + Fw_k$

* After the process is completed and product is measured, we retrieve the measured output.
    > $$Y_{k} = CX_k + Gf_k + v_k$$

### Equation 1: Process Dynamics
$$X_{k+1} = AX_k + BU_k + Fw_k$$
where, for example:  
$$
A = \begin{bmatrix}
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 \\
\end{bmatrix},
B = \begin{bmatrix}
    model_{11} & model_{12} & model_{13} & 0 & 0 & 0 \\
    model_{21} & model_{22} & model_{23} & 0 & 0 & 0 \\
    model_{31} & model_{32} & model_{33} & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix},
F = \begin{bmatrix}
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

Process dynamics equation describes the underlying dynamics ("state") of the process as a result of past state, past inputs, and other unknown interferences. __A__ matrix parameter defines how past states affect future state e.g. combination of zero matrix and identity matrix is commonly used in basic linear equations. __B__ matrix parameter defines how system inputs (e.g. time, temperature, loop counts) impact the process dynamics. Similarly, __C__ matrix parameter defines relationship between past state disturbance and future state. Zero matrix components in __A__, __B__ and __C__ represent the assumption that process inputs have no interactions with previous states. Identity matrix components in __A__ and __C__ represent the assumption that past process dynamics and disturbances proportionately impact future states.

<u>Note</u>: Consider __C__ matrix in equation 2, we will see that $Y = B*U + (A*\text{state component} + ...)$. This is the same form as linear regression of $Y=mX+C$. Therefore, __B__ matrix can be determined by the slope in regression analysis. Then, essentially, State Space Equation can be thought of as a tool to find process intercept which can change over time due to process drifts or interferences, known or unknown.  


### Equation 2: Process Output
$$Y_{k} = CX_k + Gf_k$$
where, for example:  
$$
C = \begin{bmatrix}
    1 & 0 & 0 & 1 & 0 & 0 \\
    0 & 1 & 0 & 0 & 1 & 0 \\
    0 & 0 & 1 & 0 & 0 & 1 \\
\end{bmatrix},

$$G = \begin{bmatrix}
    g_{a,11} & g_{a,12} & g_{a,13} & g_{b,11} & g_{b,12} & g_{b,13} & \dots \\
    g_{a,21} & g_{a,22} & g_{a,23} & g_{b,21} & g_{b,22} & g_{b,23} & \dots \\
    g_{a,31} & g_{a,32} & g_{a,33} & g_{b,31} & g_{b,32} & g_{b,33} & \dots \\
\end{bmatrix}
$$

Process output equation describes the true output as a result of the current process dynamics. Let's recall the expanded form for first element: $Y_{k,1} = CX_{k,1} + Gf_{k,1}$. __C__ parameter defines how states impact outputs. If we don't know the weightage of how states and system inputs impact output, __C__ can be a combination of 2 identity matrices. The ratio between the first 3 and last 3 columns (in this case, 1:1) represents assumption that the states and inputs have the same weights. If we continue out state space model above, we can recall that $k$ denotes the time sequence, and  
$$ X_{k,1} = (B_{1,1}U_{k-1,1} + B_{1,2}U_{k-1,2} + B_{1,3}U_{k-1,3}) + (A_{4,4}X_{k-1,4} + A_{5,5}X_{k-1,5} + A_{6,6}X_{k-1,6}) $$ 

__G__ defines the relationship between incoming disturbance and output. When we write out the first element of output equation, we get $Y_{k,1} = CX_{k,1} + Gf_{k,1}$. Since __C__ is an identity matrix, we get $Y_{k,1} = 1*X_{k,1} + Gf_{k,1}$. If we don't know the weightage of how states and Feed Forward disturbance impact output, we can set __G__ as 1 as well. However, sometimes an incoming variation of 10 nm may only cause the output to drift by smaller amount of 8 nm. In that case, we can set __G__ to be 0.8 to reflex the smaller weightage.  

<u>Note</u>: The number of columns in __C__ must be the same as the number of elements in states vector. The number of columns in __G__ can be as large as needed to account for multiple types of disturbances. For example, sources of incoming disturbances may include (1) incoming thickness, (2) design id, (3) number of wafers in furnace, (4) tool sensor values. In this case, we would have a matrix of 3 by 4 or more; "3" is the number of outputs, and "4 or more" is the number of terms in FF equation. 

__Example:__
Let's say from analysis, we found a model below that describe the process quite well.  

$\Delta\text{Thickness}_{top} = \Delta\text{Incoming Thickness}_{top}    + \Delta\text{FF Design ID} + \Delta\text{FF Load Size}_{1}$   
$\Delta\text{Thickness}_{center} = \Delta\text{Incoming Thickness}_{center}    + \Delta\text{FF Design ID} + \Delta\text{FF Load Size}_{1} + \Delta\text{FF Load Size}_{2}$   
$\Delta\text{Thickness}_{bottom} = 0.8*\Delta\text{Incoming Thickness}_{bottom}  + \Delta\text{FF Design ID} + \Delta\text{FF Load Size}_{2}$ 

Then, we can format the equation above to: 

$
Y_k = \begin{bmatrix} Thickness Top \\ Thickness Center \\ Thickness Bottom \\\end{bmatrix} = G \cdot f_k + (\dots)= 
\begin{bmatrix}
    1 & 0 & 0   & 1 & 1 & 0 \\
    0 & 1 & 0   & 1 & 1 & 1 \\
    0 & 0 & 0.8 & 1 & 0 & 1 \\
\end{bmatrix} \cdot
\begin{bmatrix}
    \text{FF dist Incoming Thickness}_{1} \\
    \text{FF dist Incoming Thickness}_{2} \\
    \text{FF dist Incoming Thickness}_{3} \\
    \text{FF dist Design ID} \\
    \text{FF dist Load Size}_{1} \\
    \text{FF dist Load Size}_{2} \\
\end{bmatrix}+ (\dots)
$

### Equation 3: Measurement Equation
$$Y_{k} = CX_k + Gf_k + v_k$$

Measurement equation adds noise term to Process output equation above. This signifies that measurements may not be the same as true output due to imprecisions or errors in the measurement.
