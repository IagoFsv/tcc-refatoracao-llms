# Example usage
item1 = {
    "langs": {
        "overrides": {
            "python": "Python override"
        }
    }
}

item2 = {
    "langs": {
        "overrides": None
    }
}

print(run(item1))  # Should output: 'Python override'
print(run(item2))  # Should output: None
