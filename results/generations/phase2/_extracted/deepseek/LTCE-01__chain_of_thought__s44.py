# Check if the verbose parameter is passed
if "-v" in parameters or "--verbose" in parameters:
    # Get the verbose parameter
    if "-v" in parameters:
        verbose_param_index = parameters.index("-v") + 1
    else:
        verbose_param_index = parameters.index("--verbose") + 1
        
    verbose_param = parameters[verbose_param_index]
    
    # Check if the verbose parameter is True
    if verbose_param.lower() == "true" or verbose_param.lower() == "t":
        verbose = True
    else:
        verbose = False
else:
    verbose = False
