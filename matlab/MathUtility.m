classdef MathUtility < handle
	% MathUtility - A collection of floating point math utility methods.
	
	properties (GetAccess = public, SetAccess = public)
		printMessages = true; % print messages to stdout
	end
	
	properties (GetAccess = public, SetAccess = private)
		zeroDelta = 1e-9; % numbers smaller than this are considered zero.
		scalarZero = 0.0;
		scalarOne = 1.0;
	end
	
	methods (Access = public)
		
		function bool = contains(A, b)
			bool = any(ismember(A, b));
		end
		
		% Compare two scalars a, b and return a boolean if a ~ b.
		function [eq, percentDifference] = compareScalars(obj, a, b, varargin)
			eq = (abs(a - b) < obj.zeroDelta);
			percentDifference = (b - a) / a;
			if (obj.printMessages && ~isempty(varargin))
				if (eq)
					fprintf('No difference in %s. \n', varargin{1});
				else
					fprintf('***Difference in %s: %f vs. %f   %%diff = %f%% \n', varargin{1}, a, b, 100*percentDifference);
				end
			end
		end
		
		% Compare two matricies A & B and return a boolean if A ~ B, the maximum delta, and percent difference.
		function [eq, deltaCount, maxDelta, maxPercentDifference] = compareMatricies(obj, A, B, varargin)
			if ~(min(size(A) == size(B)))
				if (obj.printMessages)
					fprintf('*** Difference in %s array size. ***\n', varargin{1});
				end
				deltaCount = 0;
				maxDelta = 0;
				maxPercentDifference = 0;
				eq = false;
				return;
			end
			A(A == Inf) = 0;
			B(B == Inf) = 0;
			delta = B - A;
			deltaCount = sum(sum((abs(delta) > obj.zeroDelta)));
			eq = ~(deltaCount > obj.scalarZero);
			maxDelta = max(max(abs(delta)));
			percentDifference = (delta) ./ A;
			maxAbsPercentDifference = max(max(abs(percentDifference)));
			maxPercentDifference = percentDifference(isequalwithequalnans(abs(percentDifference), maxAbsPercentDifference));
			if (isempty(maxPercentDifference))
				maxPercentDifference = 0;
			else
				maxPercentDifference = maxPercentDifference(1,1);
			end
			if (obj.printMessages && ~isempty(varargin))
				if (eq)
					fprintf('No difference in %s. \n', varargin{1});
				else
					fmtStr = '***Difference in %s:  deltaCount = %u,  maxDelta = %f,  maxPercentDifference = %f%% \n';
					fprintf(fmtStr, varargin{1}, deltaCount, maxDelta, 100*maxPercentDifference);
				end
			end
		end
		
		% Compare two cell arrays A & B and return a boolean if A ~ B, the maximum delta, and percent difference.
		function [eq, deltaCount, maxDelta, maxPercentDifference] = compareCellArrays(obj, A, B, varargin)
			[n1a, n2a] = size(A);
			[n1b, n2b] = size(B);
			if ~(n1a == n1b) || ~(n2a == n2b)
				if (obj.printMessages)
					fprintf('*** Difference in cell array %s size. ***\n', varargin{1});
				end
				deltaCount = 0;
				maxDelta = 0;
				maxPercentDifference = 0;
				eq = false;
				return;
			end
			A2 = [];
			B2 = [];
			for i = 1:n1a
				for j = 1:n2a
					aFlat = reshape(A{i, j},1,[]);
					bFlat = reshape(B{i, j},1,[]);
					A2 = cat(2, A2, aFlat);
					B2 = cat(2, B2, bFlat);
				end
			end
			[eq, deltaCount, maxDelta, maxPercentDifference] = obj.compareMatricies(A2, B2, varargin{1});
		end
		
		
		% A method to recognize a lower bound, clean close values, and throw an exception otherwise.
		function x = enforceZeroLowerBound(obj, x)
			if (x < -obj.zeroDelta)
				throw(MException('MATLAB:ZeroLowerBoundExceeded', 'Zero lower bound exceeded.'));
			end
			x(x < obj.scalarZero) = obj.scalarZero;
		end
		
		% A method to cap values to a maximum value of one.
		function x = enforceOneUpperBound(obj, x)
			x(x > obj.scalarOne) = obj.scalarOne;
		end
		
		% A method to ensure sum(x) = 1, and throw an exception otherwise.
		function x = normalizeProbability(obj, x)
			x = obj.enforceZeroLowerBound(x);
			sumX = sum(x); % the sum is guaranteed to be positive.
			if (abs(sumX - obj.scalarOne) > 2.0 * obj.zeroDelta * length(x))
				throw(MException('MATLAB:ProbabilityNormalizationFailed', 'Probability vector does not match one.'));
			end
			x = x ./ sumX;
		end
	end
	
end

