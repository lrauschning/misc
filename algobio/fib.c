#include<argp.h>
#include<stdio.h>
#include<stdlib.h>
#include<math.h>

unsigned long fn_calls = 0;
unsigned long adds = 0;
unsigned long mults = 0;

unsigned long long fib_rec(unsigned long n){
	fn_calls++;
	if(n < 2){
		return 1;
	}
	adds++;
	return fib_rec(n-1) + fib_rec(n-2);
}

unsigned long long fib_dp(unsigned long in){
	fn_calls++;
	unsigned int n = in;
	unsigned long long buf1 = 1;
	unsigned long long buf2 = 1;

	n--;
	while(n--){
		adds++; buf1 += buf2;
		if(!n--){
			return buf1;
		};
		adds++; buf2 += buf1;
	}
	return buf2;

	/* not actually faster, but leaving it here just because
	n += 2;
	while((n -= 2) > 1){
		adds += 2;
		buf2 += buf1;
		buf1 += buf2;
	}
	return n ? buf1:buf2;
	*/
}

unsigned long long fib_smart(unsigned long n){
	fn_calls++;
	if(n < 2){
		return 1;
	}

	//mults++; // not sure if division counts?
	unsigned long k = n/2;
	unsigned long long kval = fib_smart(k);
	// j := k-1, because alphabetically j comes just before k
	unsigned long long jval = fib_smart(k-1);

	// choose appropriate formula, use automatic rounding
	// mults/adds is constant anyway
	adds += 2; mults += 2;

	if(n % 2){
		return (kval*jval) + (kval*fib_smart(k+1));
	} else {
		return (kval*kval) + (jval*jval);
	}
}

unsigned long long fib_exp(unsigned long in){
	fn_calls++;
	// define some constants so that they dont need to be recalculated every time
	const long double phi = 1.6180339887498948482045868343656381177203091798057628621354486227;
	const long double psi = -0.618033988749894848204586834365638117720309179805762862135448622;
	// sqrt(5)
	const long double root = 2.2360679774997896964091736687312762354406183596115257242708972454;
	// adapt to zero-based indexing
	unsigned long n = in +1;

	adds++;
	// mults += 2*n; // + 1; // not really relevant here
	return (powl(phi, n) - powl(psi, n))/root;
}


int main(int argc, char **argv){
	unsigned long long (*fun) (unsigned long) = NULL;
	unsigned long n = 0;
	int stats = 0;
	// argument parsing
	struct argp_option options[] = {
		{ 0, 'n', "NUM", 0, "Index of the Fibonacci number to calculate."},
		{ "bench", 'b', 0, 0, "Print only performance statistics.\nPrinted as #fn_calls,#multiplications,#additions ."},
		{ 0, 0, 0, 0, "Fibonacci Algorithms:", 1},
		{ "recursive", 'r', 0, 0, "Use a simple recursive algorithm in O(2^n)."}, 
		{ "dp", 'd', 0, 0, "Use a dynamic programming algorithm in O(n)."}, 
		{ "smart", 's', 0, 0, "Use a clever recursive algorithm in O(log n)."},
		{ "exponential", 'e', 0, 0, "Use the explicit formula."},
		{0}
	};

	int parse_opt (int key, char *arg, struct argp_state *state){ 
		switch (key) {
			case 'r':
				fun = &fib_rec;
				break;
			case 'd':
				fun = &fib_dp;
				break;
			case 's':
				fun = &fib_smart;
				break;
			case 'e':
				fun = &fib_exp;
				break;
			case 'n':
				char** temp = NULL;
				n = strtoul(arg, temp, 10);
				//n = atoi(arg);
				break;
			case 'b':
				stats = 1;
				break;
			case ARGP_KEY_END:
				if(fun == NULL){
					argp_failure(state, 1, 0, "No algorithm supplied!");
				}
				if(!n){
					argp_failure(state, 1, 0, "No index supplied!");
				}
				break;
		}
		return 0;
	}

	struct argp argp = {options, parse_opt, ""};
	if(argp_parse(&argp, argc, argv, 0, 0, 0)){
		printf("invalid arguments!");
		return 1;
	}

	unsigned long long ret = fun(n);

	if(stats){
		printf("%lu,%lu,%lu\n", fn_calls, adds, mults);
	} else {
		printf("%llu\n", ret);
	}

	return 0;
}
