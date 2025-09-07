import numpy as np
import pickle
import json
import argparse

def get_params():
    parser = argparse.ArgumentParser(description='Run CLMU')
    parser.add_argument('--n', type=int, 
                        default=100, help='Number of samples to generate')
    parser.add_argument('--exp_dist', type=str, 
                        default="../1_data_collection/mcr_up_dist.json", help='Path to the distribution file')
    parser.add_argument('--output', type=str,
                        default="lhs_exps_dict.pkl", help='Output file')
    return parser.parse_args()

def initialize_params():
    try:
        import __main__  # check if running as script
        if hasattr(__main__, '__file__'):  # running as script
            args = get_params()
            return args.n, args.exp_dist, args.output
    except ImportError:
        pass
    return 100, "../1_data_collection/mcr_up_dist.json", "lhs_exps_dict.pkl"

## <--- Define the Latin Hypercube Sampling function --->
def LHS(n, ranges, seed=0):
    """
    Generate Latin Hypercube Sample (LHS) in a given dimension with different ranges for each dimension.

    Args:
        n (int): Number of samples.
        ranges (list of tuples): Ranges for each dimension. Each tuple contains (min, max) for that dimension.

    Returns:
        np.array: Latin Hypercube Sample.
    """
    
    np.random.seed(seed)

    dims = len(ranges)

    lhs = np.zeros((n, dims))

    # Generate random numbers for each dimension
    for i, (min_val, max_val) in enumerate(ranges):
        step = (max_val - min_val) / n
        for j in range(n):
            lhs[j, i] = np.random.uniform(min_val + j * step, min_val + (j + 1) * step)

    # Shuffle the samples
    for i in range(dims):
        np.random.shuffle(lhs[:,i])

    return lhs


def main(exp_dist='../1_data_collection/mcr_up_dist.json',
         n=100,
         outputfile='lhs_exps_dict.pkl'
        ):

    """
    Main function to run the CLMU model with Latin Hypercube Sampling.
    
    Args:
        exp_range (list of tuples): Ranges for each parameter. Each tuple contains (min, max) for that parameter.
        cities (list of str): List of cities to run the model.
        n (int): Number of samples.
        nproc (int): Number of processes to run in parallel.
    """

    with open(exp_dist, 'r') as f:
        exp_dis_range = json.load(f)
        
    exp_range = []
    
    varlist = [
    'ALB_ROOF',
    'EM_ROOF',
    'ALB_IMPROAD',
    'EM_IMPROAD',
    'ALB_PERROAD',
    'EM_PERROAD',
    'ALB_WALL',
    'EM_WALL',
    'HT_ROOF',
    'CANYON_HWR',
    'WTLUNIT_ROOF',
    'WTROAD_PERV']
    
    
    for key in varlist:
        
        low = 0.8*exp_dis_range[key][0]
        high = 1.2*exp_dis_range[key][1] 
        
        if ("ALB" in key) or ("EM" in key) or ("WT" in key):
            high = high if high < 1 else 1
            
        
        exp_range.append((low, high))


    lhs_exps = LHS(n, exp_range)
    
    lhs_exps_dict = []
    for i in range(n):
        dict_ = {}
        for j, key in enumerate(varlist):
            
            if "ALB" in key:
                dict_[f"{key}_DIF"] = lhs_exps[i][j] 
                dict_[f"{key}_DIR"] = lhs_exps[i][j] 
                
            elif "HT" in key:
                
                dict_['WIND_HGT_CANYON'] = lhs_exps[i][j] * 0.5
                dict_[key] = lhs_exps[i][j]
                
            else:
                dict_[key] = lhs_exps[i][j]
                
                
        lhs_exps_dict.append(dict_)
    
    print(f'Number of experiments: {len(lhs_exps_dict)}')
    print(f'Experiment ranges: {exp_range}')
    print(f'Experiments: {lhs_exps_dict}')
    
    with open(outputfile, 'wb') as f:
        pickle.dump(lhs_exps_dict, f)
        
        
if __name__ == '__main__':
    
    n, exp_dist, output = initialize_params()
    main(exp_dist=exp_dist, n=n, outputfile=output)