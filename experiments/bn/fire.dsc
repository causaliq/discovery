belief network "unknown"
node AudioFireCues {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node EmotionalStability {
  type : discrete [ 2 ] = { "Stable", "Unstable" };
}
node Escape {
  type : discrete [ 2 ] = { "True", "False" };
}
node FireCues {
  type : discrete [ 2 ] = { "Consistent", "Not consistent" };
}
node FireKnowledge {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node LayoutFamiliarity {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node PerceivedHazard {
  type : discrete [ 2 ] = { "Risky", "Not risky" };
}
node PsychologicalIncapacitation {
  type : discrete [ 2 ] = { "Mild", "Severe" };
}
node Stress {
  type : discrete [ 2 ] = { "Low", "High" };
}
node TimePressure {
  type : discrete [ 2 ] = { "Low", "High" };
}
node VisualFireCues {
  type : discrete [ 2 ] = { "Yes", "No" };
}
probability ( AudioFireCues ) {
   0.5, 0.5;
}
probability ( EmotionalStability | FireCues, FireKnowledge, LayoutFamiliarity, TimePressure ) {
  (0, 0, 0, 0) : 0.86, 0.14;
  (1, 0, 0, 0) : 0.75, 0.25;
  (0, 1, 0, 0) : 0.75, 0.25;
  (1, 1, 0, 0) : 0.59, 0.41;
  (0, 0, 1, 0) : 0.75, 0.25;
  (1, 0, 1, 0) : 0.59, 0.41;
  (0, 1, 1, 0) : 0.63, 0.37;
  (1, 1, 1, 0) : 0.41, 0.59;
  (0, 0, 0, 1) : 0.63, 0.37;
  (1, 0, 0, 1) : 0.59, 0.41;
  (0, 1, 0, 1) : 0.59, 0.41;
  (1, 1, 0, 1) : 0.37, 0.63;
  (0, 0, 1, 1) : 0.59, 0.41;
  (1, 0, 1, 1) : 0.41, 0.59;
  (0, 1, 1, 1) : 0.41, 0.59;
  (1, 1, 1, 1) : 0.25, 0.75;
}
probability ( Escape | PerceivedHazard, PsychologicalIncapacitation ) {
  (0, 0) : 0.63, 0.37;
  (1, 0) : 0.63, 0.37;
  (0, 1) : 0.29, 0.71;
  (1, 1) : 0.41, 0.59;
}
probability ( FireCues | AudioFireCues, FireKnowledge, VisualFireCues ) {
  (0, 0, 0) : 0.86, 0.14;
  (1, 0, 0) : 0.59, 0.41;
  (0, 1, 0) : 0.41, 0.59;
  (1, 1, 0) : 0.25, 0.75;
  (0, 0, 1) : 0.71, 0.29;
  (1, 0, 1) : 0.41, 0.59;
  (0, 1, 1) : 0.25, 0.75;
  (1, 1, 1) : 0.04, 0.96;
}
probability ( FireKnowledge ) {
   0.37, 0.63;
}
probability ( LayoutFamiliarity ) {
   0.59, 0.41;
}
probability ( PerceivedHazard | FireKnowledge, Stress ) {
  (0, 0) : 0.25, 0.75;
  (1, 0) : 0.14, 0.86;
  (0, 1) : 0.59, 0.41;
  (1, 1) : 0.63, 0.37;
}
probability ( PsychologicalIncapacitation | Stress ) {
  (0) : 0.86, 0.14;
  (1) : 0.37, 0.63;
}
probability ( Stress | EmotionalStability, TimePressure ) {
  (0, 0) : 0.86, 0.14;
  (1, 0) : 0.86, 0.14;
  (0, 1) : 0.25, 0.75;
  (1, 1) : 0.25, 0.75;
}
probability ( TimePressure ) {
   0.63, 0.37;
}
probability ( VisualFireCues ) {
   0.5, 0.5;
}
