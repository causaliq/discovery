belief network "unknown"
node AccidentalViolations {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node CreateAFalseImpressionToDeceiveTheRegulators {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node DecisionErrors {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node DeparmentsAndInstitutionsAreNotComplete {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node HabitualViolations {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node IllegalCommand {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node InadequateEmergencyPlan {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node InsufficientCracdownOnIllegalActivities {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node InsufficientSupervisionOfWorkSafety {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node MentalStates {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node OrganizeProductionInViolationOfLawsAndRegulations {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node PerceptualErrors {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node PhysicalIntellectualDisability {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node SafetyEducationAndTraning {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node SafetySupervisionIsInadequate {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node SecurityManagementConfusion {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node SkillBasedErrors {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
node TechnicalEnvironment {
  type : discrete [ 2 ] = { "Non-occurence", "Occurence" };
}
probability ( AccidentalViolations | IllegalCommand, OrganizeProductionInViolationOfLawsAndRegulations ) {
  (0, 0) : 0.903, 0.097;
  (1, 0) : 0.905, 0.095;
  (0, 1) : 0.793, 0.207;
  (1, 1) : 0.789, 0.211;
}
probability ( CreateAFalseImpressionToDeceiveTheRegulators | SecurityManagementConfusion ) {
  (0) : 0.875, 0.125;
  (1) : 0.706, 0.294;
}
probability ( DecisionErrors | IllegalCommand, OrganizeProductionInViolationOfLawsAndRegulations, TechnicalEnvironment ) {
  (0, 0, 0) : 1.0, 0.0;
  (1, 0, 0) : 0.846, 0.154;
  (0, 1, 0) : 0.882, 0.118;
  (1, 1, 0) : 1.0, 0.0;
  (0, 0, 1) : 1.0, 0.0;
  (1, 0, 1) : 0.75, 0.25;
  (0, 1, 1) : 0.75, 0.25;
  (1, 1, 1) : 1.0, 0.0;
}
probability ( DeparmentsAndInstitutionsAreNotComplete | SafetySupervisionIsInadequate ) {
  (0) : 0.74, 0.26;
  (1) : 0.68, 0.32;
}
probability ( HabitualViolations | MentalStates, PhysicalIntellectualDisability ) {
  (0, 0) : 0.645, 0.355;
  (1, 0) : 0.333, 0.667;
  (0, 1) : 0.333, 0.667;
  (1, 1) : 0.0, 1.0;
}
probability ( IllegalCommand ) {
   0.6, 0.4;
}
probability ( InadequateEmergencyPlan ) {
   0.79, 0.21;
}
probability ( InsufficientCracdownOnIllegalActivities ) {
   0.78, 0.22;
}
probability ( InsufficientSupervisionOfWorkSafety ) {
   0.56, 0.44;
}
probability ( MentalStates | SafetyEducationAndTraning ) {
  (0) : 1.0, 0.0;
  (1) : 0.857, 0.143;
}
probability ( OrganizeProductionInViolationOfLawsAndRegulations | DeparmentsAndInstitutionsAreNotComplete, SecurityManagementConfusion ) {
  (0, 0) : 0.619, 0.381;
  (1, 0) : 0.545, 0.455;
  (0, 1) : 0.52, 0.48;
  (1, 1) : 0.389, 0.611;
}
probability ( PerceptualErrors | IllegalCommand ) {
  (0) : 0.917, 0.083;
  (1) : 0.85, 0.15;
}
probability ( PhysicalIntellectualDisability | InadequateEmergencyPlan, SafetyEducationAndTraning, SecurityManagementConfusion ) {
  (0, 0, 0) : 1.0, 0.0;
  (1, 0, 0) : 1.0, 0.0;
  (0, 1, 0) : 1.0, 0.0;
  (1, 1, 0) : 0.667, 0.333;
  (0, 0, 1) : 0.974, 0.026;
  (1, 0, 1) : 1.0, 0.0;
  (0, 1, 1) : 0.875, 0.125;
  (1, 1, 1) : 1.0, 0.0;
}
probability ( SafetyEducationAndTraning | SafetySupervisionIsInadequate ) {
  (0) : 0.78, 0.22;
  (1) : 0.66, 0.34;
}
probability ( SafetySupervisionIsInadequate ) {
   0.5, 0.5;
}
probability ( SecurityManagementConfusion | InsufficientCracdownOnIllegalActivities, SafetySupervisionIsInadequate ) {
  (0, 0) : 0.417, 0.583;
  (1, 0) : 0.0, 1.0;
  (0, 1) : 0.233, 0.767;
  (1, 1) : 0.25, 0.75;
}
probability ( SkillBasedErrors | CreateAFalseImpressionToDeceiveTheRegulators, IllegalCommand, TechnicalEnvironment ) {
  (0, 0, 0) : 0.969, 0.031;
  (1, 0, 0) : 1.0, 0.0;
  (0, 1, 0) : 0.957, 0.043;
  (1, 1, 0) : 0.75, 0.25;
  (0, 0, 1) : 0.9, 0.1;
  (1, 0, 1) : 0.833, 0.167;
  (0, 1, 1) : 0.7274549, 0.2725451;
  (1, 1, 1) : 0.5, 0.5;
}
probability ( TechnicalEnvironment | InsufficientSupervisionOfWorkSafety ) {
  (0) : 0.75, 0.25;
  (1) : 0.659, 0.341;
}
