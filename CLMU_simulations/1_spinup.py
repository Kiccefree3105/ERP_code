from pyclmuapp import usp_clmu
import os
import argparse

def get_params():
    parser = argparse.ArgumentParser(description='Run CLMU')
    parser.add_argument('--FORCING', type=str, 
                        default="../1_data_collection/era5_forcing_53.417_-2.25_30_2010_1_2023_12.nc", help='Path to the forcing file')
    parser.add_argument('--SURF', type=str, 
                        default="../1_data_collection/surfdata_mcr.nc", help='Path to the surface file')
    
    parser.add_argument('--RUN_STARTDATE', type=str,
                        default="2010-01-01", help='Start date of the simulation')
    parser.add_argument('--STOP_OPTION', type=str,
                        default="ndays", help='Stop option')
    parser.add_argument('--STOP_N', type=str,
                        default="4581", help='Stop number')
    parser.add_argument('--container_type', type=str,
                        default='docker', help='Container type to use')
    parser.add_argument('--case_name', type=str,
                        default="man_spinup", help='Name of the case to run')
    return parser.parse_args()

def initialize_params():
    try:
        import __main__  # check if running as script
        if hasattr(__main__, '__file__'):  # running as script
            args = get_params()
            return args.FORCING, args.SURF, args.RUN_STARTDATE, args.STOP_OPTION, args.STOP_N, args.container_type, args.case_name
    except ImportError:
        pass
    return "../1_data_collection/era5_forcing_53.417_-2.25_30_2010_1_2023_12.nc", "./1_data_collection/surfdata_mcr.nc", "2010-01-01", "days", "126", 'docker'





if __name__ == '__main__':
    
    FORCING, SURF, RUN_STARTDATE, STOP_OPTION, STOP_N, container_type, case_name = initialize_params()

    usp = usp_clmu(pwd=os.path.join(os.getcwd(), f'workdir'), # will create a temporary working directory workdir
                container_type = container_type)

    # the SourceMods/src.clm is not including the urban irr model
    usp_init = usp.run(
                case_name = case_name,
                SURF = SURF,
                FORCING = FORCING,
                RUN_STARTDATE = RUN_STARTDATE, # the start date of the simulation, must include in the forcing file time range
                STOP_OPTION = STOP_OPTION, # can be 'ndays', 'nmonths', 'nyears', 'nsteps'; nsteps means 1800s
                STOP_N = STOP_N, # run for 10 years)
    )
    