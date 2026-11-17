config = Config()
config.config["world"] = {"regions": "1,2,3,4"}
result = run("1,2,3,4")
print(result)  # Output should be [1, 2, 3, 4]
