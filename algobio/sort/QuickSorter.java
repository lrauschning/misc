package sort;

import java.util.List;
import java.util.Comparator;
import java.util.Collections;

@Sorter.RecursiveSorter
public class QuickSorter implements Sorter{
	// This implementation uses a central pivot
	public<T> List<T> sort(List<T> list, Comparator<? super T> comp, int start, int end){
		// termination condition(s)
		if(end-start<=1)
			return list;
		// additional termination condition to save recursive function calls
		if(end-start==2 && comp.compare(list.get(start), list.get(end-1)) > 0)
			return list;

		// buffer pivot at the start, to avoid weirdness later
		Collections.swap(list, start, (start + end)/2);
		T pivot = list.get(start);

		// partition the Array
		int left = start+1;
		int right = end-1;
		for( ; ; ){
			// right-search for an element that is lesser than the pivot
			while(right > start && comp.compare(list.get(right), pivot) <= 0)
				right--;
			// left-search for an element that is greater than the pivot
			while(left < end && comp.compare(pivot, list.get(left)) <= 0)
				left++;

			// swap the two, unless they have reached each other
			if(left >= right)
				break;
			else
				Collections.swap(list, left, right);
		}

		// replace the pivot at the correct position
		// right now points at the last left element,
		// so swap(start, right) preserves the ordering on pivot
		Collections.swap(list, start, right);
		// recursive calls
		this.sort(list, comp, start, right);
		this.sort(list, comp, right+1, end);

		return list;
	}
}
