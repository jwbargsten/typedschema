df1.select(F.col(myschema.a)).show()
df1.select(myschema.a).show()
df1.select(myschema.a.col).show()
df1.select(myschema.a.c).show()