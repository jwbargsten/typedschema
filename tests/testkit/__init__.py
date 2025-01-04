def _calc_row_hash(d):
    return "||".join([str(i[1]) for i in sorted(d.items(), key=lambda x: x[0])])


def _rows_to_dicts(rows, sort=True):
    res = [row.asDict() for row in rows]
    if sort:
        return sorted(res, key=_calc_row_hash)
    return res


def df_assert_equal(rows_df1, rows_df2, sort=True, msg=None):
    assert _rows_to_dicts(rows_df1, sort=sort) == _rows_to_dicts(rows_df2, sort=sort), msg
