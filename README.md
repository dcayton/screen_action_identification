# Screen Action Identification: #
### A methodology to take tracking data and play-by-play data to identify play types ###

The goal of this analysis is to identify pick-and-roll and pick-and-pop actions from NBA tracking data combined with play-by-play data. The data is taken from the following repository below, which was also engineered by myself. However, that data is piped from two other sources, additionally linked below.

- https://huggingface.co/datasets/dcayton/nba_tracking_data_15_16 (source of data)
- https://github.com/linouk23/NBA-Player-Movements/tree/master (tracking data source)
- https://github.com/sumitrodatta/nba-alt-awards/tree/main (PBP data source)

The analysis can be performed by following along the notebook `PNR_and_PNP_identification.ipynb`.

These techniques were developed by building off of the following papers.

- Using Hex Maps to Classify & Cluster Dribble Hand-off
Variants in the NBA (Stephanos et al.)
- Automatically Recognizing On-Ball Screens (McQueen, Weins, Guttag)
- NBA ON-BALL SCREENS: AUTOMATIC IDENTIFICATION AND ANALYSIS OF BASKETBALL PLAYS (Andrew Yu)

The goal of this project is to ultimate create a pipeline, using raw coordinate and play-by-play data, from which actions can be identified and then watched by coaches and staff. This can aid scouting and development.

For example, if a coach wanted to watch how a player performed every time they were the ball-handler in the pick-and-roll, the events for the last $\textit{n}$ games could be processed and potential PNR events could be output. Then the coach can use game film to go back and watch them without having to watch the whole game looking out for these situations.

Similarly, if a scout wanted to understand how another team's center operated, they could run the pipeline for all events where the player is in the game and a screener and understand the proportion of pick and rolls to pick and pops.

While the outputs may not be entirely correct, as we achieved $\textbf{84}$% accuracy, there is little penalty to incorrectly identifying some events, and much reward to correctly identifying the majority. This is because a subsample of correct events can still inform behavior while little extra may be gleaned from the misclassified ones.
