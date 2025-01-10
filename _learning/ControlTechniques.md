# Process Control for Semiconductor Manufacturing


## Feedback and Feed Forward

In most process control situation, we assume that the process is linear time invariant (LTI). If we just let the process run, we will see the output of the process hovering around some mean value with some process noise. If we change the input to the process, the output will change approximately linearly. In semiconductor fabs, we commonly use model-predictive control method (MPC) e.g. State Space Model to find optimal tool settings. The main goal of feedback is to bring the process output to target by adjusting the baseline inputs e.g. temperature, processing time, plasma voltage, gas flow, etc. During Feedback, we first update the "state" using Kalman filter (with parameter $Q$ and $R$) or EWMA (with parameter $\lambda$). With the state known, we then solve for:
$$U = M^{-1} (Y - State)$$
> where $U$ is a system input vector and $Y$ is the output target.

If we know prior to the process starts that there is an incoming or systemic disturbance, we can adjust the process accordingly BEFORE process starts. This is called "Feed Forward". Before we committed materials to the process, we assume that without any incoming disturbances, the current baseline inputs will perform right on target. If we have an equation to describe how incoming variations (e.g. incoming metrology, load size, design type, tool variations) will impact the process outcome (i.e. post-process metrology), we can simply solve for: 
$$Y=MU+c \Rightarrow \Delta U = -M^{-1} * \Delta FF$$
> where $U$ is a system input vector and $FF$ is a disturbance vector (same unit as output).

"Vector" was explicitly stated here because there can be one or many inputs and outputs in these equations. SISO (single-in, single-out) and MIMO (multiple-in, multiple-out) scenarios can be solved with State Space Model. 

In semiconductor processing, we also typically consider 2 levels of control granularity: 
* __Wafer-level__ : Rarely can tuning knobs control more finely than wafer mean. Therefore, this is the finest level we can typically control the process.
* __Lot-level__ : As measurement can be cost-prohibitive, we often do not have wafer-level data for FF. However, measuring 2 wafers per lot can give us lot-level information that is good enough to reduce majority of variations. If we have data for all wafers cheaply (by virtual metrology, for example), then wafer-level control is possible for some wafer-level processing tools. Nevertheless, batch processing tools often still do not have any knobs that will allow fine tuning of individual wafers within the chamber.    

## Data quality
Raw data from factory are often dirty. They may be incomplete, incorrectly measured, incorrectly processed, noisy, or lack of direct insights. Before we use these data, they will have to be cleaned or processed to ensure data quality and completeness. 
1. Data Correctness / Goodness of Fit
     * Raw points outliers (when multiple measurements makes up a data point)
       * Remove raw data point that has low data quality e.g. large confidence interval, low goodness of fit
       * Remove aggregated data if there is high variation of raw points e.g. stddev > 200 nm
       * Use aggregation statistics that is less impacted by outliers e.g. median instead of mean 
       * Remove raw data point that may cause high variance e.g. manual selection rules (e.g. data within 5cm radius of wafer center), outlier rules (Tukey's method or Grubbs' test) 
     * Time-trend outliers
       * Kalman Filter, which is already applied over state calculation
       * EWMA (time-trend) over a given rolling window
       * SPC-based limits (3 sigma of mean/median/ewma)
       * Tukey IQR outlier threshold
     * Other metrics for data science solutions
       * Typically, DS metrics include things like MAE, RMSE or R2. These are great metrics to compare performance of multiple models typically on the same dataset. However, when making decisions whether the model is good enough for business use, these metrics do not directly translate to business needs.
         * Feature Completeness -- Missing features during prediction are imputed with mean of that feature at training population (or of the past N wafers). However, if the feature are deemed important to the model, missing feature of feature value outside of the training dataset can degrade trust in the prediction. 
           * `Feature Completeness = sum(feature importance * binary_ispresent * binary_inIQRrange)`
         * Forecasted Error Interval / Prediction Interval -- In the absence of ground truth, traditional metrics suck as MAE and R2 is considered lagging. One method to estimate the errors of unpaired predictions (i.e. prediction without ground truth) is to use a forecast model.
           * __Step 1__: Fit ML model errors over the past N points/days to Theta forecast model
           * __Step 2__: Generate prediction interval for ML model errors (Upper and Lower Error Intervals), M values ahead 
           * __Step 3__: Calculate "Prediction Intervals" : Upper PI = Prediction + Upper Error Interval, Lower PI = Prediction + Lower Error Interval
               * **NOTE** :: It is possible that the Prediction value lies outside of [LPI, UPI] range. This happens when the prediction errors are not random and contains a consistent bias. Optionally, we can remove the data point from consideration if we require normality. However, personally, I see this the same as adding intercept to the prediction, similar to how states work in R2R.
           * __Step 4__: Calculate "Delta from target" : Upper Delta = UPI - Target, Lower Delta = LPI - Target
           * __Step 5__: Calculate "Confidence of prediction" (C_PI) = abs(UD+LD)/(abs(UD) + abs(LD))
               * **NOTE** :: C_PI indicates the proportion of prediction interval that lies beyond the target by at least the amount of the interval on the minority side. Then, if the prediction interval is centered around the target, then C_PI will equal zero, and the data point will have zero impact to EWMA.
           * __Step 6__: Calculate modified R2R EWMA State = R2R Lambda * Manual Coefficient * C_PI 
         * Normality test (on errors) -- e.g. Anderson–Darling test, Jarque–Bera test, Pearson's chi-squared test, Shapiro–Wilk test
         * Autocorrelation test (on errors) -- e.g. Durbin-Watson test, Ljung–Box test
         * Lot at Risk -- Assuming prediction errors are normal and non-autocorrelated, R2 can be considered as uncertainty of the prediction. Then, we can calculate lot at risk: 
           * $\text{\%Risk Reduced} = \frac{{\text{LAR}_\text{metro}-\text{LAR}_\text{metro+CM}}}{{\text{LAR}_\text{metro}}}$; where
             * LAR = Lot at Risk (below)
             * $\text{LAR}_\text{metro+CM}$ indicates that Virtual Metrology is used in conjunction with physical metrology.
           * $\text{LAR} = \frac{\text{ARL}}{\text{\%Sampling}*\text{Wf}^{\text{power}}}$; where
             * ARL = Average Run Length (below) -- The higher the R2, the lower the run length.
             * %sampling = Percent sampling rate -- The higher the sampling, the lower the risk.
             * wf = number of wafers sampled in a lot
             * power = wafer power correlaton (0-1)
           * $\text{ARL} = \sum_{i=1}^{\infty} {(i*a(1-a)^{i-1})} = \frac{1}{a}$; where
             * $a = \text{CDF[Detection]} - \text{CDF[Detection - Process Shift}*\sqrt{R^2}]$
             * Detection = 1 $\sigma$ (suggested by statistician)
             * Process Shift = 1.6 $\sigma$ (suggested by statistician)
             * CDF = Cumulative Density Function
         * Mean shift (MS) and Sigma ratio (SR)
           * These metrics compare the level and spread of prediction with the phyiscal data.
           * The metric thresholds are currently set by SME's "eyeball test" e.g. MS=0.8 and SR=1.8 
2. Data Completeness
     * Filtering
       * Requiring minimum number of valid datapoints, otherwise invalidate the wafer or lot.
     * Imputation
       * Mean filled for missing wafers in lot
       * EWMA (time-trend) for missing wafers in lot
       * Smart sampling (site-level regression based on location/image/pattern)
       * Virtual metrology (wafer-level regression based on lot/wafer/run data)
         * Using multiple data sources such as FD, IOT, Sigma, ET, WIS, lot attributes, or multiple steps to infer about te process.

## Control Techniques
* Grouped process tuning / Golden process tuning / RPA Replication
  * Problem: Qual runs for every process are redundant and noisy, need a way to control multiple processes that uses same recipe shell.
  * Goal: To linearly scale RPA from Golden process to child processes (if assumption holds). 
  * ROI: To reduce number of qual runs which means increasing tool availability and reduce material cost.
  * Background: There are multiple processes that use the same recipe shell but different targets. Each process will have separate quals to locally ensure the process works as expected. Commonly, R2R models will be independently derived via DOE. However, within the same tool, when process A/B/C quals detect negative drift, this should also indicate that the tool drifted as a whole. Currently, instead of running quals on multiple processes, PO setup a golden qual to run for all chambers then linearly scale recommendations to other processes. This reduces individual process quals. 
  * Assumption: All processes using the same recipe shell regardless of targets is linear. Since the thinner films would need less amount of adjustment than thicker films and the effect of variations over process time is less, thicker films are recommended as golden as long as the processes in the group remain linear. 
* "Pooled process"
  * Pooled process = same input, diff output
  * Linked process = diff input, diff output
* Grouped model tuning
  * Problem: Process models drifts over time, but tuning models individually require Test Wafers and Tool Time.
  * Goal: To regularly adjust calculate R2R model using data from multiple processes that use the same recipe shell.  
  * ROI: To reduce number of DOE per recipe shell
* Auto R2R modeling
  * Goal: To come up with R2R models without relying on DOE, using historical data (when tuning knobs variations are high enough). 
  * ROI: To reduce number of DOE for new R2R candidates
* Grouped state tuning
  * Problem: Not enough quals for the same process per DID 
  * Goal: To regularly adjust calculate R2R model using data from multiple processes that use the same recipe shell.  
  * ROI: To reduce number of DOE per DID and improve controls
  * Background: High mix low volume (HMLV) situation is when we have a high number of products running the same process. Because each product can result in different output even while subjected to the same process (e.g. For diffusion, each DID have different surface area), the states and models can be different for the same process and tool. However, with low volume, it is difficult to control each process individually with small amount of data. In semiconductor processing, we can assume that the additive or subtractive process will impact the state of all processes in the same direction. This assumption lets us take advantage of high mix of product using the same process. The calculation is similar to Group model tuning.
* Qual + Prod control (similar to HMLV??)
  * Problem: Qual are least frequent than Prod, but can better capture state of the process that can be more reliable and applied to multiple products at the same time.
  * Note: need to avoid race condition i.e. qual adjustment is back-to-back with prod adjustment. This can result in too much / conflicting adjustment. Generally, we trust qual data more, therefore, the BKM is to ignore prod adjustment 

## Handling periodic or systemic disturbances
* Preventive Maintenance Handling
  * RPA should be calculated differently for first run (by model or tracking all past post-PM), all horizon and state reset
  * Weighted average ensemble for post-Preventive-Maintenance setting
      * src: https://machinelearningmastery.com/weighted-average-ensemble-for-deep-learning-neural-networks/

## Control Parameter Optimization
* Mathematical optimization
  * R2R simulation
  * Parameter optimization (Q, R, Lambda)
* VPDOE (virtual process DOE - digital twin) 

## Infrastructure and system health
* Setup error detection (automation to detect human errors) 
  * R2R RPG Defense line
    - control status
    - function check
    - auto notice
    - auto compare
  * New process setup integration test (sample messages)
* R2R Metrics
  * Coverage
  * Error 
  * Harris Index (control performance)
  * Cpk
  * Other effectiveness metrics

## Material and tool handling
Aside from classical control theory, other tools can be helpful in improving process outcome.

* Auto material disposition
  * simple rules based on metrology that previously require manual requests to rework. We can now set up for automatic rules.
    * Equipment target hold
    * RA target hold
    * CPE (correction per exposure) sub-recipe type
    * LIS (AMAT Photo overlay improvement tool) Global sub-recipe type
    * LIS Refinement sub-recipe type
  * DROID (data-driven rework optimization with integrated disposition)
    * auto calculate setting when reworking wafer (the setting cannot be the same as baseline process)
* Dynamic Wafer Sampling
  * To ensure coverage for all photo tracks
* Dynamic recipe selection
  * Basically an if-else statement based on some material or run attributes

## Business Process and Workflow
* R2R Central UI (for both customer and engineers)
  - customer request
  - engineer setting (view, create, update)
  - knowledge managementment
  - setting transfer (since we don't all have aligned controller: (a) list all functionalities, (b) list critical setting in each functionalities that need transfer)

