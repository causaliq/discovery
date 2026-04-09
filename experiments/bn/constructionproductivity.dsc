belief network "unknown"
node Accidents {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node AdverseWeather {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Age {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Attitude {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node EngineerQualification {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Experience {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node HealthStatus {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node MaterialPresence {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node OwnerFinance {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node PlanningAndMethod {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Productivity {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Sex {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node SkilledWorkers {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node TaskComplexity {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node TechnologyLevel {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node WorkingFrequency {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node WorkingTools {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Workmanship {
  type : discrete [ 2 ] = { "Yes", "No" };
}
probability ( Accidents | HealthStatus ) {
  (0) : 0.617, 0.383;
  (1) : 0.587, 0.413;
}
probability ( AdverseWeather ) {
   0.47, 0.53;
}
probability ( Age ) {
   0.73, 0.27;
}
probability ( Attitude ) {
   0.9, 0.1;
}
probability ( EngineerQualification ) {
   0.67, 0.33;
}
probability ( Experience | Age ) {
  (0) : 0.703, 0.297;
  (1) : 0.463, 0.537;
}
probability ( HealthStatus | AdverseWeather ) {
  (0) : 0.44, 0.56;
  (1) : 0.647, 0.353;
}
probability ( MaterialPresence | OwnerFinance ) {
  (0) : 0.887, 0.113;
  (1) : 0.627, 0.373;
}
probability ( OwnerFinance ) {
   0.9, 0.1;
}
probability ( PlanningAndMethod | EngineerQualification ) {
  (0) : 0.627, 0.373;
  (1) : 0.73, 0.27;
}
probability ( Productivity | Accidents, TaskComplexity, TechnologyLevel, WorkingFrequency ) {
  (0, 0, 0, 0) : 0.627, 0.373;
  (1, 0, 0, 0) : 0.527, 0.473;
  (0, 1, 0, 0) : 0.527, 0.473;
  (1, 1, 0, 0) : 0.227, 0.773;
  (0, 0, 1, 0) : 0.627, 0.373;
  (1, 0, 1, 0) : 0.127, 0.873;
  (0, 1, 1, 0) : 0.327, 0.673;
  (1, 1, 1, 0) : 0.727, 0.273;
  (0, 0, 0, 1) : 0.327, 0.673;
  (1, 0, 0, 1) : 0.427, 0.573;
  (0, 1, 0, 1) : 0.827, 0.173;
  (1, 1, 0, 1) : 0.427, 0.573;
  (0, 0, 1, 1) : 0.327, 0.673;
  (1, 0, 1, 1) : 0.727, 0.273;
  (0, 1, 1, 1) : 0.727, 0.273;
  (1, 1, 1, 1) : 0.327, 0.673;
}
probability ( Sex ) {
   0.53, 0.47;
}
probability ( SkilledWorkers | OwnerFinance ) {
  (0) : 0.76, 0.24;
  (1) : 0.83, 0.17;
}
probability ( TaskComplexity | Workmanship ) {
  (0) : 0.703, 0.297;
  (1) : 0.403, 0.597;
}
probability ( TechnologyLevel | PlanningAndMethod ) {
  (0) : 0.73, 0.27;
  (1) : 0.7, 0.3;
}
probability ( WorkingFrequency | Attitude, MaterialPresence, Sex, SkilledWorkers, WorkingTools ) {
  (0, 0, 0, 0, 0) : 0.827, 0.173;
  (1, 0, 0, 0, 0) : 0.627, 0.373;
  (0, 1, 0, 0, 0) : 0.4264264, 0.5735736;
  (1, 1, 0, 0, 0) : 0.13, 0.87;
  (0, 0, 1, 0, 0) : 0.727, 0.273;
  (1, 0, 1, 0, 0) : 0.727, 0.273;
  (0, 1, 1, 0, 0) : 0.627, 0.373;
  (1, 1, 1, 0, 0) : 0.527, 0.473;
  (0, 0, 0, 1, 0) : 0.527, 0.473;
  (1, 0, 0, 1, 0) : 0.427, 0.573;
  (0, 1, 0, 1, 0) : 0.127, 0.873;
  (1, 1, 0, 1, 0) : 0.327, 0.673;
  (0, 0, 1, 1, 0) : 0.327, 0.673;
  (1, 0, 1, 1, 0) : 0.127, 0.873;
  (0, 1, 1, 1, 0) : 0.627, 0.373;
  (1, 1, 1, 1, 0) : 0.727, 0.273;
  (0, 0, 0, 0, 1) : 0.627, 0.373;
  (1, 0, 0, 0, 1) : 0.527, 0.473;
  (0, 1, 0, 0, 1) : 0.727, 0.273;
  (1, 1, 0, 0, 1) : 0.527, 0.473;
  (0, 0, 1, 0, 1) : 0.727, 0.273;
  (1, 0, 1, 0, 1) : 0.13, 0.87;
  (0, 1, 1, 0, 1) : 0.327, 0.673;
  (1, 1, 1, 0, 1) : 0.627, 0.373;
  (0, 0, 0, 1, 1) : 0.427, 0.573;
  (1, 0, 0, 1, 1) : 0.727, 0.273;
  (0, 1, 0, 1, 1) : 0.827, 0.173;
  (1, 1, 0, 1, 1) : 0.227, 0.773;
  (0, 0, 1, 1, 1) : 0.227, 0.773;
  (1, 0, 1, 1, 1) : 0.527, 0.473;
  (0, 1, 1, 1, 1) : 0.627, 0.373;
  (1, 1, 1, 1, 1) : 0.527, 0.473;
}
probability ( WorkingTools | OwnerFinance ) {
  (0) : 0.787, 0.213;
  (1) : 0.66, 0.34;
}
probability ( Workmanship | Experience ) {
  (0) : 0.8, 0.2;
  (1) : 0.6, 0.4;
}
