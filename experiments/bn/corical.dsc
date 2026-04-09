belief network "unknown"
node Age {
  type : discrete [ 8 ] = { "0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+" };
}
node AZVaccineDoses {
  type : discrete [ 3 ] = { "None", "One", "Two" };
}
node BackgroundCSVTOver6Weeks {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node BackgroundPVTOver6Weeks {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Covid19AssociatedCSVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node Covid19AssociatedPVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromBackgroundCSVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromBackgroundPVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromCovid19 {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromCovid19AssociatedCSVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromCovid19AssociatedPVT {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node DieFromVaccineAssociatedTTS {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node IntensityOfCommunityTransmission {
  type : discrete [ 10 ] = { "None", "ATAGI Low", "ATAGI Med", "ATAGI High", "One Percent", "Two Percent", "NSW 200 Daily", "NSW 1000 Daily", "VIC 1000 Daily", "QLD 1000 Daily" };
}
node RiskOfSymptomaticInfection {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node RiskOfSymptomaticInfectionUnderCurrentTransmissionAndVaccinationStatus {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node SARSCoV2Variant {
  type : discrete [ 2 ] = { "Alpha Wild", "Delta" };
}
node Sex {
  type : discrete [ 2 ] = { "Male", "Female" };
}
node VaccineAssociatedTTS {
  type : discrete [ 2 ] = { "Yes", "No" };
}
node VaccineEffectivenessAgainstDeathIfInfected {
  type : discrete [ 2 ] = { "Effective", "Not Effective" };
}
node VaccineEffectivenessAgainstSymptomaticInfection {
  type : discrete [ 2 ] = { "Effective", "Not Effective" };
}
probability ( Age ) {
   0.1233831, 0.1233831, 0.1402985, 0.1452736, 0.1273632, 0.1213930, 0.1044776, 0.1144279;
}
probability ( AZVaccineDoses ) {
   0.30, 0.35, 0.35;
}
probability ( BackgroundCSVTOver6Weeks | Age ) {
  (0) : 0.03, 0.97;
  (1) : 0.03, 0.97;
  (2) : 0.04, 0.96;
  (3) : 0.04, 0.96;
  (4) : 0.04, 0.96;
  (5) : 0.05, 0.95;
  (6) : 0.05, 0.95;
  (7) : 0.05, 0.95;
}
probability ( BackgroundPVTOver6Weeks | Age ) {
  (0) : 0.01, 0.99;
  (1) : 0.01, 0.99;
  (2) : 0.02, 0.98;
  (3) : 0.025, 0.975;
  (4) : 0.035, 0.965;
  (5) : 0.05, 0.95;
  (6) : 0.07, 0.93;
  (7) : 0.08, 0.92;
}
probability ( Covid19AssociatedCSVT | RiskOfSymptomaticInfectionUnderCurrentTransmissionAndVaccinationStatus, Sex ) {
  (0, 0) : 0.20, 0.80;
  (1, 0) : 0.0, 1.0;
  (0, 1) : 0.25, 0.75;
  (1, 1) : 0.0, 1.0;
}
probability ( Covid19AssociatedPVT | RiskOfSymptomaticInfectionUnderCurrentTransmissionAndVaccinationStatus, Sex ) {
  (0, 0) : 0.30, 0.70;
  (1, 0) : 0.0, 1.0;
  (0, 1) : 0.25, 0.75;
  (1, 1) : 0.0, 1.0;
}
probability ( DieFromBackgroundCSVT | BackgroundCSVTOver6Weeks ) {
  (0) : 0.15, 0.85;
  (1) : 0.0, 1.0;
}
probability ( DieFromBackgroundPVT | BackgroundPVTOver6Weeks ) {
  (0) : 0.27, 0.73;
  (1) : 0.0, 1.0;
}
probability ( DieFromCovid19 | Age, RiskOfSymptomaticInfectionUnderCurrentTransmissionAndVaccinationStatus, Sex, VaccineEffectivenessAgainstDeathIfInfected ) {
  (0, 0, 0, 0) : 0.0, 1.0;
  (1, 0, 0, 0) : 0.0, 1.0;
  (2, 0, 0, 0) : 0.0, 1.0;
  (3, 0, 0, 0) : 0.0, 1.0;
  (4, 0, 0, 0) : 0.0, 1.0;
  (5, 0, 0, 0) : 0.0, 1.0;
  (6, 0, 0, 0) : 0.0, 1.0;
  (7, 0, 0, 0) : 0.0, 1.0;
  (0, 1, 0, 0) : 0.0, 1.0;
  (1, 1, 0, 0) : 0.0, 1.0;
  (2, 1, 0, 0) : 0.0, 1.0;
  (3, 1, 0, 0) : 0.0, 1.0;
  (4, 1, 0, 0) : 0.0, 1.0;
  (5, 1, 0, 0) : 0.0, 1.0;
  (6, 1, 0, 0) : 0.0, 1.0;
  (7, 1, 0, 0) : 0.0, 1.0;
  (0, 0, 1, 0) : 0.0, 1.0;
  (1, 0, 1, 0) : 0.0, 1.0;
  (2, 0, 1, 0) : 0.0, 1.0;
  (3, 0, 1, 0) : 0.0, 1.0;
  (4, 0, 1, 0) : 0.0, 1.0;
  (5, 0, 1, 0) : 0.0, 1.0;
  (6, 0, 1, 0) : 0.0, 1.0;
  (7, 0, 1, 0) : 0.0, 1.0;
  (0, 1, 1, 0) : 0.0, 1.0;
  (1, 1, 1, 0) : 0.0, 1.0;
  (2, 1, 1, 0) : 0.0, 1.0;
  (3, 1, 1, 0) : 0.0, 1.0;
  (4, 1, 1, 0) : 0.0, 1.0;
  (5, 1, 1, 0) : 0.0, 1.0;
  (6, 1, 1, 0) : 0.0, 1.0;
  (7, 1, 1, 0) : 0.0, 1.0;
  (0, 0, 0, 1) : 0.05, 0.95;
  (1, 0, 0, 1) : 0.07, 0.93;
  (2, 0, 0, 1) : 0.07, 0.93;
  (3, 0, 0, 1) : 0.10, 0.90;
  (4, 0, 0, 1) : 0.10, 0.90;
  (5, 0, 0, 1) : 0.15, 0.85;
  (6, 0, 0, 1) : 0.25, 0.75;
  (7, 0, 0, 1) : 0.45, 0.55;
  (0, 1, 0, 1) : 0.0, 1.0;
  (1, 1, 0, 1) : 0.0, 1.0;
  (2, 1, 0, 1) : 0.0, 1.0;
  (3, 1, 0, 1) : 0.0, 1.0;
  (4, 1, 0, 1) : 0.0, 1.0;
  (5, 1, 0, 1) : 0.0, 1.0;
  (6, 1, 0, 1) : 0.0, 1.0;
  (7, 1, 0, 1) : 0.0, 1.0;
  (0, 0, 1, 1) : 0.04, 0.96;
  (1, 0, 1, 1) : 0.05, 0.95;
  (2, 0, 1, 1) : 0.05, 0.95;
  (3, 0, 1, 1) : 0.08, 0.92;
  (4, 0, 1, 1) : 0.08, 0.92;
  (5, 0, 1, 1) : 0.12, 0.88;
  (6, 0, 1, 1) : 0.20, 0.80;
  (7, 0, 1, 1) : 0.40, 0.60;
  (0, 1, 1, 1) : 0.0, 1.0;
  (1, 1, 1, 1) : 0.0, 1.0;
  (2, 1, 1, 1) : 0.0, 1.0;
  (3, 1, 1, 1) : 0.0, 1.0;
  (4, 1, 1, 1) : 0.0, 1.0;
  (5, 1, 1, 1) : 0.0, 1.0;
  (6, 1, 1, 1) : 0.0, 1.0;
  (7, 1, 1, 1) : 0.0, 1.0;
}
probability ( DieFromCovid19AssociatedCSVT | Covid19AssociatedCSVT ) {
  (0) : 0.40, 0.60;
  (1) : 0.0, 1.0;
}
probability ( DieFromCovid19AssociatedPVT | Covid19AssociatedPVT ) {
  (0) : 0.40, 0.60;
  (1) : 0.0, 1.0;
}
probability ( DieFromVaccineAssociatedTTS | VaccineAssociatedTTS ) {
  (0) : 0.15, 0.85;
  (1) : 0.0, 1.0;
}
probability ( IntensityOfCommunityTransmission ) {
   0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1;
}
probability ( RiskOfSymptomaticInfection | Age, SARSCoV2Variant ) {
  (0, 0) : 0.12, 0.88;
  (1, 0) : 0.20, 0.80;
  (2, 0) : 0.35, 0.65;
  (3, 0) : 0.28, 0.72;
  (4, 0) : 0.25, 0.75;
  (5, 0) : 0.25, 0.75;
  (6, 0) : 0.22, 0.78;
  (7, 0) : 0.28, 0.72;
  (0, 1) : 0.25, 0.75;
  (1, 1) : 0.35, 0.65;
  (2, 1) : 0.35, 0.65;
  (3, 1) : 0.28, 0.72;
  (4, 1) : 0.25, 0.75;
  (5, 1) : 0.25, 0.75;
  (6, 1) : 0.18, 0.82;
  (7, 1) : 0.15, 0.85;
}
probability ( RiskOfSymptomaticInfectionUnderCurrentTransmissionAndVaccinationStatus | IntensityOfCommunityTransmission, RiskOfSymptomaticInfection, VaccineEffectivenessAgainstSymptomaticInfection ) {
  (0, 0, 0) : 0.0, 1.0;
  (1, 0, 0) : 0.0, 1.0;
  (2, 0, 0) : 0.0, 1.0;
  (3, 0, 0) : 0.0, 1.0;
  (4, 0, 0) : 0.0, 1.0;
  (5, 0, 0) : 0.0, 1.0;
  (6, 0, 0) : 0.0, 1.0;
  (7, 0, 0) : 0.0, 1.0;
  (8, 0, 0) : 0.0, 1.0;
  (9, 0, 0) : 0.0, 1.0;
  (0, 1, 0) : 0.0, 1.0;
  (1, 1, 0) : 0.0, 1.0;
  (2, 1, 0) : 0.0, 1.0;
  (3, 1, 0) : 0.0, 1.0;
  (4, 1, 0) : 0.0, 1.0;
  (5, 1, 0) : 0.0, 1.0;
  (6, 1, 0) : 0.0, 1.0;
  (7, 1, 0) : 0.0, 1.0;
  (8, 1, 0) : 0.0, 1.0;
  (9, 1, 0) : 0.0, 1.0;
  (0, 0, 1) : 0.0, 1.0;
  (1, 0, 1) : 0.05, 0.95;
  (2, 0, 1) : 0.10, 0.90;
  (3, 0, 1) : 0.5759, 0.4241;
  (4, 0, 1) : 0.15, 0.85;
  (5, 0, 1) : 0.25, 0.75;
  (6, 0, 1) : 0.10, 0.90;
  (7, 0, 1) : 0.22276, 0.77724;
  (8, 0, 1) : 0.27289, 0.72711;
  (9, 0, 1) : 0.35067, 0.64933;
  (0, 1, 1) : 0.0, 1.0;
  (1, 1, 1) : 0.0, 1.0;
  (2, 1, 1) : 0.0, 1.0;
  (3, 1, 1) : 0.0, 1.0;
  (4, 1, 1) : 0.0, 1.0;
  (5, 1, 1) : 0.0, 1.0;
  (6, 1, 1) : 0.0, 1.0;
  (7, 1, 1) : 0.0, 1.0;
  (8, 1, 1) : 0.0, 1.0;
  (9, 1, 1) : 0.0, 1.0;
}
probability ( SARSCoV2Variant ) {
   0.05, 0.95;
}
probability ( Sex ) {
   0.5, 0.5;
}
probability ( VaccineAssociatedTTS | Age, AZVaccineDoses ) {
  (0, 0) : 0.0, 1.0;
  (1, 0) : 0.0, 1.0;
  (2, 0) : 0.0, 1.0;
  (3, 0) : 0.0, 1.0;
  (4, 0) : 0.0, 1.0;
  (5, 0) : 0.0, 1.0;
  (6, 0) : 0.0, 1.0;
  (7, 0) : 0.0, 1.0;
  (0, 1) : 0.04, 0.96;
  (1, 1) : 0.04, 0.96;
  (2, 1) : 0.04, 0.96;
  (3, 1) : 0.04, 0.96;
  (4, 1) : 0.04, 0.96;
  (5, 1) : 0.045, 0.955;
  (6, 1) : 0.035, 0.965;
  (7, 1) : 0.04, 0.96;
  (0, 2) : 0.015, 0.985;
  (1, 2) : 0.015, 0.985;
  (2, 2) : 0.015, 0.985;
  (3, 2) : 0.015, 0.985;
  (4, 2) : 0.015, 0.985;
  (5, 2) : 0.015, 0.985;
  (6, 2) : 0.015, 0.985;
  (7, 2) : 0.015, 0.985;
}
probability ( VaccineEffectivenessAgainstDeathIfInfected | AZVaccineDoses, SARSCoV2Variant ) {
  (0, 0) : 0.0, 1.0;
  (1, 0) : 0.8, 0.2;
  (2, 0) : 0.95, 0.05;
  (0, 1) : 0.0, 1.0;
  (1, 1) : 0.69, 0.31;
  (2, 1) : 0.9, 0.1;
}
probability ( VaccineEffectivenessAgainstSymptomaticInfection | AZVaccineDoses, SARSCoV2Variant ) {
  (0, 0) : 0.0, 1.0;
  (1, 0) : 0.6, 0.4;
  (2, 0) : 0.8, 0.2;
  (0, 1) : 0.0, 1.0;
  (1, 1) : 0.3333333, 0.6666667;
  (2, 1) : 0.61, 0.39;
}
