__author__ = 'MaximilianKing'


"""
Main model parameters.
"""

####################
PROCESSES = 1           # number of processes in parallel (quadcore)
rSeed_pop = 0           # seed for population RNG (0 for pure random, -1 for stepwise up to N_NC
rSeed_net = 0
rSeed_run = 0
N_MC = 1               # total number of iterations (Monte Carlo runs)
N_REPS = 1
N_POP = 55000           # population size
TIME_RANGE = 60        # total time steps to iterate
burnDuration = 60
model = 'Overdose'         # Model Type for fast flag toggling
network_type = 'scale_free' #scale_free or max_k_comp_size
setting = 'RI_OD_Morality'
####################


"""
Output flags and settings
"""
outputDir = ''

printIncidenceEvents = False
printStartAgentList = False
printEndingAgentList = False
printIntermAgentList = False
intermPrintFreq = 60
calcNetworkStats = False
calcComponentStats = False
drawFigures = False
drawEdgeList = False
drawFigureColor = 'SO'

"""
Calibration scaling parameters for fitting to empirical data
"""

PARTNERTURNOVER = 0.0         # Partner acquisition parameters (higher number more partnering)
cal_NeedlePartScaling = 0.90     # IDU partner number scaling
cal_NeedleActScaling = 0.60      # IDU act frequency scaling factor
cal_SexualPartScaling = 0.90     # Sexual partner number scaling factor
cal_SexualActScaling = 0.80      # Sexual acts  scaling factor
cal_pXmissionScaling = 1.0      # Global transmission probability scaling factor
cal_AcuteScaling = 4.3         # Infectivity multiplier ratio for Acute status infections
cal_RR_Dx = 0.53                # Risk reduction in transmission probability for agents diagnosed
cal_RR_HAART = 1.0              # Scaling factor for effectiveness of ART therapy on xmission P
cal_TestFreq = 0.70              # Scaling factor for testing frequency
cal_Mortality = 1.0             # Scaling factor for all cause mortality rates
cal_ProgAIDS = 1.0              # Scaling factor for all progression to AIDS from HIV rates
cal_ART_cov = 0.70               # Scaling factor for enrollment on ART probability
cal_IncarP = 1.0                # Scaling factor for probability of becoming incarcerated
cal_raceXmission = 1.0          # Scaling factor for increased STI transmission P comparing race1/race2
cal_ptnrSampleDepth = 100       # Sampling depth for partnering algorithm.


"""
High risk params
"""
HR_partnerScale = 0       # Linear increase to partner number during HR period
HR_proportion = 0.0         #Proportion of people who enter HR group when partner incarcerated
HR_M_dur = 13                #Duration of high risk for males post release
HR_F_dur = 13               #Duration of high risk for females post release

"""
Misc. params
"""

flag_AssortativeMix = False     # Boolean for if assortative mixing occurs at all
AssortMixType = 'HR'            # Other assortative mixing types
flag_AgeAssortMix = False       # Assortative mix by age
flag_RaceAssortMix = False      # Assortative mix by race
AssortMixCoeff = 0.3            # Proportion of following given assort mix rules
safeNeedleExchangePrev = 1.0    # Prevalence scalar on SNE
initTreatment = 9999999              # Requirement to start treatment
treatmentCov = 0.0             # Prop that receive treatment

"""
Incarceration params
"""
inc_JailMax = 22
inc_JailMin = 1
inc_JailTestProb = 0.69
inc_PrisMax = 96
inc_PrisMin = 45
inc_PrisTestProb = 0.69
inc_PropPrison = 0.5
inc_ARTenroll = 0.51
inc_ARTadh = 0.21
inc_ARTdisc = 0.12
inc_Recidivism = 0.267
inc_PtnrDissolution = 0.55
inc_treatment_startdate = 48    # Timestep where inc treatment can begin
inc_treatment_dur = 12          # Duration for which agents are forced on respective treatment post release
inc_treat_set = ['HM']          # Set of agent classifiers effected by HR treatment
inc_treat_HRsex_beh = True      # Remove sexual higrisk behaviour during treatment duration
inc_treat_IDU_beh = True         # Remove IDU behav:iour during treatment duration
inc_treat_RIC = False            # Force retention in care of ART therapy

"""
IDU/NIDU Treatment params
"""
p_mort_oat_scalar = 0.4            # Prob mortatlity risk for on OAT
p_mort_nalt_scalar = 0.2            # Prob mort risk for on naltrx
p_mort_oat_postcess_scalar = 2.0    # Prob mortality risk post exit OAT
p_mort_nalt_postcess_scalar = 8.0   # Prob mort risk post ext Naltx
p_mort_post_release_scalars={1:20,  # Prob mort risk post release (1 timestep, 2 timestep, 3-HR dura)
                             2:4,
                             3:2}

MATasOAT = 0.992                    # Percentage of MAT as OAT in community
p_enroll_OAT_post_release = 0.0     # prob of enrolling OAT post release
p_enroll_Nal_post_release = 0.0     # prob of enrolling naltx post release
p_discont_trt_on_incar = 1.0        # Probability of exit trt upon incarceration




"""
PrEP params
"""
PrEP_type = "Oral"      #Oral/Inj PrEP modes
PrEP_Target = 0.10      # Target coverage for PrEP therapy at 10 years (unused in non-PrEP models)
PrEP_startT = 0         # Start date for PrEP program (0 for start of model)
PrEP_Adherence = 0.82   # Probability of being adherent
PrEP_AdhEffic = 0.96    # Efficacy of adherence PrEP
PrEP_NonAdhEffic = 0.76 # Efficacy of non-adherence PrEP
PrEP_falloutT = 0       # During PrEP remains effective post discontinuation
PrEP_resist = 0.0
PrEP_disc = 0.15
PrEP_target_model = 'IncarHR' #Clinical, Allcomers, HighPN5, HighPN10, SRIns, SR,Rec, Incar,IncarHR, HR
PrEP_clinic_cat = 'Mid'

if PrEP_type == 'Oral':
    PrEP_Adherence = 0.923
    PrEP_AdhEffic = 0.96
    PrEP_NonAdhEffic = 0.76
    PrEP_falloutT = 1
    PrEP_disc = 0.15
elif PrEP_type == 'Inj':
    PrEP_Adherence = 1.0
    PrEP_AdhEffic = 1.0
    PrEP_NonAdhEffic = 1.00
    PrEP_falloutT = 12
    PrEP_disc = 0.04
    PrEP_peakLoad = 4.91
    PrEP_halflife = 40.0


"""
Model Type for fast flag toggling
    flag_incar      Incarceration effects
    flag_PrEP       PrEP enrollment
    flag_HR         High risk behavior for incar or genPop
    flag_ART        ART therapy enrollment
    flag_DandR      Die and replace functionality

"""
if model == 'PrEP':
    flag_incar = False
    flag_PrEP = True
    flag_HR = False
    flag_ART = True
    flag_DandR = True
    flag_staticN = False
    flag_agentZero = False

elif model == 'Incar':
    flag_incar = True
    flag_PrEP = True
    flag_HR = True
    flag_ART = True
    flag_DandR = True
    flag_staticN = False
    flag_agentZero = False

elif model == 'NoIncar':
    flag_incar = False
    flag_PrEP = False
    flag_HR = True
    flag_ART = True
    flag_DandR = True
    flag_staticN = False
    flag_agentZero = False

elif model == 'StaticZero':
    flag_incar = False
    flag_PrEP = False
    flag_HR = False
    flag_ART = False
    flag_DandR = False
    flag_staticN = True
    flag_agentZero = True

elif model == 'Overdose':
    flag_incar = True
    flag_PrEP = False
    flag_HR = True
    flag_ART = False
    flag_DandR = True
    flag_staticN = True
    flag_agentZero = False

elif model == 'Custom':
    flag_incar = True
    flag_PrEP = False
    flag_HR = True
    flag_ART = False
    flag_DandR = True
    flag_staticN = True
    flag_agentZero = False

agentPopulations = ['HM','HF']
agentSexTypes = ['HM', 'HF', 'MSM']
"""
RaceClass is a distinct racial/ethnic/social classification for demographics of the population.
ID is the specific mode of partnership the agent engages in (ie MSM, HM, HF, PWID)
RaceClass agent classifier template
"""
RC_template = {     'Race':None,            #Race of demographic
                    'Class':None,           #Classification of networking
                    'POP':0.0,              #Percentage of total raceclass population that are ID
                    'HIV':0.0,              #Proportion of total ID population that are HIV
                    'AIDS':0.0,             #Proportion of total HIV_ID that are AIDS
                    'HAARTprev':0.0,        #Proportion of HIV_TESTED_ID that are enrolled on ART
                    'INCARprev':0.0,        #Proportion of ID that are incarcerated
                    'TestedPrev':0.0,       #Proportion of HIV_ID that are tested positively
                    'HighRiskPrev':0.0,     #Proportion of agents that are HR
                    'IDUprev':0.0,          #Proportion of agents that are IDU
                    'mNPart':0.0,           #Mean number of sex partners
                    'NUMPartn':0.0,         #Number of partners (redundant)
                    'NUMSexActs':0.0,       #Mean number of sex acts with each partner
                    'UNSAFESEX':0.0,        #Probability of engaging in unsafe sex (per act)
                    'NEEDLESH':0.0,         #Probability of sharing syringes during join drug use (per act)
                    'HIVTEST':0.0,          #Probability of testing for HIV
                    'INCAR':0.0,            #Probability of becoming incarcerated (rate)
                    'HAARTadh':0.0,         #Adherence to ART therapy
                    'HAARTdisc':0.0,        #Probability of discontinuing ART therapy
                    'PrEPdisc':0.0,         #Probability of discontinuing PrEP treatment
                    'MATprev':0.0,
                    'EligPartnerType':[],   #List of agent SO types the agent cant partner with
                    'AssortMixMatrix':[]    #List of assortMix Matrix to be zipped with EligPart
                }

RC_allTemplate = {  'Proportion':1.00,      #Proportion of total population that is raceclass
                    'HAARTdisc':0.018,      #Overall HAART discontinuation probability
                    'PrEPdisc':0.0,         #Overall PrEP discontinuation probability
                    'AssortMixCoeff':1.0,   #Proportion RC mixes with other raceclass
                }

RaceClass1 = {'MSM':{}, 'HM':{}, 'HF':{}, 'IDU':{}, 'ALL':{}}
RaceClass2 = {'MSM':{}, 'HM':{}, 'HF':{}, 'IDU':{}, 'ALL':{}}
for a in ['MSM','HM','HF','IDU']:
    RaceClass1[a] = dict(RC_template)
    RaceClass2[a] = dict(RC_template)

incarNIDUProb = 0.08
incarIDUProb = 0.15
incarProbScalar = 0.01
cal_MAT_disc_prob = 0.045
MATProbScalar = .005
RaceClass1['HM'].update({'POP': 0.60,
                         'INCARprev': 0.08,
                         'INCAR': incarNIDUProb * incarProbScalar,
                         'MATprev': .1,
                         'EligSE_PartnerType': ['HF']
                         })

RaceClass1['HF'].update({'POP': 0.40,
                         'INCARprev': 0.08,
                         'HighRiskPrev': 0.0,
                         'INCAR': incarNIDUProb * incarProbScalar,
                         'MATprev': .1,
                         'EligSE_PartnerType': ['HM']
                         })



RaceClass1['ALL'].update({'Proportion':0.818,
                          'HAARTdisc':0.0,
                          'PrEPdisc':0.0,
                          'AssortMixCoeff':1.0,
                          })

RaceClass2['HM'].update({'POP': 0.80,
                         'INCARprev': 0.15,
                         'HighRiskPrev': 0.0,
                         'INCAR': incarIDUProb * incarProbScalar,
                         'MATprev': .68,
                         'EligSE_PartnerType': ['HF']
                         })

RaceClass2['HF'].update({'POP': 0.20,
                         'INCARprev': 0.15,
                         'HighRiskPrev': 0.0,
                         'INCAR': incarIDUProb * incarProbScalar,
                         'MATprev': .68,
                         'EligSE_PartnerType': ['HM']
                         })

RaceClass2['ALL'].update({'Proportion':0.182,
                        'HAARTdisc':0.018,
                        'PrEPdisc':0.0,
                        'AssortMixCoeff':1.0,
                        })

DemographicParams = {'WHITE':RaceClass1, 'BLACK':RaceClass2}


"""
Partnership duration distribution bins
"""
sexualDurations = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
sexualDurations[1] = {'p_value':(0.323 + 0.262), 'min':1, 'max':6}
sexualDurations[2] = {'p_value':(0.323 + 0.262 + 0.116), 'min':7, 'max':12}
sexualDurations[3] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121), 'min':13, 'max':24}
sexualDurations[4] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualDurations[5] = {'min':37, 'max':48}

needleDurations = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
needleDurations[1] = {'p_value':1.0, 'min':1, 'max':6}
needleDurations[2] = {'p_value':(0.323 + 0.262), 'min':1, 'max':6}
needleDurations[3] = {'p_value':(0.323 + 0.262), 'min':1, 'max':6}
needleDurations[4] = {'p_value':(0.323 + 0.262), 'min':1, 'max':6}
needleDurations[5] = {'min':1, 'max':6}

PartnershipDurations = {'SEX':sexualDurations, 'NEEDLE':needleDurations}

"""
Partnership acts distribution bins
"""
sexualFrequency = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
sexualFrequency[1] = {'p_value':(0.323 + 0.262), 'min':1, 'max':6}
sexualFrequency[2] = {'p_value':(0.323 + 0.262 + 0.116), 'min':7, 'max':12}
sexualFrequency[3] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121), 'min':13, 'max':24}
sexualFrequency[4] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualFrequency[5] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualFrequency[6] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualFrequency[7] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualFrequency[8] = {'p_value':(0.323 + 0.262 + 0.116 + 0.121 + 0.06), 'min':25, 'max':36}
sexualFrequency[9] = {'min':37, 'max':48}

needleFrequency = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
needleFrequency[1] = {'p_value':1.0, 'min':1, 'max':6}
needleFrequency[2] = {'p_value':(0.323 + 0.262), 'min':3, 'max':12}
needleFrequency[3] = {'p_value':(0.323 + 0.262), 'min':6, 'max':24}
needleFrequency[4] = {'p_value':(0.323 + 0.262), 'min':9, 'max':36}
needleFrequency[5] = {'min':12, 'max':60}

PartnershipFrequency = {'SEX':sexualFrequency, 'NEEDLE':needleFrequency}



"""
Sexual and injection transmission probabilities
"""
SexTrans = {'MSM':{}, 'HM':{}, 'HF':{}}
SexTrans['MSM'] = {'0':0.00745, '1':0.005, '2':0.004, '3':0.002, '4':0.001, '5':0.0001}
SexTrans['HM'] = {'0':0.001, '1':0.001, '2':0.0008, '3':0.0004, '4':0.0002, '5':0.0001}
SexTrans['HF'] = {'0':0.001, '1':0.001, '2':0.0008, '3':0.0004, '4':0.0002, '5':0.0001}

NeedleTrans = {'0':0.007, '1':0.007, '2':0.0056, '3':0.0028, '4':0.0014, '5':0.0002}
TransmissionProbabilities = {'SEX':SexTrans, 'NEEDLE':NeedleTrans}



"""
Age bin distributions and HIV if utilized
"""
ageMatrix = {'WHITE':{}, 'BLACK':{}}
ageMatrix['WHITE'] = {'Prop':{0:0.0, 1:0.18, 2:0.18+0.16, 3:0.18+0.16+0.15, 4:0.18+0.16+0.15+0.20, 5:0.18+0.16+0.15+0.20+0.31},
                       'HIV':{0:0.0, 1:0.006, 2:0.029, 3:0.055, 4:0.069, 5:0.025}}
ageMatrix['BLACK'] = {'Prop':{0:0.0, 1:0.28, 2:0.28+0.24, 3:0.28+0.24+0.19, 4:0.28+0.24+0.19+0.15, 5:0.28+0.24+0.19+0.15+0.14},
                       'HIV':{0:0.0, 1:0.144, 2:0.144, 3:0.250, 4:0.377, 5:0.194}}


"""
Age mixing matrix for assortative mixing by age
"""
mixingMatrix = {1:{},2:{},3:{},4:{},5:{}}
mixingMatrix[1] = {1:0.500,2:0.226,3:0.123,4:0.088,5:0.064}
mixingMatrix[2] = {1:0.156,2:0.500,3:0.185,4:0.099,5:0.061}
mixingMatrix[3] = {1:0.074,2:0.162,3:0.500,4:0.184,5:0.079}
mixingMatrix[4] = {1:0.057,2:0.093,3:0.199,4:0.500,5:0.150}
mixingMatrix[5] = {1:0.062,2:0.086,3:0.128,4:0.224,5:0.500}

"""
Clinic bins for targetting strategies
Bins represent partner numbers of the following category 0:0, 1:1, 2:2,  3:3-4, 4:5-9, 5:10+
"""
clinicAgents = {'Low':{},'Mid':{},'High':{}}
clinicAgents['Mid'] = {0:{'Prob':0.0,'min':0,'max':0},
                       1:{'Prob':0.054,'min':0,'max':1},
                       2:{'Prob':0.061,'min':1,'max':2},
                       3:{'Prob':0.168,'min':3,'max':4},
                       4:{'Prob':0.246,'min':5,'max':9},
                       5:{'Prob':0.471,'min':10,'max':120}}
