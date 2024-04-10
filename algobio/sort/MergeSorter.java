package sort;

import java.util.List;
import java.util.ArrayList;
import java.util.Comparator;

@Sorter.RecursiveSorter
public class MergeSorter implements Sorter{

	public<T> List<T> sort(List<T> list, Comparator<? super T> comp, int start, int end){
		// termination condition(s)
		if(end-start<=1)
			return list.subList(start, end);
		// additional termination condition to save recursive function calls
		if(end-start==2 && comp.compare(list.get(start), list.get(end-1)) <= 0)
			return list.subList(start, end);
		// recursive calls
		// List.sublist() could also have been used
		int middle = (start + end)/2;
		List<T> left = this.sort(list, comp, start, middle);
		List<T> right = this.sort(list, comp, middle, end);
		// Merge step
		List<T> ret = new ArrayList<T>(end-start); // preinitialise to return size
		int pleft = 0;
		int pright = 0;
		// Merge main body
		while(pleft < left.size() && pright < right.size()){
			if(comp.compare(left.get(pleft), right.get(pright)) < 0){
				ret.add(right.get(pright));
				pright++;
			} else {
				ret.add(left.get(pleft));
				pleft++;
			}
		}
		// Merge the rest; in practice, only one of these should actually run
		for( ; pleft < left.size(); pleft++)
			ret.add(left.get(pleft));
		for( ; pright < right.size(); pright++)
			ret.add(right.get(pright));

		return ret;
	}
}
