# ERP code
# CLMU emulation for HR urban climate mapping
## Workflow

### CLMU simulations
- Latin hypercube sampling for 100,000 samples using U-surf data.
- Plus ERA5 data, using `pyclmuapp` tool to favour CLMU simulations.
- Together with CLMU simulations using data extracted within the Greater Manchester area and use the result as 'true values' for models comparison.
  
### 0_Trainingdata_Preparation
- Extract three target urban cliamte variables (TSA, RH2M and HIA) from original CLMU output files.
- Calculat the max and mean values of three target urban cliamte variables and treat them to be the six target variables for model traning.

### 1_Model_Training
- Use sampled 100,000 data and corresponding results from CLMU as traning data for model traning.
- Model one: FLAML-automated tree based models.
- Model two: FLAML-tuned MLP model.

### 2_Model_Comparison
- Choose the better performed model based on several model performance parameters.

### 3_Mapping_&_Model_Explanation
- Map the six target variables using the final choosed model.
- Explaine feature importance and model performance on the six target variables.

### 4_Case_Studies_Analysis
- Analysis of two case studies based on model explanation.
