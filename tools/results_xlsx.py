import xlsxwriter
import argparse

def parse_args():
    parser = argparse.ArgumentParser("Summarizes transliteration results.")
    parser.add_argument("-r", "--results", required="Results TSV table")
    parser.add_argument("-o", "--output-xlsx", required="Output XLSX table")
    return parser.parse_args()


def parse_tsv_line(line):
    line = line.rstrip('\n')
    return line.split('\t')


def read_tsv(tsv_path):
    table = []
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        for line in tsv_file:
            line = line.rstrip('\n')
            table.append(line.split('\t'))
            assert len(table[0]) == len(table[-1])
    return table


def col_name2index(table, col_name):
    return table[0].index(col_name)


def unique_values(table, col_name):
    col_index = col_name2index(table, col_name)
    values = set()
    for row in table[1:]:
        values.add(row[col_index])
    return sorted(values)


def grep(table, col_name, value):
    col_index = col_name2index(table, col_name)
    out_table = []
    
    # title
    out_table.append(table[0])

    for row in table:
        if row[col_index] != value:
            continue
        out_table.append(row)
    
    return out_table


def cut(table, col_names):
    col_indices = [ col_name2index(table, name) for name in col_names ]
    out_table = []
    for row in table:
        out_row = [ row[index] for index in col_indices ]
        out_table.append(out_row)
    return out_table


def get_col(table, col_name):
    values = []
    for row in cut(table, [col_name]):
        assert len(row) == 1
        values.append(row[0])
    return values


def to_float(table, col_name):
    col_index = col_name2index(table, col_name)
    for row in table[1:]:
        row[col_index] = float(row[col_index])


def get_format(value, special_value):
    global normal_format
    global bold_format
    if value != special_value:
        return normal_format
    else:
        return bold_format


def fill_dataset_cells(dataset_table, dataset_name, row_idx, col_idx, ws):
    to_float(dataset_table, "wer")
    to_float(dataset_table, "cer")

    # compute min values for wer / cer: we need this for formatting
    min_wer = min(get_col(dataset_table, "wer")[1:])
    min_cer = min(get_col(dataset_table, "cer")[1:])

    # ws.write(row_idx, col_idx + 0, dataset_name.upper(), bold_format)
    global dataset_name_format
    ws.merge_range(row_idx, col_idx, row_idx, col_idx + 2, dataset_name.upper(), dataset_name_format)

    row_idx += 1
    ws.write(row_idx, col_idx + 0, "tool", bold_format)
    ws.write(row_idx, col_idx + 1, "wer", bold_format)
    ws.write(row_idx, col_idx + 2, "cer", bold_format)

    row_idx += 1
    for tool, wer, cer in dataset_table[1:]:
        ws.write(row_idx, col_idx + 0, tool, normal_format)
        ws.write(row_idx, col_idx + 1, wer, get_format(wer, min_wer))
        ws.write(row_idx, col_idx + 2, cer, get_format(cer, min_cer))
        row_idx += 1


def cumulate_dataset_results(total, dataset_table):
    if not total:
        return dataset_table
    
    result = []
    assert len(total) == len(dataset_table)

    result.append(total[0])
    for i in range(1, len(total)):
        total_row = total[i]
        dataset_row = dataset_table[i]

        assert total_row[0] == dataset_row[0]
        result.append([total_row[0], total_row[1] + dataset_row[1], total_row[2] + dataset_row[2]])

    return result


def divide_total(total, count):
    for row in total[1:]:
        row[1] /= count
        row[2] /= count

def fill_alphabet_worksheet(alphabet_results, datasets, ws):
    next_row = 0

    total = None

    # get dataset results
    for dataset in datasets:
        # extract data
        dataset_results = grep(alphabet_results, "dataset", dataset)
        dataset_name = dataset_results[1][col_name2index(dataset_results, "dataset")]
        dataset_table = cut(dataset_results, ["tool", "wer", "cer"])
        
        # output cells to xlsx
        fill_dataset_cells(dataset_table, dataset_name, next_row, 0, ws)

        # move to position after table for this dataset
        next_row += len(dataset_results) + 2

        # cumulate values for macro average
        total = cumulate_dataset_results(total, dataset_table)

    # divide to get macro average table
    divide_total(total, len(dataset))

    # output macro average table
    fill_dataset_cells(total, "MACRO AVG", 0, 5, ws)



def split_datasets(datasets):
    test_sets = []
    dev_sets = []
    for dataset in datasets:
        tokens = dataset.lower().split("_")
        assert len(tokens) > 1
        dataset_type = tokens[-1]
        if dataset_type == "test":
            test_sets.append(dataset)
        elif dataset_type == "dev":
            dev_sets.append(dataset)
        else:
            assert False, "Unsupported dataset name format: %s" % dataset
    return test_sets, dev_sets



if __name__ == "__main__":
    args = parse_args()

    # load table
    table = read_tsv(args.results)
    assert table[0] == ["tool", "dataset", "alphabet", "wer", "cer", "#words", "wins", "wsub", "wdel", "#chars", "cins", "csub", "cdel"]

    # get all alphabets and datasets
    alphabets = unique_values(table, "alphabet")
    datasets = unique_values(table, "dataset")
    test_sets, dev_sets = split_datasets(datasets)

    # get all tools that are measured
    tools = unique_values(table, "tool")

    # create xlsx workbook
    wb = xlsxwriter.Workbook(args.output_xlsx)

    global dataset_name_format
    dataset_name_format = wb.add_format({
        'bg_color': '#000000',
        'font_color': '#FFFFFF',
        'border': 1,
        'border_color': '#FFFFFF',
        'bold': True
    })
    
    global bold_format 
    bold_format = wb.add_format({'bold': True, 'border': 1})
    global normal_format
    normal_format = wb.add_format({'bold': False, 'border': 1})

    for alphabet in alphabets:
        # get results for this alphabet
        alphabet_results = grep(table, "alphabet", alphabet)

        # one worksheet per alphabet
        ws = wb.add_worksheet(alphabet.upper() + " " + "DEV")
        fill_alphabet_worksheet(alphabet_results, dev_sets, ws)
        ws.autofit()

        # one worksheet per alphabet
        ws = wb.add_worksheet(alphabet.upper() + " " + "TEST")
        fill_alphabet_worksheet(alphabet_results, test_sets, ws)
        ws.autofit()

    # Close to save
    wb.close()

