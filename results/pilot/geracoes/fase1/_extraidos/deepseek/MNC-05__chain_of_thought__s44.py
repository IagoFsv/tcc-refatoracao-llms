assert executar({'containers': [{'name': 'container1', 'field1': 'value1'}, {'name': 'container2', 'field1': 'value2'}]}) == \
    {'services': {'container1': {'field1': 'value1'}, 'container2': {'field1': 'value2'}}, 'containers': None}
