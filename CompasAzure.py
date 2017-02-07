import numpy as np
import itertools
import os

nBinariesPerGridPoint = 100
nBinariesPerTask = 25

assert nBinariesPerTask <= nBinariesPerGridPoint
assert nBinariesPerGridPoint % nBinariesPerTask == 0

nTasksPerGridPoint = nBinariesPerGridPoint/nBinariesPerTask

gridDictionary = {}
gridDictionary['--common-envelope-alpha'] = np.linspace(0.,2.,3)

initialSeed = 1234567
np.random.seed(initialSeed)

shareSeeds = False

def prepareCommands():

    commands = specifyCommandLineOptions()
        
    return commands

def specifyCommandLineOptions():
    """Generates a string for the terminal command to run COMPAS. This function is intended to be modified by the user, so that they may swap out constant values for functions etc.
        Options not to be included in the command line should be set to pythons None (except booleans, which should be set to False)

    """
    number_of_binaries = nBinariesPerTask
    random_seed = 0
    debugging = False
    populationPrinting = False
    hdf5Output = True
    hdf5OutputDirectory = './compasOutput.h5'

    output = os.getcwd()
    
    #-- set inidividual system parameters
    single_star = False
    individual_system = False
    individual_initial_primary_mass = 96.2
    individual_initial_secondary_mass = 60.2
    individual_initial_primary_metallicity = 0.0006
    individual_initial_secondary_metallicity = 0.0006
    individual_initial_primary_type = 1
    individual_initial_secondary_type = 1
    individual_initial_primary_rotational_velocity = 0.0
    individual_initial_secondary_rotational_velocity = 0.0
    individual_initial_orbital_separation = 11.5
    individual_initial_orbital_period = -1
    individual_initial_orbital_eccentricity = 0.0
    individual_initial_primary_core_mass = 0
    individual_initial_secondary_core_mass = 0
    individual_effective_initial_primary_mass = 0
    individual_effective_initial_secondary_mass = 0
    individual_initial_primary_age = 0
    individual_initial_secondary_age = 0


    use_mass_loss = True
    mass_transfer = True
    post_newtonian_evolution = False
    detailed_output = False
    only_double_compact_objects = False
    lambda_calculation_every_timestep = False

    metallicity = 0.002

    common_envelope_alpha = 1.0
    common_envelope_lambda = 0.1 #1.0 # default was 0.1
    common_envelope_hertzsprung_gap_assumption = 'PESSIMISTIC_HG_CE' #'OPTIMISTIC_HG_CE'
    common_envelope_lambda_prescription = 'LAMBDA_FIXED'
    common_envelope_slope_Kruckow = -2.0/3.0
    common_envelope_zeta_prescription = 'STARTRACK'

    tides_prescription = 'NONE'
    mass_loss_prescription = 'VINK'
    luminous_blue_variable_multiplier = 1.5 #10.0 #1.5 #10.0
    wolf_rayet_multiplier = 1.0

    circularise_binary_during_mass_transfer = False
    mass_transfer_prescription = 'DEMINK'
    mass_transfer_angular_momentum_loss_prescription = 'ISOTROPIC' #'ARBITRARY' #
    mass_transfer_accretion_efficiency_prescription = 'THERMAL' #'FIXED' #
    mass_transfer_fa = 0.5
    mass_transfer_jloss = 1.0
    mass_transfer_rejuvenation_prescription = 'STARTRACK'
    mass_transfer_thermal_limit_accretor= 'CFACTOR'
    mass_transfer_thermal_limit_C= 10.0

    #-- Critical mass ratios for MT. 0.0 for always stable, < 0.0 to disable
    critical_mass_ratio_MS_non_degenerate_accretor = 0.65
    critical_mass_ratio_MS_degenerate_accretor = 0.0
    critical_mass_ratio_HG_non_degenerate_accretor = -1.0 #0.40
    critical_mass_ratio_HG_degenerate_accretor = -1.0 #0.21
    critical_mass_ratio_giant_non_degenerate_accretor = -1.0 #0.0
    critical_mass_ratio_giant_degenerate_accretor = -1.0 #0.87
    critical_mass_ratio_helium_giant_non_degenerate_accretor = -1.0 #1.28
    critical_mass_ratio_helium_giant_degenerate_accretor = -1.0 #0.87

    #-- X-Ray Binaries (HMXB and ULX) flags and values
    useXRayBinaries = False
    x_ray_binary_rlof_factor = 0.5
    detailed_output_XRayBinaries = False

    maximum_evolution_time = 13700.0
    maximum_number_iterations = 99999

    initial_mass_function = 'KROUPA'
    initial_mass_min = 7.0
    initial_mass_max = 100.0

    initial_mass_power = 0.0

    semi_major_axis_distribution = 'FLATINLOG'
    semi_major_axis_min = 0.1
    semi_major_axis_max = 1000.0

    spin_distribution = 'ZERO'
    spin_assumption = 'BOTHALIGNED'
    spin_mag_min = 0.0
    spin_mag_max = 1.0

    mass_ratio_distribution = 'FLAT'
    mass_ratio_min = 0.0
    mass_ratio_max = 1.0

    eccentricity_distribution = 'ZERO'
    eccentricity_min = 0.0
    eccentricity_max = 1.0

    rotational_velocity_distribution = 'ZERO'

    orbital_period_min = 1.1
    orbital_period_max = 1000

    sample_kick_velocity_sigma = False
    sample_kick_velocity_sigma_min = 0.0
    sample_kick_velocity_sigma_max = 400.0

    sample_kick_direction_power = False
    sample_kick_direction_power_min = -10.0
    sample_kick_direction_power_max = 10.0

    sample_common_envelope_alpha = False
    sample_common_envelope_alpha_min = 0.0
    sample_common_envelope_alpha_max = 5.0

    sample_wolf_rayet_multiplier = False
    sample_wolf_rayet_multiplier_min = 0.0
    sample_wolf_rayet_multiplier_max = 10.0

    sample_luminous_blue_variable_multiplier = False
    sample_luminous_blue_variable_multiplier_min = 0.0
    sample_luminous_blue_variable_multiplier_max = 10.0

    remnant_mass_prescription = 'FRYER2012'
    fryer_supernova_engine = 'DELAYED' #'RAPID' #'DELAYED'
    black_hole_kicks = 'FALLBACK'
    kick_velocity_distribution = 'MAXWELLIAN'
    kick_velocity_sigma = 250
    fix_dimensionless_kick_velocity = -1
    kick_direction = 'ISOTROPIC'
    kick_direction_power = 0.0

    pair_instability_supernovae = False
    PISN_lower_limit = 130.0
    PISN_upper_limit = 250.0

    pulsation_pair_instability = False
    PPI_lower_limit = 100.0
    PPI_upper_limit = 130.0

    booleanChoices  =  [debugging,single_star,individual_system,use_mass_loss,mass_transfer,post_newtonian_evolution,detailed_output,only_double_compact_objects,
                        sample_kick_velocity_sigma,sample_kick_direction_power,sample_common_envelope_alpha,sample_wolf_rayet_multiplier,
                        sample_luminous_blue_variable_multiplier,populationPrinting,hdf5Output,lambda_calculation_every_timestep,circularise_binary_during_mass_transfer, useXRayBinaries]
    booleanCommands  =  ['--debugging','--single-star','--individual-system','--use-mass-loss','--massTransfer','--PNEcc','--detailedOutput','--only-double-compact-objects','--sample-kick-velocity-sigma','--sample-kick-direction-power','--sample-common-envelope-alpha','--sample-wolf-rayet-multiplier',
            '--sample-luminous-blue-variable-multiplier','--populationDataPrinting','--hdf5-output','--lambda-calculation-every-timeStep','--circulariseBinaryDuringMassTransfer','--XRayBinaries']


    numericalChoices  =  [number_of_binaries,individual_initial_primary_mass,individual_initial_secondary_mass,individual_initial_primary_metallicity,
                        individual_initial_secondary_metallicity,individual_initial_primary_type,individual_initial_secondary_type,
                        individual_initial_primary_rotational_velocity,individual_initial_secondary_rotational_velocity,individual_initial_orbital_separation,
                        individual_initial_orbital_period,individual_initial_orbital_eccentricity,individual_initial_primary_core_mass,
                        individual_initial_secondary_core_mass,individual_effective_initial_primary_mass,individual_effective_initial_secondary_mass,
                        individual_initial_primary_age,individual_initial_secondary_age,metallicity,common_envelope_alpha,common_envelope_lambda,
                        luminous_blue_variable_multiplier,wolf_rayet_multiplier,mass_transfer_fa,mass_transfer_jloss,maximum_evolution_time,
                        maximum_number_iterations,initial_mass_min,initial_mass_max,initial_mass_power,semi_major_axis_min,semi_major_axis_max,spin_mag_min,
                        spin_mag_max,mass_ratio_min,mass_ratio_max,eccentricity_min,eccentricity_max,orbital_period_min,orbital_period_max,kick_velocity_sigma,
                        fix_dimensionless_kick_velocity,kick_direction_power,sample_kick_velocity_sigma_min,sample_kick_velocity_sigma_max,
                        sample_kick_direction_power_min,sample_kick_direction_power_max,sample_common_envelope_alpha_min,
                        sample_common_envelope_alpha_max,sample_wolf_rayet_multiplier_min,sample_wolf_rayet_multiplier_max,
                        sample_luminous_blue_variable_multiplier_min,sample_luminous_blue_variable_multiplier_max,random_seed,
                        critical_mass_ratio_MS_non_degenerate_accretor,critical_mass_ratio_MS_degenerate_accretor,
                        critical_mass_ratio_HG_non_degenerate_accretor,critical_mass_ratio_HG_degenerate_accretor,critical_mass_ratio_giant_non_degenerate_accretor,
                        critical_mass_ratio_giant_degenerate_accretor,critical_mass_ratio_helium_giant_non_degenerate_accretor,critical_mass_ratio_helium_giant_degenerate_accretor,
                        mass_transfer_thermal_limit_C, common_envelope_slope_Kruckow,PISN_lower_limit,PISN_upper_limit,PPI_lower_limit,PPI_upper_limit]
    numericalCommands  =  ['--number-of-binaries','--individual-initial-primary-mass','--individual-initial-secondary-mass','--individual-initial-primary-metallicity',
                    '--individual-initial-secondary-metallicity',
                    '--individual-initial-primary-type','--individual-initial-secondary-type','--individual-initial-primary-rotational-velocity','--individual-initial-secondary-rotational-velocity',
                    '--individual-initial-orbital-separation','--individual-initial-orbital-period','--individual-initial-orbital-eccentricity','--individual-initial-primary-core-mass',
                    '--individual-initial-secondary-core-mass','--individual-effective-initial-primary-mass','--individual-effective-initial-secondary-mass','--individual-initial-primary-age',
                    '--individual-initial-secondary-age','--metallicity','--common-envelope-alpha','--common-envelope-lambda','--luminous-blue-variable-multiplier','--wolf-rayet-multiplier',
                    '--mass-transfer-fa','--mass-transfer-jloss','--maximum-evolution-time','--maximum-number-iterations','--initial-mass-min','--initial-mass-max','--initial-mass-power',
                    '--semi-major-axis-min','--semi-major-axis-max','--spin-mag-min','--spin-mag-max','--mass-ratio-min','--mass-ratio-max','--eccentricity-min','--eccentricity-max','--orbital-period-min',
                    '--orbital-period-max','--kick-velocity-sigma','--fix-dimensionless-kick-velocity','--kick-direction-power',
                    '--sample-kick-velocity-sigma-min','--sample-kick-velocity-sigma-max',
                    '--sample-kick-direction-power-min','--sample-kick-direction-power-max','--sample-common-envelope-alpha-min','--sample-common-envelope-alpha-max','--sample-wolf-rayet-multiplier-min','--sample-wolf-rayet-multiplier-max','--sample-luminous-blue-variable-multiplier-min','--sample-luminous-blue-variable-multiplier-max','--random-seed','--critical-mass-ratio-MS-non-degenerate-accretor','--critical-mass-ratio-MS-degenerate-accretor','--critical-mass-ratio-HG-non-degenerate-accretor','--critical-mass-ratio-HG-degenerate-accretor','--critical-mass-ratio-giant-non-degenerate-accretor','--critical-mass-ratio-giant-degenerate-accretor','--critical-mass-ratio-helium-giant-non-degenerate-accretor','--critical-mass-ratio-helium-giant-degenerate-accretor','--mass-transfer-thermal-limit-C','--common-envelope-slope-Kruckow','--PISN-lower-limit','--PISN-upper-limit','--PPI-lower-limit','--PPI-upper-limit']


    stringChoices  =  [tides_prescription,mass_loss_prescription,mass_transfer_prescription,mass_transfer_angular_momentum_loss_prescription,
                    mass_transfer_accretion_efficiency_prescription,mass_transfer_rejuvenation_prescription,initial_mass_function,semi_major_axis_distribution,
                    spin_distribution,spin_assumption,mass_ratio_distribution,eccentricity_distribution,rotational_velocity_distribution,remnant_mass_prescription,fryer_supernova_engine,
                    black_hole_kicks,kick_velocity_distribution,kick_direction,output,common_envelope_hertzsprung_gap_assumption,hdf5OutputDirectory,common_envelope_lambda_prescription,common_envelope_zeta_prescription,mass_transfer_thermal_limit_accretor]

    stringCommands  =  ['--tides-prescription','--mass-loss-prescription','--mass-transfer-prescription','--mass-transfer-angular-momentum-loss-prescription',
                    '--mass-transfer-accretion-efficiency-prescription','--mass-transfer-rejuvenation-prescription','--initial-mass-function','--semi-major-axis-distribution','--spin-distribution',
                    '--spin-assumption','--mass-ratio-distribution','--eccentricity-distribution','--rotational-velocity-distribution','--remnant-mass-prescription','--fryer-supernova-engine',
                    '--black-hole-kicks','--kick-velocity-distribution','--kick-direction','--output','--common-envelope-hertzsprung-gap-assumption','--hdf5-output-directory','--common-envelope-lambda-prescription','--common-envelope-zeta-prescription','--mass-transfer-thermal-limit-accretor']


    command = hyperparameterGridCommand(booleanChoices,booleanCommands,numericalChoices,numericalCommands,stringChoices,stringCommands)

    return command
    
def generateCommandLineOptions(binaries_executable,booleanChoices,booleanCommands,numericalChoices,numericalCommands,stringChoices,stringCommands):

    nBoolean = len(booleanChoices)
    assert len(booleanCommands) == nBoolean

    nNumerical = len(numericalChoices)
    assert len(numericalCommands) == nNumerical

    nString = len(stringChoices)
    assert len(stringCommands) == nString

    command = binaries_executable + ' '

    for i in range(nBoolean):

        if booleanChoices[i] == True:

            command += booleanCommands[i] + ' '

    for i in range(nNumerical):

        if not numericalChoices[i] == None:

            command += numericalCommands[i] + ' ' + str(numericalChoices[i]) + ' '

    for i in range(nString):

        if not stringChoices[i] == None:

            command += stringCommands[i] + ' ' + stringChoices[i] + ' '

    return command
    
def hyperparameterGridCommand(booleanChoices,booleanCommands,numericalChoices,numericalCommands,stringChoices,stringCommands):

    keys = gridDictionary.keys()

    valuesLists = []
    nGridPoints = 1
    for key in keys:
        nGridPoints *= len(gridDictionary[key])
        valuesLists.append(gridDictionary[key])
        
    bashCommands = []
        
    for en,combination in enumerate(itertools.product(*valuesLists)):
    
        #if we're sharing seeds between gridpoints, reseed the generator
        if shareSeeds:
            np.random.seed(initialSeed)
    
        for k in range(nTasksPerGridPoint):
      
            bashCommand = ''

            for i, val in enumerate(combination):

                for index,command in enumerate(numericalCommands):
                    if command == keys[i]:
                        break
                numericalChoices[index] = val

            seed = np.random.randint(0,2**31)
        
            for index,command in enumerate(numericalCommands):
                if command == '--random-seed':
                    break
            numericalChoices[index] = seed

            bashCommand += generateCommandLineOptions('~/COMPAS',booleanChoices,booleanCommands,numericalChoices,numericalCommands,stringChoices,stringCommands)

            bashCommands.append(bashCommand)

    return bashCommands
    
if __name__ == '__main__':
    prepareCommandLineFilesAndSubmit()
