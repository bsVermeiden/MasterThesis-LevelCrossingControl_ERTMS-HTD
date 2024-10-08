### CHANGE LOG ###
12/03/2024: The first version with working CSS_TVP and CSS_TR
- Works fully modularly 
- On this, we have verified the property "If train on LX then barriers closed."

18/03/2024: Global Time
- Added global time by syncing all timers
- Added time that LX is active to lx_status. 
- We can verify the property "If train on LX then lx_active for at least ANNOUNCEMENT_TIME".
  This does not always verify correctly, especially for TR trains, but this has to do with how the CSS_TR is implemented.

19/03/2024: Updated Train Movement
 - All trains move once per tick to VSS location + speed.
 - Trains can emit all positions between the current and next positions.

21/03/2024: All trains reach the end of their track
 - Added mcf that verifies this.
 - Archived this by letting the Train send a decrease_trains action when at the end of its track.

22/03/2024: Combined the CSS_TVP and CSS_TR into one model
 - Done by adding train type selector and changing the action names of move actions.

28/03/2024: Updated CSS_TVP to make sure the time before crossing is ANNOUNCEMENT_TIME.
 - Done by letting the model create the announcement zone
 - Announcement zone consists of one or more track sections
 - Added check that verifies if the track is long enough to allow for the announcement zone
 - From Thales section 2.3.2

12/04/2024: Added formula that verifies deactivation of LX 
 - Done by adding an all_trains process. This process keeps track of all train locations
 - We use those locations to verify if all trains are outside active locations
 - If that is the case, the action "all_trains_outside_active_zone" is possible
 - Changed Train_pos from list to struct. Instead of a list with 2 elements, made a struct with front_w and rear_w 

15/04/2024: Added Activation Timer
 - Used for train reports that are received too early
 - If set, activate LX for that track when its timer reaches zero

17/04/2024: Removed `train_p` action and synced all `move` actions
 - Added `Ghost_Train` process that creates `move` actions for non-existing trains
 - The update of the timers is also added in sync of `move` actions
 - Changed CSS_TVP to not use `move` anymore; now uses `current_position`
 - TVP trains now only send TS of front and rear wheels instead of Pos of front and rear wheels
 - Updated deactivate mcf. The lx should be deactivated in the same second after the action `all_trains_outside_active_zone` is received 
 
19/04/2024: Changed next_pos_speed & Added realistic branch
 - The next_pos_speed function now uses a non-recursive function, speeds up generation
 - The branch `Realistic-Values` has realistic values for train speed and track lengths

24/04/2024: Added Variable Speed
 - Updated calculation of time_to_lx to include the possibility of maximum acceleration
 - Train reports are now fully in line with CSS specification

30/04/2024: Activation time is calculated using CSS-506
 - Activation time is determined by approach time, configured announcement time and time that LX is active
 - This leads to a situation where the LX is not closed for long enough while a train is on the LX

07/05/2024: Activation delay
 - Added activation delay functionality
 - Added middle section occupancy deactivation
 - Activation delay required rewrite of currently active, this now includes which activation type is used

08/05/2024: Train standstill
 - Added the ability for trains to stand still
 - Trains can maximum stand still for a given time, and a maximum number of times

21/05/2024: Departure detection
 - Fully working departure detection
 - This includes train speed down when no MA given and fully functional standstill