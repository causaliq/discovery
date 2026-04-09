belief network "unknown"
node BenthicFishForaging {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Disturbance {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Ecosystem {
  type : discrete [ 3 ] = { "Standing floating", "Standing submerged", "Flowing submerged" };
}
node EcosystemServices {
  type : discrete [ 9 ] = { "Flooding", "Birds", "Nutrient retention", "Angling", "Swimming", "Boating", "Hydropower", "Irrigation", "Invasive species" };
}
node EpiphyticInvertebrates {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Flow {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Light {
  type : discrete [ 2 ] = { "Low", "High" };
}
node NutrientLoading {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Phytoplankton {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node PiscivorousFish {
  type : discrete [ 2 ] = { "Absent", "Present" };
}
node PiscivorousFishPredation {
  type : discrete [ 2 ] = { "Low", "High" };
}
node PlanktivorousFish {
  type : discrete [ 2 ] = { "Low", "High" };
}
node PlantRemoval {
  type : discrete [ 3 ] = { "None", "Partial", "Full" };
}
node Resources {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
node Zooplankton {
  type : discrete [ 3 ] = { "Low", "Medium", "High" };
}
probability ( BenthicFishForaging | EpiphyticInvertebrates ) {
  (0) : 0.0, 0.0, 1.0;
  (1) : 0.0, 1.0, 0.0;
  (2) : 1.0, 0.0, 0.0;
}
probability ( Disturbance | Flow, Zooplankton ) {
  (0, 0) : 1.0, 0.0, 0.0;
  (1, 0) : 0.0, 1.0, 0.0;
  (2, 0) : 0.0, 0.0, 1.0;
  (0, 1) : 0.0, 1.0, 0.0;
  (1, 1) : 0.0, 0.5, 0.5;
  (2, 1) : 0.3333333, 0.3333333, 0.3333333;
  (0, 2) : 0.00, 0.75, 0.25;
  (1, 2) : 0.3333333, 0.3333333, 0.3333333;
  (2, 2) : 0.3333333, 0.3333333, 0.3333333;
}
probability ( Ecosystem ) {
   0.3333333, 0.3333333, 0.3333333;
}
probability ( EcosystemServices ) {
   0.1, 0.0, 0.1, 0.4, 0.1, 0.0, 0.2, 0.1, 0.0;
}
probability ( EpiphyticInvertebrates | Ecosystem, PlantRemoval ) {
  (0, 0) : 0.75, 0.25, 0.00;
  (1, 0) : 0.00, 0.25, 0.75;
  (2, 0) : 0.00, 0.25, 0.75;
  (0, 1) : 0.5, 0.5, 0.0;
  (1, 1) : 0.00, 0.25, 0.75;
  (2, 1) : 0.00, 0.25, 0.75;
  (0, 2) : 0.25, 0.50, 0.25;
  (1, 2) : 1.0, 0.0, 0.0;
  (2, 2) : 1.0, 0.0, 0.0;
}
probability ( Flow | Ecosystem, PlantRemoval ) {
  (0, 0) : 1.0, 0.0, 0.0;
  (1, 0) : 1.0, 0.0, 0.0;
  (2, 0) : 0.75, 0.25, 0.00;
  (0, 1) : 1.0, 0.0, 0.0;
  (1, 1) : 1.0, 0.0, 0.0;
  (2, 1) : 0.0, 0.5, 0.5;
  (0, 2) : 1.0, 0.0, 0.0;
  (1, 2) : 1.0, 0.0, 0.0;
  (2, 2) : 0.0, 0.0, 1.0;
}
probability ( Light | Ecosystem, PlantRemoval ) {
  (0, 0) : 1.0, 0.0;
  (1, 0) : 0.5, 0.5;
  (2, 0) : 0.5, 0.5;
  (0, 1) : 0.5, 0.5;
  (1, 1) : 0.25, 0.75;
  (2, 1) : 0.25, 0.75;
  (0, 2) : 0.0, 1.0;
  (1, 2) : 0.0, 1.0;
  (2, 2) : 0.0, 1.0;
}
probability ( NutrientLoading ) {
   0.525, 0.275, 0.200;
}
probability ( Phytoplankton | Disturbance, Resources ) {
  (0, 0) : 0.5, 0.5, 0.0;
  (1, 0) : 0.75, 0.25, 0.00;
  (2, 0) : 1.0, 0.0, 0.0;
  (0, 1) : 0.0, 0.5, 0.5;
  (1, 1) : 0.0, 1.0, 0.0;
  (2, 1) : 0.5, 0.5, 0.0;
  (0, 2) : 0.0, 0.0, 1.0;
  (1, 2) : 0.0, 0.5, 0.5;
  (2, 2) : 0.0, 1.0, 0.0;
}
probability ( PiscivorousFish ) {
   0.5, 0.5;
}
probability ( PiscivorousFishPredation | PiscivorousFish, PlantRemoval ) {
  (0, 0) : 1.0, 0.0;
  (1, 0) : 1.0, 0.0;
  (0, 1) : 1.0, 0.0;
  (1, 1) : 0.5, 0.5;
  (0, 2) : 1.0, 0.0;
  (1, 2) : 0.0, 1.0;
}
probability ( PlanktivorousFish | PiscivorousFishPredation ) {
  (0) : 0.0, 1.0;
  (1) : 1.0, 0.0;
}
probability ( PlantRemoval | EcosystemServices ) {
  (0) : 0.00, 0.25, 0.75;
  (1) : 1.0, 0.0, 0.0;
  (2) : 0.75, 0.25, 0.00;
  (3) : 0.0, 1.0, 0.0;
  (4) : 0.00, 0.25, 0.75;
  (5) : 0.0, 0.0, 1.0;
  (6) : 0.00, 0.25, 0.75;
  (7) : 0.0, 0.5, 0.5;
  (8) : 0.0, 0.0, 1.0;
}
probability ( Resources | BenthicFishForaging, Light, NutrientLoading ) {
  (0, 0, 0) : 1.0, 0.0, 0.0;
  (1, 0, 0) : 0.9, 0.1, 0.0;
  (2, 0, 0) : 0.8, 0.2, 0.0;
  (0, 1, 0) : 0.75, 0.25, 0.00;
  (1, 1, 0) : 0.5, 0.5, 0.0;
  (2, 1, 0) : 0.25, 0.75, 0.00;
  (0, 0, 1) : 0.75, 0.25, 0.00;
  (1, 0, 1) : 0.7, 0.3, 0.0;
  (2, 0, 1) : 0.65, 0.35, 0.00;
  (0, 1, 1) : 0.00, 0.75, 0.25;
  (1, 1, 1) : 0.00, 0.65, 0.35;
  (2, 1, 1) : 0.00, 0.55, 0.45;
  (0, 0, 2) : 0.5, 0.5, 0.0;
  (1, 0, 2) : 0.5, 0.5, 0.0;
  (2, 0, 2) : 0.5, 0.5, 0.0;
  (0, 1, 2) : 0.0, 0.0, 1.0;
  (1, 1, 2) : 0.0, 0.0, 1.0;
  (2, 1, 2) : 0.0, 0.0, 1.0;
}
probability ( Zooplankton | Flow, PlanktivorousFish ) {
  (0, 0) : 0.0, 0.0, 1.0;
  (1, 0) : 0.0, 1.0, 0.0;
  (2, 0) : 1.0, 0.0, 0.0;
  (0, 1) : 0.5, 0.5, 0.0;
  (1, 1) : 0.75, 0.25, 0.00;
  (2, 1) : 1.0, 0.0, 0.0;
}
