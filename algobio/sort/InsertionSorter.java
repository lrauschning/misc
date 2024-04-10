package sort;

import java.util.List;
import java.util.Comparator;
import java.util.Collections;

@Sorter.SimpleSorter
public class InsertionSorter implements Sorter{

	public<T> List<T> sort(List<T> list, Comparator<? super T> comp, int start, int end){
		for(int index=start+1; index<end; index++) { // position 0 does not need swapping with itself
			for(int insert=index-1;
					insert >= start && comp.compare(list.get(insert), list.get(insert+1)) <= 0;
					insert--){
				Collections.swap(list, insert+1, insert);
			}
		}
		return list;
	}

}
