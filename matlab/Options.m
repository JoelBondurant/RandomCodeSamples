classdef Options < handle
	
	properties (SetAccess = private, GetAccess = public)
		databaseName;
		samplingOptimizationCacheThresholdInHours;
		runOptimization;
		optimizer;
		optimizerX0;
		compiledSimulation;
		f_CIThreshold;
		minArrivalRate;
		maxIterations;
		maxDeltah;
		optimizerMaxIterations;
		utilizationTargetReduction;
		qtLimit;
		maxSimConfIterations;
		simWarmup;
		simArrivalsPerSample;
		simNumSamples;
		simAlpha;
		u_LPMinDiff;
		f_URed;
		n_LoopLimit;
		f_SlackThr;
		n_ExitStepLimit;
		u_Target;
		n_PerInHorz;
		n_PerInHorz_2;
		n_HrsInPeriod;
		n_ShiftsPerDay;
		n_DaysInWIPFcst;
		t_Fcst_f;
		t_Fcst;
		t_OptDTThreshold;
		f_TargBound;
		z_TargBound;
		I_TargetType;
		p_Lower_TargBound;
		p_Upper_TargBound;
		ctqPath;
		wipPath;
	end
	
	methods
		function obj = Options()
			optionsFile = fopen('c:/SensorAnalytics/trunk/MATLAB/CycleTimeAndQueuing/Options.txt', 'r');
			while ~feof(optionsFile)
				optionText = fgetl(optionsFile);
				optionText = strcat('obj.', optionText);
				eval(optionText);
			end
			fclose(optionsFile);
		end
	end
	
end

