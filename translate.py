import java.util as util
import edu.cmu.tetrad.data as td


def pandas_to_tetrad(df, int_as_cont=False):
    dtypes = ["float16", "float32", "float64"]
    if int_as_cont:
        dtypes += [f"int{2 ** i}" for i in range(3, 7)]
        dtypes += [f"uint{2 ** i}" for i in range(3, 7)]

    cols = df.columns
    discrete_cols = [col for col in cols if df[col].dtypes not in dtypes]
    category_map = {}

    for col in discrete_cols:
        category_map[col] = {val: i for i, val in enumerate(df[col].unique())}
    df = df.replace(category_map)

    values = df.values
    n, p = df.shape

    variables = util.ArrayList()

    for col in cols:
        if col in discrete_cols:
            categories = util.ArrayList()
            for category in category_map[col]:
                categories.add(str(category))
            variables.add(td.DiscreteVariable(str(col), categories))
        else:
            variables.add(td.ContinuousVariable(str(col)))

    if len(discrete_cols) == len(cols):
        databox = td.IntDataBox(n, p)
    elif len(discrete_cols) == 0:
        databox = td.DoubleDataBox(n, p)
    else:
        databox = td.MixedDataBox(variables, n)

    for col, var in enumerate(values.T):
        for row, val in enumerate(var):
            databox.set(row, col, val)

    return td.BoxDataSet(databox, variables)
