class CustomerDataSchema(Schema):
    a = Column(LongType(), True)
    b = Column(DoubleType(), True)
    c = Column(StringType(), True)
    d = Column(DateType(), True)
    e = Column(TimestampType(), True)
    f = Column(LongType(), True)
customer_data_schema = CustomerDataSchema()
