differences = diff_schemas(myschema, df2.schema)

for change, my, other in differences:
    print(f"{change} {my} {other}")