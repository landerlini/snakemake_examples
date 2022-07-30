# Example 1. Transform and reduce
A very simple example with a transform and reduce diagram.

A  first step, named *production*, store in a pickle file a 
user-defined number passed as an argument, then the pickle file 
is read in a second step, named *transformation*, it is multiplied 
by 2 and the result is stored in a new pickle file. 
Finally, in a third step, named *reduction*, all the pickle files 
obtained from *transformation* are loaded, the contained numbers 
are summed up and the result is stored in a pickle file.

This problem is extremely simple but allows to:
 * identify multiple dependencies for a single task 
   (reduction depends on the success of all the transformation tasks)
 * provide an example for jobs without input dependencies (production) 
   that can be processed simultaneously.
 * provide an example for jobs with input dependencies (transform) 
   that can be processed as soon as the dependencies are ready.

To ease the distribution, the three steps (production, transformation
and reduction) are defined in a single file, named `job.py`.
The logic of the dependency diagram discussed above is defined in 
the `Snakefile`.

### Running the example 
Move to the directory where the `Snakefile` is placed and run
```
snakemake -j<n_cores> --forceall
```
where:
 * `<n_cores>` is the maximum number of tasks that can be run in parallel,
 * `--forceall` requires snakemake to rerun the whole graph

To visualize the list of tasks (instead of executing them), the `-np` 
option is made available:
```
snakemake -j<n_cores> --forceall -np
```

### Understanding what is happening
By defaul the process is very fast and it is difficult to follow what is 
happening. An option, `--waited-time <seconds>` allows to add a `sleep`
operation to each task to make it clearer how snakemake solves the 
diagram.



