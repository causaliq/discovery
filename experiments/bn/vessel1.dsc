belief network "unknown"
node CarryingLoadAboveTransportLimits {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DesignDefect {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node HuntingEquipmentOverload {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node LossOfBuoyancy {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node LossOfStability {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node LossOfWaterTightness {
  type : discrete [ 2 ] = { "Present", "Absent" };
}
node Overload {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node PlannedMaintenance {
  type : discrete [ 2 ] = { "Completed", "Uncompleted" };
}
node Sinking {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node UnstableLoading {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node UsedHuntingEquipment {
  type : discrete [ 2 ] = { "Proper", "Improper" };
}
node VesselAge {
  type : discrete [ 2 ] = { "Old", "New" };
}
node VesselPipelines {
  type : discrete [ 2 ] = { "Corroded", "Normal" };
}
node VesselStructure {
  type : discrete [ 2 ] = { "Worn", "Normal" };
}
node WaterIntake {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node WeatherAndSeaConditions {
  type : discrete [ 2 ] = { "Bad", "Good" };
}
probability ( CarryingLoadAboveTransportLimits | Overload ) {
  (0) : 1.0, 0.0;
  (1) : 0.0, 1.0;
}
probability ( DesignDefect ) {
   0.04, 0.96;
}
probability ( HuntingEquipmentOverload | UsedHuntingEquipment ) {
  (0) : 0.13, 0.87;
  (1) : 1.0, 0.0;
}
probability ( LossOfBuoyancy | WaterIntake ) {
  (0) : 1.0, 0.0;
  (1) : 0.04, 0.96;
}
probability ( LossOfStability | DesignDefect, HuntingEquipmentOverload, UnstableLoading ) {
  (0, 0, 0) : 1.0, 0.0;
  (1, 0, 0) : 1.0, 0.0;
  (0, 1, 0) : 0.5, 0.5;
  (1, 1, 0) : 0.4, 0.6;
  (0, 0, 1) : 0.75, 0.25;
  (1, 0, 1) : 0.5, 0.5;
  (0, 1, 1) : 0.1, 0.9;
  (1, 1, 1) : 0.0, 1.0;
}
probability ( LossOfWaterTightness | VesselAge ) {
  (0) : 0.09, 0.91;
  (1) : 0.0, 1.0;
}
probability ( Overload ) {
   0.16, 0.84;
}
probability ( PlannedMaintenance ) {
   0.9, 0.1;
}
probability ( Sinking | CarryingLoadAboveTransportLimits, LossOfBuoyancy, LossOfStability, WeatherAndSeaConditions ) {
  (0, 0, 0, 0) : 1.0, 0.0;
  (1, 0, 0, 0) : 1.0, 0.0;
  (0, 1, 0, 0) : 1.0, 0.0;
  (1, 1, 0, 0) : 1.0, 0.0;
  (0, 0, 1, 0) : 1.0, 0.0;
  (1, 0, 1, 0) : 1.0, 0.0;
  (0, 1, 1, 0) : 1.0, 0.0;
  (1, 1, 1, 0) : 0.33, 0.67;
  (0, 0, 0, 1) : 1.0, 0.0;
  (1, 0, 0, 1) : 0.63, 0.37;
  (0, 1, 0, 1) : 0.38, 0.62;
  (1, 1, 0, 1) : 0.23, 0.77;
  (0, 0, 1, 1) : 0.5, 0.5;
  (1, 0, 1, 1) : 0.35, 0.65;
  (0, 1, 1, 1) : 0.1, 0.9;
  (1, 1, 1, 1) : 0.0, 1.0;
}
probability ( UnstableLoading ) {
   0.13, 0.87;
}
probability ( UsedHuntingEquipment ) {
   0.93, 0.07;
}
probability ( VesselAge ) {
   0.74, 0.26;
}
probability ( VesselPipelines | PlannedMaintenance, VesselAge ) {
  (0, 0) : 0.9, 0.1;
  (1, 0) : 0.96, 0.04;
  (0, 1) : 0.0, 1.0;
  (1, 1) : 0.08, 0.92;
}
probability ( VesselStructure | VesselAge ) {
  (0) : 0.72, 0.28;
  (1) : 0.375, 0.625;
}
probability ( WaterIntake | LossOfWaterTightness, VesselPipelines, VesselStructure ) {
  (0, 0, 0) : 1.0, 0.0;
  (1, 0, 0) : 0.74, 0.26;
  (0, 1, 0) : 0.94, 0.06;
  (1, 1, 0) : 0.6, 0.4;
  (0, 0, 1) : 0.43, 0.57;
  (1, 0, 1) : 0.1, 0.9;
  (0, 1, 1) : 0.3, 0.7;
  (1, 1, 1) : 0.0, 1.0;
}
probability ( WeatherAndSeaConditions ) {
   0.33, 0.67;
}
