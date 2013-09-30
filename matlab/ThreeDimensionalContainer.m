classdef ThreeDimensionalContainer < handle

	properties  (SetAccess = private, GetAccess = private)
		backingContainer;
	end
	
	methods
		function obj = ThreeDimensionalContainer()
			obj.backingContainer = containers.Map('KeyType', 'int64', 'ValueType', 'any');
		end
		
		function val = get(obj, i, j, k)
			y = obj.backingContainer(i);
			val = y.get(j, k);
		end
		
		function set(obj, val, i, j, k)
			if (~isKey(obj.backingContainer, {i}))
				obj.backingContainer(i) = TwoDimensionalContainer();
			end
			y = obj.backingContainer(i);
			y.set(val, j, k);
		end
		
		function len = lengthOfDimensionOne(obj)
			len = length(obj.backingContainer);
		end
		
		function len = lengthOfDimensionTwo(obj, i)
			y = obj.backingContainer(i);
			len = y.lengthOfDimensionOne();
		end
		
		function len = lengthOfDimensionThree(obj, i, j)
			y = obj.backingContainer(i);
			len = y.lengthOfDimensionTwo(j);
		end
	end
	
end

