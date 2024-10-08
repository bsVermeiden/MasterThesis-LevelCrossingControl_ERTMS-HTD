### DESCRIPTION

Master Thesis about the formal verification of a level crossing controller using mCRL2. This level crossing controller will be used under ERTMS HTD where trains are detected using Train Vacancy Proving (TVP) and using Train Report (TR) based announcement. TVP is the current standard using Trackside Train Detection (TTD) equipement. TR is the new activation method where the system receives speed and location updates from the train to determine the correct activation moment of the crossing.

Using this model we verified the safety of the level crossing controller.

### USAGE

Track and Train specifications can be changed at the first lines of the model. If no train or track should be present, set the specification for that track to `[]` or the specification for that train to `No_Train`.
To choose between a train that uses Train Reports (TR) or Train Vacancy Proving (TVP) on track `X`, change the line `Type_x` to either `TR` or `TVP`.
You can choose the initial speed of each train. The speed determines the number of locations the train moves per move action and, thus, the number of meters the train moves per second.
The location of the level crossing can be set for each track and is set for the local track in terms of its Track Section.
The trains' acceleration and deceleration rates can be set. If 0 is chosen for both variables, the model behaves as if the trains have a constant speed.
The MAX_HALTED variable states the maximum time that any train can stand still and the number of times it can stand still.

LPS and LTS generation and verification are done using the usual method. See https://www.mcrl2.org/web/user_manual/tools/tools.html for an overview.
Verification properties are found in the `properties` directory.

Automated verification can be done using the `run.py` Python script.

### CHANGE LOG

The change log can be found here: [Change log](CHANGELOG.md)

### TODO

- Add nondeterminism to sending and receiving of train reports.
  - The CSS might not receive correct train reports and needs to be able to deal with this
  - I don't think this will result in any interesting observations, only if zero reports come in but then it will always fail or trains will never make progress
- Possibly change positions from Pos to Real to allow for non-integer positions
- Investigate whether the middle section occupancy can be the only deactivation condition
