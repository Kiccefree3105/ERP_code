# Import the external modules
import numpy as np
from pyclmuapp import usp_clmu
import pickle
import os
from multiprocessing import Pool, cpu_count
import argparse

def get_params():
    parser = argparse.ArgumentParser(description='Run CLMU')
    parser.add_argument('--nproc', type=int, 
                        default=None, help='Number of processes to use')
    parser.add_argument('--container_type', type=str,
                        default='docker', help='Container type to use')
    parser.add_argument('--input_file', type=str,
                        default='lhs_exps_dict.pkl', help='Input file')
    return parser.parse_args()

def initialize_params():
    try:
        import __main__  # check if running as script
        if hasattr(__main__, '__file__'):  # running as script
            args = get_params()
            return args.nproc, args.container_type, args.input_file
    except ImportError:
        pass
    return None, 'docker', 'lhs_exps_dict.pkl'

## <--- Define the run_clmu function --->
## This function is used to run the CLMU model and return the dataset
def run_clmu(
             usp,
             action_s={},
             case_num=0,
             case_name_num=0,
             SURF="",
             RUN_STARTDATE = "",
             STOP_N = "1"):
    
    usp.modify_surf(usr_surfdata=SURF, action=action_s, urban_type=2, mode="replace", surfata_name=f"lhs_{case_name_num}_surfdata.nc")

    usp_res = usp.run(
                    case_name = f"msc_{case_name_num}",
                    RUN_STARTDATE = RUN_STARTDATE, # the start date of the simulation, must include in the forcing file time range
                    STOP_OPTION = "ndays", # can be 'ndays', 'nmonths', 'nyears', 'nsteps'; nsteps means 1800s
                    STOP_N = STOP_N, # run for 10 years
                    hist_type="GRID",
                    RUN_TYPE= "branch",
                    RUN_REFCASE= "man_spinup", #! the reference case name, please refer to `1_spinup.py`
                    RUN_REFDATE= "2022-07-18", #! the start date of the reference case, please refer to `1_spinup.py`
                )
    
    #print(f'Experiment {action_s} , case_num {case_num} completed.')
    #print(f'usp_res: {usp_res}')
    
    #the ouptut path is in op_path
    #op_path = os.path.join(usp.output_path, 'lnd', 'hist')
    
    #usp_res = []
    #
    #for filename in os.listdir(op_path):
    #    
    #    if f"msc_{case_name_num}" in filename:
    #        
    #        usp_res.append(os.path.join(op_path, filename))
    
    return usp_res

def worker(worker_args):
    # Set the parameters
    usp, exp, case_num, i, input_dict = worker_args
    
    case_name_num = case_num 
    case_num = case_num + i
    
    # Run the CLMU model
    res = run_clmu(
                  usp=usp,
                  action_s=exp,
                  case_num=case_num,
                  case_name_num = case_name_num,
                  SURF=input_dict['SURF'],
                  RUN_STARTDATE=input_dict['RUN_STARTDATE'],
                  STOP_N=input_dict['LENGTH'])
    outputpath="lhs_data"
    
    try:
        if len(res) > 0:
            os.makedirs(outputpath, exist_ok=True)
            os.system(f'mv {res[0]} {outputpath}/{case_num}.nc')
        else:
            print(f"Error moving {case_num}.nc")
    except:
        print(f"Error moving {case_num}.nc")
        pass
    #print(f'Experiment {exp} completed.')
    return res

## <--- Define the main function --->
def main(
        usp,
        exps,
        nproc = None,
        input_dict = None
        ):

    """
    Main function to run the CLMU model with Latin Hypercube Sampling.
    
    Args:
        usp (object): usp_clmu object.
        exp_range (list of tuples): Ranges for each parameter. Each tuple contains (min, max) for that parameter.
        cities (list of str): List of cities to run the model.
        n (int): Number of samples.
        nproc (int): Number of processes to run in parallel.
    """

    n = len(exps)
    
    print(f'Number of experiments: {n}')
    #print(f'Experiments: {exps}')
    
    num_processes = cpu_count() if nproc is None else nproc
    print(f"num_processes: {num_processes}")
    
    for i in range(0, len(exps), num_processes):
    
        # multiprocessing.Pool is used to run the CLMU model in parallel
        with Pool(processes=num_processes) as pool:
            batch_results = pool.map(
                worker,
                [(usp, lhs_exp, j , i, input_dict) for j, lhs_exp in enumerate(exps[i:i+num_processes])]
            )
            
        print(f'Batch {i//num_processes} completed.')
            
            
if __name__ == '__main__':
    
    input_dict = {
            'FORCING': "../1_data_collection/era5_forcing_53.417_-2.25_30_2010_1_2023_12.nc",
            'SURF': "../1_data_collection/surfdata_mcr.nc",
            'RUN_STARTDATE': "2022-07-18",
            'LENGTH': "2"
    }
    
    
    nproc, container_type, input_file = initialize_params()
    
    
    #! must define the the usp first, then pass it to the main function
    # or it will raise an error when running in parallel
    # it is because the usp object is will check the surfdata at the beginning for all initialized usp objects
    usp = usp_clmu(container_type = container_type)
    usp.check_forcing(usr_forcing=input_dict['FORCING'])
    usp.check_surf(usr_surfdata=input_dict['SURF'])
    usp.check_domain()
    
    with open(input_file, 'rb') as f:
        lhs_exps_dict = pickle.load(f)
        
        # lhs_exps_dict is a list of dictionaries
        # each dictionary contains the parameter values for each experiment for `pyclmuapp.usp_clmu`
        # e.g., {'ALB_ROOF_DIF': 0.8671086069477685, 'ALB_ROOF_DIR': 0.8671086069477685,
        # 'EM_ROOF': 0.9902408721077689, 'ALB_IMPROAD_DIF': 0.1519206948434331, 
        # 'ALB_IMPROAD_DIR': 0.1519206948434331, 'EM_IMPROAD': 0.8978307358199666, 
        # 'ALB_PERROAD_DIF': 0.10365642624521552, 'ALB_PERROAD_DIR': 0.10365642624521552, 
        # 'EM_PERROAD': 0.9378550603825474, 'ALB_WALL_DIF': 0.6292637272769789, 
        # 'ALB_WALL_DIR': 0.6292637272769789, 'EM_WALL': 0.9930753064901631, 
        # 'WIND_HGT_CANYON': 0.7667338209337629, 
        # 'HT_ROOF': 1.5334676418675257, 'CANYON_HWR': 1.124636590418945, 
        # 'WTLUNIT_ROOF': 0.04269840319863123, 'WTROAD_PERV': 0.3553999065873856}
        
    main(usp, exps=lhs_exps_dict, nproc=nproc, input_dict=input_dict)