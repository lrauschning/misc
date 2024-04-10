package sort;

import java.util.List;
import java.util.Comparator;
import java.util.Collections;

@Sorter.RecursiveSorter
public class HeapSorter implements Sorter{

	public<T> List<T> sort(List<T> list, Comparator<? super T> comp, int start, int end){
		// make a heap, starting in the middle of the selection
		// saves on checking the leaves
		for (int index = (end-start)/2; index >= 0; index--)
			this.heapify(list, comp, index, start, end);

		// unwind the heap towards the end; end is used as a counter variable
		while(end > start){
			Collections.swap(list, start, end-1);
			end--;
			this.heapify(list, comp, start, start, end);
		}
		return list;
	}

	// performs the sift-down operation
	// for a max-heap starting at start and ending at end
	// implemented without recursion
	// start/end represent the interval, begin the point to start the heapification from
	private<T> void heapify(List<T> list, Comparator<? super T> comp, int begin, int start, int end){
		for( ; ; ){
			int pmin = begin;
			int chleft = 2*pmin +1;
			int chright = 2*pmin +2;
			// check if one of the children violates the heap condition
			if(chleft < end && comp.compare(list.get(pmin+start), list.get(chleft+start)) > 0)
				pmin = chleft;
			if(chright < end && comp.compare(list.get(pmin+start), list.get(chright+start)) > 0)
				pmin = chright;

			if(pmin == begin)
				break;

			Collections.swap(list, start+begin, start+pmin);
			begin = pmin; // reassigns the input, effectively replacing recursive calls
		}
	}
}
