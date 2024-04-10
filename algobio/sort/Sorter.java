package sort;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.util.regex.Pattern;
import java.util.function.Function;

import java.nio.file.Files;
import java.nio.file.Path;

import java.io.IOException;

// base interface for sort implementations
@FunctionalInterface
public interface Sorter{
	// main method if implementing this interface
	// preferentially use ArrayLists or some other List type with random access in O(1)
	public<T> List<T> sort(List<T> list, Comparator<? super T> comp, int start, int end);

	// defers to sort(arr[], comp, int start, int end), setting the boundary as the entire array
	public default<T> List<T> sort(List<T> list, Comparator<? super T> comp){
		return this.sort(list, comp, 0, list.size());
	}

	// equivalent functions, but declared on arrays
	// java does not like creating generic arrays, so this returns a List instead
	// TODO maybe find workaround?
	public default<T> List<T> sort(T[] arr, Comparator<? super T> comp, int start, int end){
		return this.sort(Arrays.asList(arr), comp, start, end);//.toArray(new T[0]);
	}
	public default<T> List<T> sort(T[] arr, Comparator<? super T> comp){
		return this.sort(Arrays.asList(arr), comp, 0, arr.length);//.toArray(new T[0]);
	}

	// curries the comparator out of a Sorter, for convenience
	public class Currier<T>{
		Comparator<? super T> comp;
		Sorter sorter;
		public Currier(Sorter sorter, Comparator<? super T> comp){
			this.comp = comp;
			this.sorter = sorter;
		}
		public List<T> sort(List<T> list, int start, int end){
			return this.sorter.sort(list, comp, start, end);
		}
		public List<T> sort(List<T> list){
			return this.sorter.sort(list, comp);
		}
		public List<T> sort(T[] arr, int start, int end){
			return this.sorter.sort(arr, comp, start, end);
		}
		public List<T> sort(T[] arr){
			return this.sorter.sort(arr, comp);
		}
	}

	// Marker annotations for differentiating the implementation kinds
	@interface SimpleSorter{}
	@interface RecursiveSorter{}
	@interface LinearSorter{}


	// i/o code, also reports runtimes for benchmarking
	public static void main(String[] args){
		long startStamp = System.currentTimeMillis();
		if(args.length < 4){
			System.out.println("Nicht genügend Argumente!");
			System.out.println("Usage: [sort|bench] [integer|lines] [insertion|heap|merge|quick] <Dateipfad>");
			System.exit(1);
		}
		Path input = Path.of(args[3]);
		// not declaring the generic type here will throw a warning
		// but allow the type to be dynamically set at file imputing
		// wishing for trait objects...
		List<? extends Comparable> list = null;
		Sorter sorter = null;

		// using case fallthrough for multiple aliases
		switch(args[2]){
			case "i":
			case "insertion":
			case "InsertionSort":
				sorter = new InsertionSorter();
				break;
			case "m":
			case "merge":
			case "MergeSort":
				sorter = new MergeSorter();
				break;
			case "q":
			case "quick":
			case "QuickSort":
				sorter = new QuickSorter();
				break;
			case "h":
			case "heap":
			case "HeapSort":
				sorter = new HeapSorter();
				break;
		}

		// parse the file
		switch(args[1]){
			case "integer":
			case "int":
				try{
					list = Files.lines(input)
						.flatMap(Pattern.compile(",")::splitAsStream)
						.map(Integer::parseInt)
						.collect(Collectors.toList());
					//.collect(Collectors.toCollection(ArrayList::new)); // guarantees the List to be an ArrayList
				} catch(IOException e){
					e.printStackTrace();
				}
				break;
			case "string":
			case "lines":
			case "sort":
			case "POSIX":
				try{
				list = Files.lines(input)
					.collect(Collectors.toList());
				} catch(IOException e){
					e.printStackTrace();
				}
				break;

		}

		long parseStamp = System.currentTimeMillis();
		List sorted = sorter.sort(list, Comparator.comparing(Function.identity()));
		long endStamp = System.currentTimeMillis();
		switch(args[0]){
			case "bench":
				System.out.println((endStamp-parseStamp) + "," + (endStamp-startStamp));
				break;
			case "sort":
				for(Object s: sorted) // still wishing for them trait objects...
					System.out.println(s);
				break;
		}
		System.exit(0);
	}
}
